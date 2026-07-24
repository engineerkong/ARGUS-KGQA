"""
Step 0b — live ingest: pull new ARGUS readings straight from the API into
Postgres, on a loop. Postgres is the only store — no local TTL, sidecar, or
state file. Pagination bookmarks live in the `ingest_state` table and rows
dedup via ON CONFLICT DO NOTHING on their primary keys, so re-fetching the
overlap window on every cycle is always safe. Pairs with obda/ (Ontop) for a
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
# Re-walk the last few pages each cycle: the API may still be settling records
# into them, and ON CONFLICT DO NOTHING makes re-processing free.
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
        site = _rd._safe_text(reading.get("site"), "unknown_site")
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


def ingest_cycle(conn, max_records: int | None = None) -> int:
    """One fetch-and-load pass against the live API. Returns readings loaded."""
    with conn.cursor() as cur:
        cur.execute(SCHEMA_SQL.read_text())
        last_page = int(_get_state(cur, "last_successful_page", "0"))
    conn.commit()

    start_page = max(1, last_page - OVERLAP_PAGES + 1)
    pages_iter, progress = _rd.fetch_readings_paginated(max_records=max_records, start_page=start_page)

    total = 0
    with conn.cursor() as cur:
        for page_records in pages_iter:
            rows = build_rows(page_records)
            for table in _ORDER:
                if rows[table]:
                    cur.executemany(_INSERT[table], rows[table])
            total += len(page_records)
            _set_state(cur, "last_successful_page", str(progress["last_successful_page"]))
            conn.commit()

    return total


def run_once(max_records: int | None = None) -> None:
    import psycopg  # psycopg 3
    ts = datetime.now(timezone.utc).isoformat()
    print(f"[{ts}] ingest cycle start — {DSN}", flush=True)
    with psycopg.connect(DSN) as conn:
        n = ingest_cycle(conn, max_records=max_records)
    print(f"[{ts}] ingest cycle done — {n} reading(s) processed.", flush=True)


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
