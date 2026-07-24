"""
Step 2 of the OBDA plan — load raw readings into Postgres for Ontop to map.

Reuses 0_readings' extraction so SQL rows carry the same entities the RDF graph
does. Reads the JSONL sidecar by default (offline); --dry-run builds every row
and reports counts without needing a database.

    python scripts/4_load_postgres.py --dry-run
    python scripts/4_load_postgres.py            # needs psycopg + a running DB
"""

from __future__ import annotations
import argparse
import importlib
import json
import os
from pathlib import Path
from typing import Any

_rd = importlib.import_module("0_readings")

DSN = os.environ.get("ARGUS_PG_DSN", "postgresql://argus:argus@localhost:5432/argus")
SCHEMA_SQL = Path(__file__).resolve().parent.parent / "obda" / "schema.sql"


def _num(value: Any) -> tuple[float | None, str | None]:
    # Split a reading value into (numeric, text) — mirrors 0_readings typing.
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


def _read_sidecar(limit: int | None) -> list[dict]:
    path = _rd.RAW_JSONL_FILE
    if not path.exists():
        raise SystemExit(f"Sidecar not found: {path}. Run 0_readings.py first.")
    out = []
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f):
            if limit is not None and n >= limit:
                break
            try:
                out.append(json.loads(line)["reading"])
            except (json.JSONDecodeError, KeyError):
                continue
    return out


_INSERT = {
    "sites": "INSERT INTO sites VALUES (%s,%s) ON CONFLICT (site_id) DO NOTHING",
    "nodes": "INSERT INTO nodes VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (node_id) DO NOTHING",
    "sensors": "INSERT INTO sensors VALUES (%s,%s,%s) ON CONFLICT (sensor_id) DO NOTHING",
    "observed_properties": "INSERT INTO observed_properties VALUES (%s,%s) ON CONFLICT (property_id) DO NOTHING",
    "readings": "INSERT INTO readings VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (reading_id) DO NOTHING",
    "observations": "INSERT INTO observations VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (observation_id) DO NOTHING",
}
_ORDER = ["sites", "nodes", "sensors", "observed_properties", "readings", "observations"]


def load(rows: dict[str, list[tuple]]) -> None:
    import psycopg  # psycopg 3
    with psycopg.connect(DSN) as conn, conn.cursor() as cur:
        cur.execute(SCHEMA_SQL.read_text())
        for table in _ORDER:
            cur.executemany(_INSERT[table], rows[table])
            print(f"  {table}: {len(rows[table])} row(s)")
        conn.commit()


def main() -> None:
    ap = argparse.ArgumentParser(description="Load raw readings into Postgres for Ontop.")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--dry-run", action="store_true",
                    help="Build rows and report counts without touching the DB.")
    args = ap.parse_args()

    rows = build_rows(_read_sidecar(args.limit))
    if args.dry_run:
        print("Dry run — rows that would be inserted:")
        for table in _ORDER:
            print(f"  {table:20} {len(rows[table])}")
        return
    print(f"Loading into {DSN}")
    load(rows)
    print("Done.")


if __name__ == "__main__":
    main()
