"""
Step 0b — live ingest: pull new ARGUS readings straight from the API into
Postgres, on a loop. Postgres is the only store — no local TTL, sidecar, or
state file. The API pages newest-first, so each cycle walks from page 1 until
it reaches readings already in Postgres; the very first run (or one that was
interrupted) walks all the way back instead, and `ingest_state` records once
that full backfill has completed. Rows dedup via ON CONFLICT DO NOTHING on
their primary keys, so re-fetching an overlap window is always safe. Pairs with obda/ (Ontop) for a
live SPARQL endpoint — see obda/docker-compose.yml's `ingest` service.

For local dev without Postgres, use 0a_offline_readings.py instead (writes a
TTL file for the in-memory RdflibBackend).

    python scripts/0b_online_ingest.py             # loop forever, default 3600s
    python scripts/0b_online_ingest.py --once       # single cycle, then exit
    ARGUS_INGEST_INTERVAL=300 python scripts/0b_online_ingest.py
"""

from __future__ import annotations
import argparse
import importlib
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_rd = importlib.import_module("0a_offline_readings")

DSN = os.environ.get("ARGUS_PG_DSN", "postgresql://argus:argus@localhost:5432/argus")
SCHEMA_SQL = Path(__file__).resolve().parent.parent / "obda" / "schema.sql"
INTERVAL = int(os.environ.get("ARGUS_INGEST_INTERVAL", "3600"))
# Once backfilled, a cycle stops after this many consecutive pages with no new
# readings — a little slack for late-arriving records landing behind the head.
OVERLAP_PAGES = int(os.environ.get("ARGUS_INGEST_OVERLAP_PAGES", "2"))


def _num(value: Any) -> tuple[float | None, str | None]:
    # Split a reading value into (numeric, text) — mirrors 0a_offline_readings typing.
    if isinstance(value, bool):
        return None, str(value).lower()
    try:
        return float(value), None
    except (ValueError, TypeError):
        return None, (None if value is None else str(value))


def build_rows(readings: list[dict]) -> dict[str, list[tuple]]:
    sites, nodes, sensors, props = {}, {}, {}, {}
    readings_rows, obs_rows = [], []

    for reading in readings:
        rid = _rd.reading_stable_id(reading)
        site = _rd._safe_text(_rd.reading_site(reading), "unknown_site")   # partner channels → pilot site
        sid = _rd._make_uri_part(site)
        sensor_id = _rd._safe_text(reading.get("sensor_id"), "unknown_sensor")
        node_id = _rd._safe_text(reading.get("node_id"), "unknown_node")
        ts = reading.get("ts")

        sites.setdefault(sid, (sid, site))

        coords = _rd._load_node_coords().get(node_id, {})
        nodes.setdefault(node_id, (
            node_id,
            reading.get("node_label") or reading.get("node_name") or node_id,
            reading.get("node_name"), reading.get("node_model"),
            coords.get("latitude"), coords.get("longitude"), coords.get("altitude"),
        ))

        sensors.setdefault(sensor_id, (
            sensor_id,
            reading.get("sensor_name") or reading.get("node_label")
            or reading.get("node_name") or sensor_id,
            reading.get("sensor_model"),
        ))

        readings_rows.append((
            rid, ts, sid, sensor_id, node_id,
            reading.get("reading_type"), reading.get("topic"),
            reading.get("topic_id"), reading.get("device_group_id"),
        ))

        for idx, obs in enumerate(_rd._extract_observations(reading.get("payload"))):
            quantity, value, unit = obs.get("quantity"), obs.get("value"), obs.get("unit")
            if quantity is None or value is None:
                continue
            q = _rd._safe_text(quantity)
            props.setdefault(q, (q, q))
            oid = _rd._make_hash({"reading_id": rid, "index": idx,
                                  "quantity": q, "value": value, "unit": unit})
            num, txt = _num(value)
            obs_rows.append((oid, rid, q, num, txt, unit, ts))

    return {
        "sites": list(sites.values()), "nodes": list(nodes.values()),
        "sensors": list(sensors.values()), "observed_properties": list(props.values()),
        "readings": readings_rows, "observations": obs_rows,
    }


_INSERT = {
    "sites": "INSERT INTO sites VALUES (%s,%s) ON CONFLICT (site_id) DO NOTHING",
    "nodes": "INSERT INTO nodes VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (node_id) DO NOTHING",
    "sensors": "INSERT INTO sensors VALUES (%s,%s,%s) ON CONFLICT (sensor_id) DO NOTHING",
    "observed_properties": "INSERT INTO observed_properties VALUES (%s,%s) ON CONFLICT (property_id) DO NOTHING",
    "readings": "INSERT INTO readings VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (reading_id) DO NOTHING",
    "observations": "INSERT INTO observations VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (observation_id) DO NOTHING",
}
_ORDER = ["sites", "nodes", "sensors", "observed_properties", "readings", "observations"]


def _get_state(cur, key: str, default: str) -> str:
    cur.execute("SELECT value FROM ingest_state WHERE key = %s", (key,))
    row = cur.fetchone()
    return row[0] if row else default


def _set_state(cur, key: str, value: str) -> None:
    cur.execute(
        "INSERT INTO ingest_state (key, value) VALUES (%s, %s) "
        "ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value",
        (key, value),
    )


def _apply_schema(conn) -> None:
    """CREATE TABLE IF NOT EXISTS is not safe under concurrent execution —
    this and 0c_ingest_governance_pg.py both apply schema.sql on startup, and
    Postgres can raise a transient UniqueViolation on its own pg_type catalog
    (pg_type_typname_nsp_index) when two sessions create the same table at
    the same instant, even though exactly one of them ends up creating it
    either way. Retry instead of surfacing that as a real failure and waiting
    a full cycle for it to resolve itself."""
    import psycopg
    sql = SCHEMA_SQL.read_text()
    for attempt in range(5):
        try:
            with conn.cursor() as cur:
                cur.execute(sql)
            conn.commit()
            return
        except psycopg.errors.UniqueViolation:
            conn.rollback()
            time.sleep(0.5 * (attempt + 1))
    with conn.cursor() as cur:  # one last try, let a real error surface
        cur.execute(sql)
    conn.commit()


def ingest_cycle(conn, max_records: int | None = None) -> int:
    """One fetch-and-load pass against the live API. Returns new readings loaded."""
    _apply_schema(conn)
    with conn.cursor() as cur:
        backfilled = _get_state(cur, "backfill_complete", "0") == "1"
    conn.commit()
    if not backfilled:
        print("Full backfill not completed yet — walking the whole API history.", flush=True)

    pages_iter, progress = _rd.fetch_readings_paginated(max_records=max_records)

    total, idle_pages = 0, 0
    with conn.cursor() as cur:
        for page_records in pages_iter:
            rows = build_rows(page_records)
            ids = [r[0] for r in rows["readings"]]
            cur.execute("SELECT reading_id FROM readings WHERE reading_id = ANY(%s)", (ids,))
            new = len(set(ids) - {r[0] for r in cur.fetchall()})
            for table in _ORDER:
                if rows[table]:
                    cur.executemany(_INSERT[table], rows[table])
            total += new
            _set_state(cur, "last_successful_page", str(progress["last_successful_page"]))
            conn.commit()

            idle_pages = idle_pages + 1 if new == 0 else 0
            if backfilled and idle_pages >= OVERLAP_PAGES:
                print(f"Caught up — {idle_pages} page(s) with nothing new.", flush=True)
                break

        if progress["reached_end"] and not backfilled:
            _set_state(cur, "backfill_complete", "1")
            conn.commit()
            print("Full backfill complete.", flush=True)

    return total


def run_once(max_records: int | None = None) -> None:
    import psycopg  # psycopg 3
    ts = datetime.now(timezone.utc).isoformat()
    print(f"[{ts}] ingest cycle start — {DSN}", flush=True)
    with psycopg.connect(DSN) as conn:
        n = ingest_cycle(conn, max_records=max_records)
    print(f"[{ts}] ingest cycle done — {n} new reading(s).", flush=True)


def main() -> None:
    ap = argparse.ArgumentParser(description="Live-load ARGUS readings into Postgres for Ontop.")
    ap.add_argument("--once", action="store_true", help="Run a single cycle and exit.")
    ap.add_argument("--max-records", type=int, default=None,
                    help="Cap records per cycle (testing / throttling a first backfill).")
    args = ap.parse_args()

    if args.once:
        run_once(max_records=args.max_records)
        return

    print(f"Live ingest loop starting — every {INTERVAL}s.", flush=True)
    while True:
        try:
            run_once(max_records=args.max_records)
        except Exception as e:
            print(f"  ingest cycle raised: {type(e).__name__}: {e}", flush=True)
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
