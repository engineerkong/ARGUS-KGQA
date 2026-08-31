"""
Step 0c — governance data (threats/policies/decisions/assets) into Postgres,
for Ontop (see obda/argus.obda). Postgres/Ontop counterpart of
0a_offline_readings.py's ingest_governance(), which writes the same data into
a local TTL instead — same source API, same fields, same site-matching, so
the pipeline's SPARQL is identical on either backend.

Mutable reference data, not an append-only stream like 0b_online_ingest.py's
readings: an edited threshold should overwrite, so this upserts by the API's
own id (ON CONFLICT DO UPDATE) every cycle.

    python scripts/0c_ingest_governance_pg.py             # loop forever, default 3600s
    python scripts/0c_ingest_governance_pg.py --once      # single cycle, then exit
    ARGUS_GOVERNANCE_INTERVAL=300 python scripts/0c_ingest_governance_pg.py
"""

from __future__ import annotations
import argparse
import importlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

_rd = importlib.import_module("0a_offline_readings")

DSN = os.environ.get("ARGUS_PG_DSN", "postgresql://argus:argus@localhost:5432/argus")
SCHEMA_SQL = Path(__file__).resolve().parent.parent / "obda" / "schema.sql"
INTERVAL = int(os.environ.get("ARGUS_GOVERNANCE_INTERVAL", "3600"))


def build_rows() -> dict[str, list[tuple]]:
    session = _rd._make_session()
    threats_rows, policies_rows, decisions_rows, assets_rows = [], [], [], []

    for record in _rd.fetch_all_records(session, f"{_rd.API_ROOT}/threats"):
        md = _rd._parse_metadata(record)
        threats_rows.append((
            str(record["id"]), _rd._safe_text(record.get("name")),
            record.get("description"), md.get("level"),
        ))

    for record in _rd.fetch_all_records(session, f"{_rd.API_ROOT}/policies"):
        md = _rd._parse_metadata(record)
        thresholds = md.get("threshold_overrides")
        threshold_value = None
        threshold_json = None
        if isinstance(thresholds, dict) and thresholds:
            if len(thresholds) == 1:
                (_, v), = thresholds.items()
                if isinstance(v, (int, float)):
                    threshold_value = float(v)
            threshold_json = json.dumps(thresholds, ensure_ascii=False, sort_keys=True)
        pilot = md.get("pilot") or _rd._match_pilot_site(record.get("name"), record.get("description"))
        site_id = _rd._make_uri_part(pilot) if pilot else None
        policies_rows.append((
            str(record["id"]), _rd._safe_text(record.get("name")),
            record.get("description"), md.get("rule"), md.get("threat_name"),
            threshold_value, threshold_json, site_id,
        ))

    for record in _rd.fetch_all_records(session, f"{_rd.API_ROOT}/decisions"):
        md = _rd._parse_metadata(record)
        decisions_rows.append((
            str(record["id"]), _rd._safe_text(record.get("name")),
            record.get("description") or md.get("recommendation"), md.get("urgency"),
        ))

    for record in _rd.fetch_all_records(session, f"{_rd.API_ROOT}/assets"):
        md = _rd._parse_metadata(record)
        pilot = _rd._match_pilot_site(md.get("code"), record.get("name"))
        site_id = _rd._make_uri_part(pilot) if pilot else None
        assets_rows.append((
            str(record["id"]), _rd._safe_text(record.get("name")),
            record.get("description"), md.get("code"), md.get("pilot_number"),
            md.get("country"), md.get("source_url"), site_id,
        ))

    return {"threats": threats_rows, "policies": policies_rows,
            "decisions": decisions_rows, "assets": assets_rows}


_UPSERT = {
    "threats": """
        INSERT INTO threats (threat_id, label, description, threat_level)
        VALUES (%s,%s,%s,%s)
        ON CONFLICT (threat_id) DO UPDATE SET
            label = EXCLUDED.label, description = EXCLUDED.description,
            threat_level = EXCLUDED.threat_level
    """,
    "policies": """
        INSERT INTO policies (policy_id, label, description, rule_id, threat_name,
                               threshold_value, threshold_json, site_id)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (policy_id) DO UPDATE SET
            label = EXCLUDED.label, description = EXCLUDED.description,
            rule_id = EXCLUDED.rule_id, threat_name = EXCLUDED.threat_name,
            threshold_value = EXCLUDED.threshold_value, threshold_json = EXCLUDED.threshold_json,
            site_id = EXCLUDED.site_id
    """,
    "decisions": """
        INSERT INTO decisions (decision_id, label, description, urgency)
        VALUES (%s,%s,%s,%s)
        ON CONFLICT (decision_id) DO UPDATE SET
            label = EXCLUDED.label, description = EXCLUDED.description,
            urgency = EXCLUDED.urgency
    """,
    "assets": """
        INSERT INTO assets (asset_id, label, description, asset_code, pilot_number,
                             country, source_url, site_id)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (asset_id) DO UPDATE SET
            label = EXCLUDED.label, description = EXCLUDED.description,
            asset_code = EXCLUDED.asset_code, pilot_number = EXCLUDED.pilot_number,
            country = EXCLUDED.country, source_url = EXCLUDED.source_url,
            site_id = EXCLUDED.site_id
    """,
}
_ORDER = ["threats", "policies", "decisions", "assets"]


def ingest_cycle(conn) -> dict[str, int]:
    """One fetch-and-upsert pass against the live API. Returns row counts per table."""
    with conn.cursor() as cur:
        cur.execute(SCHEMA_SQL.read_text())
    conn.commit()

    rows = build_rows()
    with conn.cursor() as cur:
        for table in _ORDER:
            if rows[table]:
                cur.executemany(_UPSERT[table], rows[table])
    conn.commit()

    return {table: len(rows[table]) for table in _ORDER}


def run_once() -> None:
    import psycopg  # psycopg 3
    ts = datetime.now(timezone.utc).isoformat()
    print(f"[{ts}] governance ingest cycle start — {DSN}", flush=True)
    with psycopg.connect(DSN) as conn:
        counts = ingest_cycle(conn)
    print(f"[{ts}] governance ingest cycle done — {counts}", flush=True)


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Upsert ARGUS governance data (threats/policies/decisions/assets) into Postgres for Ontop.")
    ap.add_argument("--once", action="store_true", help="Run a single cycle and exit.")
    args = ap.parse_args()

    if args.once:
        run_once()
        return

    print(f"Governance ingest loop starting — every {INTERVAL}s.", flush=True)
    while True:
        try:
            run_once()
        except Exception as e:
            print(f"  governance ingest cycle raised: {type(e).__name__}: {e}", flush=True)
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
