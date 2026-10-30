"""
Snapshot v2: add the LoRaWAN measurements to the frozen snapshot (argus_snapshot), with the ingestion's
own row building (0b_online_ingest.build_rows), so the snapshot holds what the fixed ingestion stores.

    python scripts/snapshot_add_lorawan.py          (back up first: pg_dump -Fc argus_snapshot)

Source: material/lorawan_readings.jsonl.gz, the partner's export of the readings table for site
"lorawan", 2026-05-13 … 2026-08-12 (lorawan_readings.summary.json). What changes, in one transaction:
  - only the snapshot's window: LoRaWAN readings up to the snapshot's last observation (data_end,
    2026-08-12 09:15 UTC) are kept; the value-less LoRaWAN readings after it are removed, so no site's
    latest reading moves and every relative window keeps its end;
  - LoRaWAN readings get their observations (payload key/value; radio metadata lora_* excluded; units from
    material/lorawan_channels.csv); readings the snapshot missed inside the window are added (ids as the
    ingestion computes them, from the record with the API's timestamp format);
  - LoRaWAN and Eurecat readings move from their channel ("lorawan", "eurecat") to the pilot site of
    their device (material/site_lookup.csv); the two channel pseudo-sites are removed;
  - node coordinates come from the device registry (material/ARGUS_nodes.csv, built from material/lut.xlsx
    by build_lookups.py): new for the LoRaWAN and Eurecat nodes, corrected for Schenkenberg; nodes without
    a name get the LUT's device type (e.g. "Weather station").
"""
from __future__ import annotations

import csv
import gzip
import importlib
import json
import os
from datetime import datetime
from pathlib import Path

import pandas as pd
import psycopg

MATERIAL = Path(__file__).resolve().parent.parent / "material"
DSN = os.environ.get("ARGUS_SNAPSHOT_DSN", "postgresql://argus:argus@localhost:5432/argus_snapshot")
_rd = importlib.import_module("0a_offline_readings")
_ing = importlib.import_module("0b_online_ingest")


def api_ts(ts: str) -> str:
    """'2026-06-17 10:58:43.6407+00' (Postgres text) → '2026-06-17T10:58:43.640700Z' (the API's form,
    which the reading id hashes)."""
    day, clock = ts.replace("+00", "").split(" ")
    sec, _, frac = clock.partition(".")
    return f"{day}T{sec}.{(frac or '0').ljust(6, '0')[:6]}Z"


def lut_device_types() -> dict[str, str]:
    """node id → device type, for node ids the LUT gives one type (not a generic id such as Baltanas's
    "sensor", shared by eight Shelly humidity and temperature devices)."""
    lut = pd.read_excel(MATERIAL / "lut.xlsx", header=None).iloc[2:]
    types: dict[str, set[str]] = {}
    for _, r in lut.iterrows():
        if not pd.isna(r[3]) and not pd.isna(r[1]):
            types.setdefault(str(r[3]).strip(), set()).add(str(r[1]).strip())
    return {node: t.pop() for node, t in types.items() if len(t) == 1}


def main() -> None:
    # autocommit, so that `with con.transaction()` below is the transaction itself (without it, the first
    # SELECT opens an implicit transaction, con.transaction() becomes a savepoint inside it, and closing the
    # connection rolls everything back)
    con = psycopg.connect(DSN, autocommit=True)
    con.execute("SET TIME ZONE 'UTC'")
    # the snapshot database is frozen (default_transaction_read_only=on, statement_timeout=120s as database
    # settings); lifted for this session only, so every other connection still sees a read-only snapshot
    con.execute("SET default_transaction_read_only = off")
    con.execute("SET statement_timeout = 0")
    (data_end,) = con.execute("SELECT max(result_time) FROM observations").fetchone()
    records = []
    for line in gzip.open(MATERIAL / "lorawan_readings.jsonl.gz", "rt"):
        r = json.loads(line)
        r["ts"] = api_ts(r["ts"])
        if datetime.fromisoformat(r["ts"].replace("Z", "+00:00")) <= data_end:
            records.append(r)
    rows = _ing.build_rows(records)
    lookup = {r["device"]: r["site"] for r in csv.DictReader(open(MATERIAL / "site_lookup.csv"))}
    coords = {r["nodeid"]: r for r in csv.DictReader(open(MATERIAL / "ARGUS_nodes.csv"))}
    types = lut_device_types()
    stats = {}
    with con.transaction():
        cur = con.cursor()
        cur.execute("DELETE FROM readings WHERE site_id = 'lorawan' AND result_time > %s "
                    "AND NOT EXISTS (SELECT 1 FROM observations o WHERE o.reading_id = readings.reading_id)", (data_end,))
        stats["lorawan readings after data_end removed"] = cur.rowcount
        for table in ("sites", "nodes", "sensors", "observed_properties"):
            cur.executemany(_ing._INSERT[table], rows[table])
        # bulk: COPY into staging tables, then set-based inserts (row-by-row inserts of ~1.6M observations
        # inside one transaction ran for an hour and lost the connection)
        cur.execute("CREATE TEMP TABLE stage_readings (LIKE readings) ON COMMIT DROP")
        cur.execute("CREATE TEMP TABLE stage_obs (LIKE observations) ON COMMIT DROP")
        with cur.copy("COPY stage_readings FROM STDIN") as cp:
            for row in rows["readings"]:
                cp.write_row(row)
        with cur.copy("COPY stage_obs FROM STDIN") as cp:
            for row in rows["observations"]:
                cp.write_row(row)
        cur.execute("""INSERT INTO readings SELECT * FROM stage_readings
                       ON CONFLICT (reading_id) DO UPDATE SET site_id = EXCLUDED.site_id""")
        stats["lorawan readings in the window (added or moved)"] = cur.rowcount
        cur.execute("INSERT INTO observations SELECT DISTINCT ON (observation_id) * FROM stage_obs "
                    "ON CONFLICT (observation_id) DO NOTHING")
        stats["observations added"] = cur.rowcount
        cur.execute("CREATE TEMP TABLE stage_site (device TEXT PRIMARY KEY, site TEXT) ON COMMIT DROP")
        cur.executemany("INSERT INTO stage_site VALUES (%s, %s)", list(lookup.items()))
        cur.execute("""UPDATE readings r SET site_id = COALESCE(s1.site, s2.site)
                       FROM readings x LEFT JOIN stage_site s1 ON s1.device = x.sensor_id
                       LEFT JOIN stage_site s2 ON s2.device = x.node_id
                       WHERE r.reading_id = x.reading_id AND x.site_id = 'eurecat'
                         AND COALESCE(s1.site, s2.site) IS NOT NULL""")
        stats["eurecat readings moved to their site"] = cur.rowcount
        cur.execute("DELETE FROM sites s WHERE site_id IN ('lorawan', 'eurecat') "
                    "AND NOT EXISTS (SELECT 1 FROM readings r WHERE r.site_id = s.site_id)")
        stats["channel pseudo-sites removed"] = cur.rowcount
        n_coord = n_name = 0
        for node_id, name in cur.execute("SELECT node_id, name FROM nodes").fetchall():
            c = coords.get(node_id)
            if c:
                cur.execute("UPDATE nodes SET latitude = %s, longitude = %s, altitude = %s WHERE node_id = %s",
                            (float(c["latitude"]), float(c["longitude"]),
                             float(c["altitude"]) if c["altitude"] else None, node_id))
                n_coord += 1
            if name is None and node_id in types:
                cur.execute("UPDATE nodes SET name = %s WHERE node_id = %s", (types[node_id], node_id))
                n_name += 1
        stats["nodes with coordinates from the LUT"] = n_coord
        stats["nodes named with their LUT device type"] = n_name
        left = cur.execute("SELECT count(*) FROM readings WHERE site_id IN ('lorawan', 'eurecat')").fetchone()[0]
        assert left == 0, f"{left} readings still under a channel pseudo-site"
    for k, v in stats.items():
        print(f"{k:45s} {v:>9,}")
    for q, label in [("SELECT count(*) FROM readings", "readings"), ("SELECT count(*) FROM observations", "observations"),
                     ("SELECT max(result_time) FROM observations", "data end"),
                     ("SELECT string_agg(site_id || ' ' || n, ', ' ORDER BY site_id) FROM "
                      "(SELECT site_id, count(*) n FROM readings GROUP BY 1) x", "readings per site")]:
        print(f"{label:45s} {con.execute(q).fetchone()[0]}")


if __name__ == "__main__":
    main()
