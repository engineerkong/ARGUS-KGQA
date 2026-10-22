"""
Anonymise a COPY of the experiment snapshot for the public Hugging Face Space.

PRIVATE tool (deploy-tools/ is never pushed). It works on the database given
by --dsn, which must be a separate copy restored from the original dump — it
refuses to touch a database named argus_snapshot or argus — and writes a new
dump; the original dump and the experiment snapshot are left as they are.

    python anonymize_db.py --dsn postgresql://argus@localhost:55432/argus_anon \
        --out ../hf-spaces/data/snapshot.dump

What it does, in one transaction, verified before commit:
  1. the same clean-up as the experiment snapshot: drop the 1,316 observations
     (188 readings) with an epoch timestamp, empty ingest_state;
  2. site ids and labels -> site_a … site_e / test_site_1, test_site_2;
  3. every free-text field (node, sensor, policy, threat, decision, asset
     texts) through the ordered replacements in site_aliases.json;
  4. assets: anonymous label, no country, URL, pilot number or code;
  5. coordinates: each site moved as a whole to a fictitious centroid, keeping
     every node's offset in metres from the site centroid, so distances within a
     site are preserved; the GNSS lat/lon readings are moved the same way;
  6. checks: no forbidden word left in any text column, row counts as the
     snapshot, within-site distances unchanged (max error printed).
"""

import argparse
import json
import math
import re
import subprocess
from pathlib import Path

import psycopg

HERE = Path(__file__).resolve().parent
EARTH_R = 6371000.0


def haversine(a, b):
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp, dl = p2 - p1, math.radians(b[1] - a[1])
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * EARTH_R * math.asin(math.sqrt(h))


def text_rules(cfg):
    rules = [(re.compile(p, re.I), r) for p, r in cfg["text"]]
    for real, s in cfg["sites"].items():
        rules.append((re.compile(re.escape(real), re.I), s["id"]))
    return rules


def anon_text(s, rules):
    if s is None:
        return None
    for pat, rep in rules:
        s = pat.sub(rep, s)
    return re.sub(r"\s{2,}", " ", s).strip()


TEXT_COLUMNS = {   # table: (key column, [text columns])
    "nodes": ("node_id", ["label", "name"]),
    "sensors": ("sensor_id", ["label"]),
    "policies": ("policy_id", ["label", "description", "threat_name"]),
    "threats": ("threat_id", ["label", "description", "threat_level"]),
    "decisions": ("decision_id", ["label", "description", "urgency"]),
    "assets": ("asset_id", ["label", "description"]),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dsn", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--pg-bin", default=str(Path.home() / "miniconda3/envs/pgtools/bin"))
    args = ap.parse_args()

    dbname = args.dsn.rstrip("/").rsplit("/", 1)[-1]
    if dbname in ("argus_snapshot", "argus"):
        raise SystemExit(f"refusing to modify {dbname!r}: run this on a separate copy restored from the dump")

    cfg = json.loads((HERE / "site_aliases.json").read_text())
    rules = text_rules(cfg)
    sites = cfg["sites"]
    con = psycopg.connect(args.dsn)
    cur = con.cursor()

    # 1. clean-up identical to the experiment snapshot
    cur.execute("DELETE FROM observations WHERE result_time < '2000-01-01'")
    print("epoch observations removed:", cur.rowcount)
    cur.execute("DELETE FROM readings WHERE result_time < '2000-01-01'")
    print("epoch readings removed:", cur.rowcount)
    cur.execute("DELETE FROM ingest_state")

    # centroids (before anything moves) and within-site distances, for the check
    cur.execute("""SELECT DISTINCT r.site_id, n.node_id, n.latitude, n.longitude FROM nodes n
                   JOIN readings r USING (node_id) WHERE n.latitude IS NOT NULL""")
    by_site = {}
    for s, nid, lat, lon in cur.fetchall():
        by_site.setdefault(s, []).append((nid, float(lat), float(lon)))
    multi = {}
    for s, ns in by_site.items():
        for nid, _, _ in ns:
            multi.setdefault(nid, set()).add(s)
    shared = {n for n, ss in multi.items() if len(ss) > 1}
    assert not shared, f"nodes at several sites: {shared}"
    before = {s: {(a[0], b[0]): haversine(a[1:], b[1:]) for i, a in enumerate(ns) for b in ns[i + 1:]}
              for s, ns in by_site.items()}

    # 2. site ids and labels (the FK from readings is dropped for the rename)
    cur.execute("SELECT conname FROM pg_constraint WHERE conrelid = 'readings'::regclass AND contype = 'f' "
                "AND pg_get_constraintdef(oid) LIKE '%sites%'")
    fks = [r[0] for r in cur.fetchall()]
    for fk in fks:
        cur.execute(f"ALTER TABLE readings DROP CONSTRAINT {fk}")
    for real, s in sites.items():
        for table, col in (("sites", "site_id"), ("readings", "site_id"), ("policies", "site_id"), ("assets", "site_id")):
            cur.execute(f"UPDATE {table} SET {col} = %s WHERE {col} = %s", (s["id"], real))
        cur.execute("UPDATE sites SET label = %s WHERE site_id = %s", (s["id"], s["id"]))
    for fk in fks:
        cur.execute(f"ALTER TABLE readings ADD CONSTRAINT {fk} FOREIGN KEY (site_id) REFERENCES sites")

    # 3. free text
    for table, (key, cols) in TEXT_COLUMNS.items():
        cur.execute(f"SELECT {key}, {', '.join(cols)} FROM {table}")
        rows = cur.fetchall()
        n = 0
        for row in rows:
            new = [anon_text(v, rules) for v in row[1:]]
            if new != list(row[1:]):
                cur.execute(f"UPDATE {table} SET {', '.join(c + ' = %s' for c in cols)} WHERE {key} = %s",
                            (*new, row[0]))
                n += 1
        print(f"{table}: {n}/{len(rows)} rows rewritten")

    # 4. assets
    for real, s in sites.items():
        if "asset" in s:
            cur.execute("UPDATE assets SET label = %s, asset_code = %s, country = NULL, source_url = NULL, "
                        "pilot_number = NULL WHERE site_id = %s", (s["asset"], s["id"], s["id"]))

    # 5. coordinates: move each site to its fictitious centroid, keeping metre offsets
    transforms = {}
    for real, s in sites.items():
        ns = by_site.get(s["id"]) or by_site.get(real)
        if not ns or "centroid" not in s:
            continue
        lat0 = sum(x[1] for x in ns) / len(ns)
        lon0 = sum(x[2] for x in ns) / len(ns)
        lat1, lon1 = s["centroid"]
        k = math.cos(math.radians(lat0)) / math.cos(math.radians(lat1))
        transforms[s["id"]] = (lat0, lon0, lat1, lon1, k)
        ids = [x[0] for x in ns]
        cur.execute("""UPDATE nodes SET latitude = %s + (latitude - %s), longitude = %s + (longitude - %s) * %s
                       WHERE node_id = ANY(%s)""", (lat1, lat0, lon1, lon0, k, ids))
        cur.execute("""UPDATE observations o SET value = %s + (o.value - %s) FROM readings r
                       WHERE r.reading_id = o.reading_id AND r.site_id = %s AND o.property_id = 'lat'
                         AND o.value IS NOT NULL""", (lat1, lat0, s["id"]))
        cur.execute("""UPDATE observations o SET value = %s + (o.value - %s) * %s FROM readings r
                       WHERE r.reading_id = o.reading_id AND r.site_id = %s AND o.property_id = 'lon'
                         AND o.value IS NOT NULL""", (lon1, lon0, k, s["id"]))
    # nodes with coordinates but no readings in the snapshot: drop the coordinates
    cur.execute("""UPDATE nodes SET latitude = NULL, longitude = NULL WHERE latitude IS NOT NULL
                   AND node_id NOT IN (SELECT DISTINCT node_id FROM readings)""")
    print("coordinates cleared on nodes without readings:", cur.rowcount)

    # 6. checks
    cur.execute("""SELECT DISTINCT r.site_id, n.node_id, n.latitude, n.longitude FROM nodes n
                   JOIN readings r USING (node_id) WHERE n.latitude IS NOT NULL""")
    after_pts = {}
    for s, nid, lat, lon in cur.fetchall():
        after_pts.setdefault(s, {})[nid] = (float(lat), float(lon))
    worst = 0.0
    for real, s in sites.items():
        for (a, b), d in before.get(real, {}).items():
            d2 = haversine(after_pts[s["id"]][a], after_pts[s["id"]][b])
            worst = max(worst, abs(d2 - d) / max(d, 1.0))
    print(f"within-site distances: max relative change {worst:.2e}")
    assert worst < 1e-3, "within-site distances changed"

    forbidden = re.compile("|".join(re.escape(w) for w in cfg["forbidden"]), re.I)
    cur.execute("""SELECT table_name, column_name FROM information_schema.columns
                   WHERE table_schema = 'public' AND data_type IN ('text', 'character varying')""")
    leaks = []
    for table, col in cur.fetchall():
        cur.execute(f"SELECT DISTINCT {col} FROM {table} WHERE {col} ~* %s LIMIT 5", (forbidden.pattern,))
        leaks += [(table, col, v[0]) for v in cur.fetchall()]
    if leaks:
        for l in leaks:
            print("LEAK:", l)
        con.rollback()
        raise SystemExit("forbidden words left — rolled back")
    cur.execute("SELECT (SELECT count(*) FROM observations), (SELECT count(*) FROM readings), "
                "(SELECT count(*) FROM sites), (SELECT count(*) FROM policies)")
    print("observations, readings, sites, policies:", cur.fetchone())
    con.commit()
    con.close()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    host, port = re.search(r"@([^:/]+):(\d+)/", args.dsn).groups()
    subprocess.run([f"{args.pg_bin}/pg_dump", "-h", host, "-p", port, "-U", "argus", "-d", dbname,
                    "-Fc", "--no-owner", "--no-privileges", "-f", str(out)], check=True)
    print(f"dump written: {out} ({out.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
