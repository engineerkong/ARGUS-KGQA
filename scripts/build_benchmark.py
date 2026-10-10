"""
Build the 500-question evaluation set (100 each: basic, spatial, temporal,
anomaly, follow-up) over the frozen experiment snapshot.

Every reference answer is computed here, directly from the snapshot database
with SQL and plain Python — independently of HeriKGQA, Interactive-KBQA and
TextRAG — and still needs manual validation before use.

    python scripts/build_benchmark.py            # writes material/benchmark_500.{json,csv,meta.json}

Conventions (also written to benchmark_500.meta.json):
  - all times UTC; "on <date>" = that UTC calendar day;
  - relative times ("last 24 hours") end at the snapshot's last reading;
  - distances are haversine on a 6,371,000 m sphere; a centroid is the mean
    latitude/longitude of the nodes; only nodes with coordinates count;
  - AD-RT verdicts follow each rule's definition: windows end at the latest
    matching reading at or before the end of the named day (or the snapshot
    end), every (sensor, quantity) series is evaluated separately and a rule
    fires if any series crosses its threshold; a question's verdict is Yes if
    any applicable rule fires, No if at least one was evaluated and none fired,
    Cannot be determined if none could be evaluated.
"""

from __future__ import annotations

import bisect
import csv
import itertools
import json
import math
import os
import random
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import psycopg

DSN = os.environ.get("ARGUS_SNAPSHOT_DSN", "postgresql://argus:argus@localhost:5432/argus_snapshot")
OUT = Path(__file__).resolve().parent.parent / "material"
SEED = 20260813
PER_TYPE = 100

SITES = ["baltanas", "delos", "lucretili", "ranverso", "schenkenberg"]
SITE = {s: s.capitalize() for s in SITES}
QNAME = {
    "temperature": "temperature", "rainfall": "rainfall", "soil_temperature": "soil temperature",
    "soil_water_potential": "soil water potential", "voltage": "voltage", "thermistor": "thermistor reading",
    "pgaComposed": "composed peak ground acceleration (pgaComposed)",
    "rmsComposed": "composed RMS acceleration (rmsComposed)",
    "potentiometer_displacement": "potentiometer displacement",
}
# quantities asked about, per site (must have data there)
SITE_QUANTITIES = {
    "baltanas": ["temperature", "soil_temperature", "soil_water_potential", "voltage"],
    "delos": ["temperature", "voltage", "potentiometer_displacement"],
    "lucretili": ["temperature", "voltage"],
    "ranverso": ["temperature", "rainfall", "voltage"],
    "schenkenberg": ["temperature", "pgaComposed", "rmsComposed"],
}
DAILY_QUANTITIES = ["temperature", "soil_temperature", "soil_water_potential", "rainfall"]
MONTHS = [(2026, 5, "May"), (2026, 6, "June"), (2026, 7, "July"), (2026, 8, "August")]
EARTH_R = 6371000.0

# Questions too close to an in-context example of a system under test
# (HeriKGQA parser few-shots, Interactive-KBQA dialog demos).
EXCLUDED = {
    ("avg", "lucretili", "temperature"),          # Interactive-KBQA demo
    ("quantity_count", "delos"),                  # HeriKGQA few-shot (quantities at delos)
    ("threshold", "baltanas", "R6_rain_1h"),      # Interactive-KBQA demo
    ("threshold", "delos", "R1a_rain_1h"),        # HeriKGQA few-shot (rainfall threshold at delos)
    ("threshold", "delos", "R1b_rain_3h"),
}


# ── helpers ────────────────────────────────────────────────────────────────

UNIT = {"Cel": "°C", "mg_acc": "mg"}


def unit(u):
    return UNIT.get(u, u) if u else ""


def plural(n, word):
    return f"{n} {word}" + ("" if n == 1 else "s")


def fnum(x: float, nd: int = 3) -> str:
    s = f"{x:.{nd}f}".rstrip("0").rstrip(".")
    return s if s not in ("-0", "") else "0"


def ftime(t: datetime) -> str:
    return t.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def haversine(a, b) -> float:
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp, dl = p2 - p1, math.radians(b[1] - a[1])
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * EARTH_R * math.asin(math.sqrt(h))


class Bench:
    def __init__(self, con):
        self.con = con
        self.items: dict[str, list[dict]] = defaultdict(list)

    def q(self, sql, *args):
        return self.con.execute(sql, args).fetchall()

    def add(self, qtype, template, question, reference, value, answerable=True, **extra):
        if isinstance(value, float):
            value = round(value, 6)  # Postgres' parallel AVG varies in the last digits between runs
        self.items[qtype].append({
            "type": qtype, "template": template, "question": question,
            "reference": reference, "reference_value": value, "answerable": answerable, **extra,
        })


# ── data pulled once ───────────────────────────────────────────────────────

def load(b: Bench):
    d = {}
    d["stats"] = {(s, p): dict(avg=a, mn=mn, mx=mx, n=n, sensors=ns, unit=u)
                  for s, p, a, mn, mx, n, ns, u in b.q("""
        SELECT r.site_id, o.property_id, avg(o.value), min(o.value), max(o.value), count(*),
               count(DISTINCT r.sensor_id), max(o.unit)
        FROM observations o JOIN readings r USING (reading_id)
        WHERE o.value IS NOT NULL GROUP BY 1, 2""")}
    d["span"] = {s: (a, z, n) for s, a, z, n in b.q(
        "SELECT site_id, min(result_time), max(result_time), count(*) FROM readings GROUP BY 1")}
    d["latest_q"] = {(s, p): t for s, p, t in b.q("""
        SELECT r.site_id, o.property_id, max(o.result_time) FROM observations o JOIN readings r USING (reading_id)
        WHERE o.value IS NOT NULL GROUP BY 1, 2""")}
    d["argmax"] = {(s, p): (v, t) for s, p, v, t in b.q("""
        SELECT DISTINCT ON (r.site_id, o.property_id) r.site_id, o.property_id, o.value, o.result_time
        FROM observations o JOIN readings r USING (reading_id) WHERE o.value IS NOT NULL
        ORDER BY r.site_id, o.property_id, o.value DESC, o.result_time ASC""")}
    d["daily"] = {(s, p, day): dict(avg=a, mn=mn, mx=mx, n=n) for s, p, day, a, mn, mx, n in b.q("""
        SELECT r.site_id, o.property_id, (o.result_time AT TIME ZONE 'UTC')::date, avg(o.value), min(o.value),
               max(o.value), count(*)
        FROM observations o JOIN readings r USING (reading_id)
        WHERE o.value IS NOT NULL AND o.property_id = ANY(%s) GROUP BY 1, 2, 3""", DAILY_QUANTITIES)}
    d["monthly"] = {(s, y, m): n for s, y, m, n in b.q("""
        SELECT site_id, extract(year FROM result_time AT TIME ZONE 'UTC')::int,
               extract(month FROM result_time AT TIME ZONE 'UTC')::int, count(*) FROM readings GROUP BY 1, 2, 3""")}
    d["nodes_n"] = dict(b.q("SELECT site_id, count(DISTINCT node_id) FROM readings GROUP BY 1"))
    d["sensors_n"] = dict(b.q("SELECT site_id, count(DISTINCT sensor_id) FROM readings GROUP BY 1"))
    d["props_n"] = dict(b.q("""SELECT r.site_id, count(DISTINCT o.property_id) FROM observations o
                               JOIN readings r USING (reading_id) GROUP BY 1"""))
    d["sensors_q"] = {(s, p): n for s, p, n in b.q("""
        SELECT r.site_id, o.property_id, count(DISTINCT r.sensor_id) FROM observations o
        JOIN readings r USING (reading_id) GROUP BY 1, 2""")}
    d["end"] = b.q("SELECT max(result_time) FROM observations")[0][0]
    nodes = defaultdict(list)
    for s, label, lat, lon, alt in b.q("""
        SELECT DISTINCT r.site_id, n.label, n.latitude, n.longitude, n.altitude FROM nodes n
        JOIN readings r USING (node_id) WHERE n.latitude IS NOT NULL"""):
        nodes[s].append((label, float(lat), float(lon), None if alt is None else float(alt)))
    d["nodes"] = nodes
    d["window_avg"] = {}
    for s in SITES:
        for hours in (24, 24 * 7):
            (a, n), = b.q("""SELECT avg(o.value), count(*) FROM observations o JOIN readings r USING (reading_id)
                             WHERE r.site_id = %s AND o.property_id = 'temperature' AND o.value IS NOT NULL
                               AND o.result_time > %s AND o.result_time <= %s""",
                          s, d["end"] - timedelta(hours=hours), d["end"])
            d["window_avg"][(s, hours)] = (a, n)
    return d


# ── basic ──────────────────────────────────────────────────────────────────

def gen_basic(b: Bench, d):
    for s in SITES:
        b.add("basic", "node_count", f"How many sensor nodes are installed at {SITE[s]}?",
              plural(d['nodes_n'][s], "sensor node") + ".", d["nodes_n"][s])
        b.add("basic", "sensor_count", f"How many sensors have reported readings at {SITE[s]}?",
              plural(d['sensors_n'][s], "sensor") + ".", d["sensors_n"][s])
        b.add("basic", "reading_count", f"How many readings are stored for {SITE[s]}?",
              f"{d['span'][s][2]} readings.", d["span"][s][2])
        if ("quantity_count", s) not in EXCLUDED:
            b.add("basic", "quantity_count", f"How many different physical quantities are measured at {SITE[s]}?",
                  f"{d['props_n'][s]} quantities.", d["props_n"][s])
        for p in SITE_QUANTITIES[s]:
            st = d["stats"][(s, p)]
            for agg, word, key in (("avg", "average", "avg"), ("max", "maximum", "mx"), ("min", "minimum", "mn")):
                if (agg, s, p) in EXCLUDED:
                    continue
                verb = random.choice(["recorded", "measured", "observed"])
                b.add("basic", f"{agg}_quantity", f"What is the {word} {QNAME[p]} {verb} at {SITE[s]}?",
                      f"{fnum(float(st[key]))}" + (f" {unit(st['unit'])}" if st["unit"] else "") + ".", float(st[key]),
                      unit=unit(st["unit"]))
            b.add("basic", "obs_count", f"How many {QNAME[p]} observations exist for {SITE[s]}?",
                  f"{st['n']} observations.", st["n"])
            b.add("basic", "sensors_measuring", f"How many sensors measure {QNAME[p]} at {SITE[s]}?",
                  plural(d['sensors_q'][(s, p)], "sensor") + ".", d["sensors_q"][(s, p)])
    avgs = {s: float(d["stats"][(s, "temperature")]["avg"]) for s in SITES}
    hi, lo = max(avgs, key=avgs.get), min(avgs, key=avgs.get)
    b.add("basic", "site_compare", "Among Baltanas, Delos, Lucretili, Ranverso and Schenkenberg, which site has the highest average temperature?",
          f"{SITE[hi]} ({fnum(avgs[hi])}).", SITE[hi])
    b.add("basic", "site_compare", "Among Baltanas, Delos, Lucretili, Ranverso and Schenkenberg, which site has the lowest average temperature?",
          f"{SITE[lo]} ({fnum(avgs[lo])}).", SITE[lo])
    most_nodes = max(SITES, key=lambda s: d["nodes_n"][s])
    b.add("basic", "site_compare", "Among Baltanas, Delos, Lucretili, Ranverso and Schenkenberg, which site has the most sensor nodes?",
          f"{SITE[most_nodes]} ({d['nodes_n'][most_nodes]} nodes).", SITE[most_nodes])
    most_r = max(SITES, key=lambda s: d["span"][s][2])
    b.add("basic", "site_compare", "Among Baltanas, Delos, Lucretili, Ranverso and Schenkenberg, which site has the most readings?",
          f"{SITE[most_r]} ({d['span'][most_r][2]} readings).", SITE[most_r])
    for s, what in [("baltanas", "relative humidity"), ("delos", "wind speed"), ("lucretili", "CO2 concentration"),
                    ("ranverso", "barometric pressure"), ("schenkenberg", "relative humidity"), ("delos", "solar radiation")]:
        b.add("basic", "unanswerable", f"What is the average {what} at {SITE[s]}?",
              f"Cannot be answered: the knowledge graph has no {what} data for {SITE[s]}.", None, answerable=False)


# ── spatial ────────────────────────────────────────────────────────────────

def gen_spatial(b: Bench, d):
    rng = random.Random(SEED + 1)
    for s in SITES:
        ns = d["nodes"][s]
        labels = [n[0] for n in ns]
        unique = {l for l in labels if labels.count(l) == 1}
        pairs = [(haversine(a[1:3], c[1:3]), a[0], c[0]) for a, c in itertools.combinations(ns, 2)]
        far = max(pairs)
        b.add("spatial", "farthest_pair", f"How far apart are the two most distant sensor nodes at {SITE[s]}?",
              f"{fnum(far[0], 1)} m, between {far[1]} and {far[2]}.", round(far[0], 1), unit="m")
        clat, clon = sum(n[1] for n in ns) / len(ns), sum(n[2] for n in ns) / len(ns)
        b.add("spatial", "centroid", f"What is the centroid of the sensor nodes at {SITE[s]}?",
              f"Latitude {clat:.6f}, longitude {clon:.6f} (mean of {len(ns)} nodes).", [round(clat, 6), round(clon, 6)])
        with_alt = [n for n in ns if n[3] is not None]
        top, bot = max(with_alt, key=lambda n: n[3]), min(with_alt, key=lambda n: n[3])
        if [n[3] for n in with_alt].count(top[3]) == 1:
            b.add("spatial", "highest_node", f"Which sensor node at {SITE[s]} is at the highest altitude?",
                  f"{top[0]}, at {fnum(top[3], 2)} m.", top[0])
        if [n[3] for n in with_alt].count(bot[3]) == 1:
            b.add("spatial", "lowest_node", f"Which sensor node at {SITE[s]} is at the lowest altitude?",
                  f"{bot[0]}, at {fnum(bot[3], 2)} m.", bot[0])
        b.add("spatial", "altitude_range", f"What is the altitude range of the sensor nodes at {SITE[s]}?",
              f"{fnum(top[3] - bot[3], 2)} m (from {fnum(bot[3], 2)} m to {fnum(top[3], 2)} m).",
              round(top[3] - bot[3], 2), unit="m")
        north, south = max(ns, key=lambda n: n[1]), min(ns, key=lambda n: n[1])
        if [n[1] for n in ns].count(north[1]) == 1:
            b.add("spatial", "northernmost", f"Which sensor node at {SITE[s]} is the northernmost?",
                  f"{north[0]} (latitude {north[1]:.6f}).", north[0])
        if [n[1] for n in ns].count(south[1]) == 1:
            b.add("spatial", "southernmost", f"Which sensor node at {SITE[s]} is the southernmost?",
                  f"{south[0]} (latitude {south[1]:.6f}).", south[0])
        named = [n for n in ns if n[0] in unique]
        for a, c in rng.sample(list(itertools.combinations(named, 2)), min(8, len(named) * (len(named) - 1) // 2)):
            dist = haversine(a[1:3], c[1:3])
            b.add("spatial", "pair_distance", f"What is the distance between sensor nodes {a[0]} and {c[0]} at {SITE[s]}?",
                  f"{fnum(dist, 1)} m.", round(dist, 1), unit="m")
        for a in rng.sample(named, min(5, len(named))):
            others = sorted((haversine(a[1:3], c[1:3]), c[0]) for c in ns if c is not a)
            if len(others) > 1 and others[0][0] < others[1][0] - 0.05 and others[0][1] in unique:
                b.add("spatial", "nearest_node", f"Which sensor node is closest to {a[0]} at {SITE[s]}?",
                      f"{others[0][1]}, {fnum(others[0][0], 1)} m away.", others[0][1])
            radius = rng.choice([10, 50, 100, 500])
            within = sum(1 for dd, _ in others if dd <= radius)
            b.add("spatial", "within_radius", f"How many other sensor nodes at {SITE[s]} are within {radius} m of {a[0]}?",
                  f"{within}.", within)
    cents = {s: (sum(n[1] for n in d["nodes"][s]) / len(d["nodes"][s]), sum(n[2] for n in d["nodes"][s]) / len(d["nodes"][s]))
             for s in SITES}
    for a, c in itertools.combinations(SITES, 2):
        dist = haversine(cents[a], cents[c]) / 1000
        b.add("spatial", "site_distance",
              f"How far apart are {SITE[a]} and {SITE[c]}, measured between the centroids of their sensor nodes?",
              f"{fnum(dist, 1)} km.", round(dist, 1), unit="km")
    for qtext in ["How far are the Baltanas sensor nodes from the nearest river?",
                  "Which sensor node at Delos is closest to the harbour?",
                  "What is the height of the Schenkenberg castle tower?"]:
        b.add("spatial", "unanswerable", qtext, "Cannot be answered from the knowledge graph.", None, answerable=False)


# ── temporal ───────────────────────────────────────────────────────────────

def gen_temporal(b: Bench, d):
    rng = random.Random(SEED + 2)
    end = d["end"]
    for s in SITES:
        a, z, _ = d["span"][s]
        b.add("temporal", "first_reading", f"When was the first reading recorded at {SITE[s]}?", f"{ftime(a)}.", ftime(a))
        b.add("temporal", "last_reading", f"When was the most recent reading recorded at {SITE[s]}?", f"{ftime(z)}.", ftime(z))
        b.add("temporal", "span", f"What time period do the readings at {SITE[s]} cover?",
              f"From {ftime(a)} to {ftime(z)}.", [ftime(a), ftime(z)])
        for p in SITE_QUANTITIES[s]:
            t = d["latest_q"][(s, p)]
            b.add("temporal", "latest_quantity", f"When was the most recent {QNAME[p]} reading at {SITE[s]}?",
                  f"{ftime(t)}.", ftime(t))
            v, t = d["argmax"][(s, p)]
            b.add("temporal", "time_of_max", f"When was the highest {QNAME[p]} at {SITE[s]} recorded?",
                  f"{ftime(t)} (value {fnum(float(v))}).", ftime(t))
        for y, m, mname in MONTHS:
            n = d["monthly"].get((s, y, m), 0)
            b.add("temporal", "monthly_count", f"How many readings were recorded at {SITE[s]} in {mname} {y}?",
                  f"{n} readings.", n)
        for hours, phrase in ((24, "the last 24 hours"), (168, "the last 7 days")):
            avg, n = d["window_avg"][(s, hours)]
            if n:
                b.add("temporal", "relative_window", f"What was the average temperature at {SITE[s]} over {phrase}?",
                      f"{fnum(float(avg))} ({n} observations, window ending {ftime(end)}).", float(avg))
    days = sorted({k[2] for k in d["daily"]})
    for (s, p, day), st in rng.sample(sorted(d["daily"].items()), 120):
        if st["n"] < 10:
            continue
        agg, word, key = rng.choice([("avg", "average", "avg"), ("max", "maximum", "mx"), ("min", "minimum", "mn")])
        b.add("temporal", f"daily_{agg}", f"What was the {word} {QNAME[p]} at {SITE[s]} on {day.isoformat()}?",
              f"{fnum(float(st[key]))}.", float(st[key]))
    for s in SITES:
        for y, m, mname in MONTHS[1:3]:
            ds = {k[2]: v["avg"] for k, v in d["daily"].items()
                  if k[0] == s and k[1] == "temperature" and k[2].month == m and v["n"] >= 10}
            if ds:
                best = max(ds, key=ds.get)
                b.add("temporal", "hottest_day", f"Which day in {mname} {y} had the highest average temperature at {SITE[s]}?",
                      f"{best.isoformat()} (daily average {fnum(float(ds[best]))}).", best.isoformat())
    for s in SITES:
        for _ in range(3):
            start = date(2026, 5, 15) + timedelta(days=rng.randrange(0, 80))
            stop = start + timedelta(days=6)
            rows = [v for k, v in d["daily"].items() if k[0] == s and k[1] == "temperature" and start <= k[2] <= stop]
            n = sum(v["n"] for v in rows)
            if n:
                avg = sum(float(v["avg"]) * v["n"] for v in rows) / n
                b.add("temporal", "range_avg",
                      f"What was the average temperature at {SITE[s]} between {start.isoformat()} and {stop.isoformat()}?",
                      f"{fnum(avg)} ({n} observations, both days inclusive).", avg)
    for qtext, ref in [("What was the temperature at Delos in April 2026?", "Cannot be answered: the data starts on 2026-05-13."),
                       ("What was the relative humidity at Baltanas on 2026-07-01?", "Cannot be answered: no humidity data."),
                       ("How many readings were recorded at Ranverso in September 2026?", "Cannot be answered: the data ends on 2026-08-12.")]:
        b.add("temporal", "unanswerable", qtext, ref, None, answerable=False)


# ── anomaly ────────────────────────────────────────────────────────────────

def _matches(label, any_of=(), all_of=(), excludes=()):
    l = label.lower()
    return ((not any_of or any(x in l for x in any_of)) and all(x in l for x in all_of)
            and not any(x in l for x in excludes))


# Rules that have data in the snapshot, with their definition.
EVALUABLE = {
    ("lucretili", "R9a_temp_lt"): dict(match=dict(any_of=("temp",)), kind="window", windows=[(24, "range", "R9a_temp_lt")]),
    ("lucretili", "R9b_temp_st"): dict(match=dict(any_of=("temp",)), kind="max_abs_diff", hours=1, key="R9b_temp_st"),
    ("lucretili", "R6a_rain"): dict(match=dict(any_of=("rain",)), kind="window",
                                    windows=[(1, "mean", "R6a_rain_1h"), (24, "mean", "R6a_rain_24h")]),
    ("lucretili", "R6b_rain_cum7d"): dict(match=dict(any_of=("rain",)), kind="window", windows=[(168, "sum", "R6b_rain_cum7d")]),
    ("lucretili", "R5_visitors"): dict(match=dict(any_of=("counter",)), kind="direct", key="R5_visitors_peak"),
    ("ranverso", "R2_rain_7d"): dict(match=dict(any_of=("rain",), excludes=("acc",)), kind="window",
                                     windows=[(168, "sum", "R2_rain_7d_diff")]),
    ("schenkenberg", "R3_vib_zscore"): dict(match=dict(any_of=("pga", "rms")), kind="zscore", key="R3_vib_zscore"),
    ("schenkenberg", "R4_pga"): dict(match=dict(any_of=("pga",)), kind="zscore", key="R4_pga"),
}
# question groups: (site, phrase, rule ids)
DATA_GROUPS = [
    ("lucretili", "temperature", ["R9a_temp_lt", "R9b_temp_st"]),
    ("lucretili", "rainfall", ["R6a_rain", "R6b_rain_cum7d"]),
    ("lucretili", "visitor count", ["R5_visitors"]),
    ("ranverso", "rainfall", ["R2_rain_7d"]),
    ("schenkenberg", "vibration", ["R3_vib_zscore", "R4_pga"]),
]
NO_DATA_GROUPS = [
    ("delos", "rainfall"), ("delos", "wind speed"), ("delos", "humidity"), ("baltanas", "rainfall"),
    ("baltanas", "humidity"), ("baltanas", "soil moisture"), ("baltanas", "airflow"), ("baltanas", "vibration (PPV)"),
    ("lucretili", "humidity"), ("lucretili", "wind speed"), ("lucretili", "crack width"), ("lucretili", "tilt"),
    ("lucretili", "barometric pressure"), ("ranverso", "humidity"), ("ranverso", "soil moisture"),
    ("schenkenberg", "crack width"), ("schenkenberg", "combined low temperature and high humidity"),
]
NO_RULE_GROUPS = [("delos", "temperature"), ("baltanas", "temperature"), ("ranverso", "temperature"),
                  ("baltanas", "soil temperature"), ("delos", "voltage")]
RULE_PHRASE = {
    "R1_ppv": "peak particle velocity (PPV)", "R2_hum_daily_range": "daily humidity range",
    "R3_gnss_change": "day-over-day GNSS position change", "R4a_soil_high": "high soil moisture",
    "R4b_soil_range": "daily soil moisture range", "R5a_airflow_const": "airflow constancy",
    "R5b_airflow_range": "airflow range", "R6_rain_1h": "1-hour rainfall", "R1a_rain_1h": "1-hour rainfall",
    "R1b_rain_3h": "3-hour rainfall", "R2_wind": "wind speed", "R3_hum_cross": "humidity threshold crossings",
    "R10_solar_zscore": "daily GNSS z-score", "R1a_crack_step": "crack step", "R1b_crack_offset": "crack offset",
    "R2a_tilt_step": "tilt step", "R2b_tilt_offset": "tilt offset", "R3_vib_zscore": "vibration z-score",
    "R4a_hum_spike_6h": "6-hour humidity spike", "R4b_hum_persist_7d": "7-day humidity persistence",
    "R4c_hum_rapid_1h": "rapid 1-hour humidity change", "R5_visitors": "visitor peak",
    "R6a_rain": "1-hour and 24-hour rainfall", "R6b_rain_cum7d": "7-day cumulative rainfall",
    "R7_wind": "wind peak ratio", "R8_baro": "6-hour barometric pressure range",
    "R9a_temp_lt": "daily temperature range", "R9b_temp_st": "short-term (1-hour) temperature change",
    "R1_hum_inside": "indoor humidity", "R2_rain_7d": "7-day rainfall", "R3_temp_nodiff": "soil/air temperature difference",
    "R4b_soil_low": "low soil moisture", "R1_temp_hum": "low temperature with high humidity",
    "R2_crack_step": "crack step", "R4_pga": "peak ground acceleration (PGA)",
}


class RuleEngine:
    def __init__(self, b: Bench, d):
        self.b, self.d = b, d
        self.policies = {(s, r): (tv, json.loads(tj) if tj else {}) for s, r, tv, tj in b.q(
            "SELECT site_id, rule_id, threshold_value, threshold_json FROM policies WHERE left(label, 5) = 'AD-RT'")}
        self.series = {}
        props_at = defaultdict(set)
        for s, p in b.q("""SELECT DISTINCT r.site_id, o.property_id FROM observations o JOIN readings r USING (reading_id)
                           WHERE o.value IS NOT NULL"""):
            props_at[s].add(p)
        for (s, rule), spec in EVALUABLE.items():
            props = sorted(p for p in props_at[s] if _matches(p, **spec["match"]))
            cols = defaultdict(lambda: ([], []))
            for sensor, p, t, v in b.q("""SELECT r.sensor_id, o.property_id, o.result_time, o.value FROM observations o
                                          JOIN readings r USING (reading_id) WHERE r.site_id = %s AND o.property_id = ANY(%s)
                                          AND o.value IS NOT NULL ORDER BY o.result_time""", s, props):
                cols[(sensor, p)][0].append(t)
                cols[(sensor, p)][1].append(float(v))
            self.series[(s, rule)] = dict(cols)

    def threshold(self, site, rule, key):
        tv, tj = self.policies[(site, rule)]
        return float(tj.get(key, tv))

    def evaluate(self, site, rule, as_of: datetime | None):
        """(fired, detail) or (None, reason) when it cannot be evaluated."""
        spec, cols = EVALUABLE[(site, rule)], self.series[(site, rule)]
        cut = as_of or self.d["end"]
        times = [ts[bisect.bisect_right(ts, cut) - 1] for ts, _ in cols.values() if bisect.bisect_right(ts, cut)]
        if not times:
            return None, "no readings"
        anchor = max(times)

        def window(hours):
            out = {}
            for k, (ts, vs) in cols.items():
                i, j = bisect.bisect_left(ts, anchor - timedelta(hours=hours)), bisect.bisect_right(ts, anchor)
                if j > i:
                    out[k] = vs[i:j]
            return out

        if spec["kind"] == "window":
            metrics, thrs = [], []
            for hours, agg, key in spec["windows"]:
                w = window(hours)
                vals = [sum(v) if agg == "sum" else sum(v) / len(v) if agg == "mean" else max(v) - min(v) for v in w.values()]
                if vals:
                    metrics.append(max(vals))
                    thrs.append(self.threshold(site, rule, key))
            if not metrics:
                return None, "no readings in window"
            m, t = max(metrics), max(thrs)
            return m > t, f"{rule}: metric {fnum(m)} vs threshold {fnum(t)} (window ending {ftime(anchor)})"
        if spec["kind"] == "max_abs_diff":
            w = window(spec["hours"])
            vals = [max(abs(v[i] - v[i - 1]) for i in range(1, len(v))) for v in w.values() if len(v) >= 2]
            if not vals:
                return None, "fewer than 2 readings in window"
            t = self.threshold(site, rule, spec["key"])
            return max(vals) > t, f"{rule}: max 1h change {fnum(max(vals))} vs threshold {fnum(t)} (ending {ftime(anchor)})"
        if spec["kind"] == "direct":
            latest = [vs[ts.index(anchor)] for ts, vs in cols.values() if anchor in ts]
            t = self.threshold(site, rule, spec["key"])
            return max(latest) > t, f"{rule}: latest reading {fnum(max(latest))} at {ftime(anchor)} vs threshold {fnum(t)}"
        if spec["kind"] == "zscore":
            zs = []
            for ts, vs in cols.values():
                j = bisect.bisect_right(ts, cut)
                xs = vs[:j]
                if len(xs) < 2:
                    continue
                mean = sum(xs) / len(xs)
                var = sum((x - mean) ** 2 for x in xs) / len(xs)
                if var > 1e-12:
                    zs.append(abs(xs[-1] - mean) / math.sqrt(var))
            if not zs:
                return None, "no series with enough variance"
            t = self.threshold(site, rule, spec["key"])
            return max(zs) > t, f"{rule}: max z-score {fnum(max(zs))} vs threshold {fnum(t)}"
        raise ValueError(spec["kind"])

    def verdict(self, site, rules, as_of):
        results = [(r, *self.evaluate(site, r, as_of)) for r in rules]
        details = [f"{r}: {detail}" if fired is None else detail for r, fired, detail in results]
        evaluated = [fired for _, fired, _ in results if fired is not None]
        if any(evaluated):
            return "Yes", details
        if evaluated:
            return "No", details
        return "Cannot be determined", details


def gen_anomaly(b: Bench, d, eng: RuleEngine):
    rng = random.Random(SEED + 3)
    days = [date(2026, 5, 14) + timedelta(days=i) for i in range(90)]
    phr = [
        "Was the {q} at {S} anomalous on {D} according to its AD-RT rules?",
        "Did the {q} at {S} exceed its AD-RT threshold on {D}?",
        "According to the AD-RT expert rules, was there a {q} anomaly at {S} on {D}?",
    ]
    for site, phrase, rules in DATA_GROUPS:
        pool = defaultdict(list)
        for day in days:
            if (site, phrase) == ("lucretili", "temperature") and day == date(2026, 5, 15):
                continue  # HeriKGQA few-shot example
            as_of = datetime.combine(day, datetime.max.time(), tzinfo=timezone.utc).replace(microsecond=0)
            v, det = eng.verdict(site, rules, as_of)
            pool[v].append((day, det))
        # Yes only occurs for two groups and three groups are always No, so cap
        # per verdict to keep the verdicts roughly balanced.
        cap = {"Yes": 10, "No": 4, "Cannot be determined": 5}
        for v, lst in pool.items():
            for day, det in rng.sample(lst, min(len(lst), cap[v])):
                tmpl = rng.choice(phr)
                b.add("anomaly", "verdict_on_date", tmpl.format(q=phrase, S=SITE[site], D=day.isoformat()),
                      f"{v}. " + "; ".join(det), v, rules=rules)
        v, det = eng.verdict(site, rules, None)
        b.add("anomaly", "verdict_latest", f"Based on the latest data, is there a {phrase} anomaly at {SITE[site]} according to its AD-RT rules?",
              f"{v}. " + "; ".join(det), v, rules=rules)
    for site, phrase in NO_DATA_GROUPS:
        tmpl = rng.choice(phr)
        day = rng.choice(days)
        b.add("anomaly", "verdict_no_data", tmpl.format(q=phrase, S=SITE[site], D=day.isoformat()),
              f"Cannot be determined: the snapshot has no {phrase} readings at {SITE[site]} for its AD-RT rule(s).",
              "Cannot be determined")
    for site, phrase in NO_RULE_GROUPS:
        b.add("anomaly", "verdict_no_rule", f"Has the {phrase} at {SITE[site]} exceeded its AD-RT threshold?",
              f"Cannot be determined: no AD-RT rule is defined for {phrase} at {SITE[site]}.", "Cannot be determined")
    for (site, rule), (tv, tj) in sorted(eng.policies.items()):
        if ("threshold", site, rule) in EXCLUDED:
            continue
        ref = ", ".join(f"{k} = {fnum(float(v))}" for k, v in tj.items()) if tj else fnum(float(tv))
        b.add("anomaly", "threshold_lookup", f"What threshold does the AD-RT {RULE_PHRASE[rule]} rule at {SITE[site]} use?",
              f"Rule {rule}: {ref}.", tj or float(tv), rule=rule)


# ── follow-up ──────────────────────────────────────────────────────────────

def gen_followup(b: Bench, d, eng: RuleEngine):
    rng = random.Random(SEED + 4)

    def add(template, turns, question, reference, value, answerable=True):
        b.add("followup", template, question, reference, value, answerable=answerable,
              history=[{"question": q, "answer": a} for q, a in turns])

    def stat_ref(s, p, key):
        st = d["stats"][(s, p)]
        return f"{fnum(float(st[key]))}" + (f" {unit(st['unit'])}" if st["unit"] else "") + "."

    for p in ["temperature", "voltage"]:
        for a, c in itertools.permutations(SITES, 2):
            if p in SITE_QUANTITIES[a] and p in SITE_QUANTITIES[c]:
                add("what_about_site", [(f"What is the average {QNAME[p]} at {SITE[a]}?", f"The average {QNAME[p]} at {SITE[a]} is {stat_ref(a, p, 'avg')}")],
                    f"What about {SITE[c]}?", stat_ref(c, p, "avg"), float(d["stats"][(c, p)]["avg"]))
    for s in SITES:
        for p in SITE_QUANTITIES[s]:
            add("and_the_minimum", [(f"What is the maximum {QNAME[p]} recorded at {SITE[s]}?", f"The maximum is {stat_ref(s, p, 'mx')}")],
                "And the minimum?", stat_ref(s, p, "mn"), float(d["stats"][(s, p)]["mn"]))
            v, t = d["argmax"][(s, p)]
            add("when_recorded", [(f"What is the maximum {QNAME[p]} recorded at {SITE[s]}?", f"The maximum is {stat_ref(s, p, 'mx')}")],
                "When was it recorded?", f"{ftime(t)}.", ftime(t))
            add("among_these", [(f"How many sensors have reported readings at {SITE[s]}?", plural(d['sensors_n'][s], "sensor") + ".")],
                f"Among these, how many measure {QNAME[p]}?", plural(d['sensors_q'][(s, p)], "sensor") + ".", d["sensors_q"][(s, p)])
    for s in SITES:
        ns = [n for n in d["nodes"][s] if n[3] is not None]
        top, bot = max(ns, key=lambda n: n[3]), min(ns, key=lambda n: n[3])
        add("and_the_lowest", [(f"Which sensor node at {SITE[s]} is at the highest altitude?", f"{top[0]}, at {fnum(top[3], 2)} m.")],
            "And which one is the lowest?", f"{bot[0]}, at {fnum(bot[3], 2)} m.", bot[0])
    far = {}
    for s in SITES:
        ns = d["nodes"][s]
        far[s] = max((haversine(a[1:3], c[1:3]), a[0], c[0]) for a, c in itertools.combinations(ns, 2))
    for a, c in rng.sample(list(itertools.permutations(SITES, 2)), 10):
        add("what_about_site_spatial", [(f"How far apart are the two most distant sensor nodes at {SITE[a]}?", f"{fnum(far[a][0], 1)} m, between {far[a][1]} and {far[a][2]}.")],
            f"What about at {SITE[c]}?", f"{fnum(far[c][0], 1)} m, between {far[c][1]} and {far[c][2]}.", round(far[c][0], 1))
    daily_temp = sorted(k for k, v in d["daily"].items() if k[1] == "temperature" and v["n"] >= 10)
    for s, p, day in rng.sample(daily_temp, 40):
        nxt = (s, p, day + timedelta(days=1))
        if nxt in d["daily"] and d["daily"][nxt]["n"] >= 10:
            add("next_day", [(f"What was the average temperature at {SITE[s]} on {day.isoformat()}?", f"{fnum(float(d['daily'][(s, p, day)]['avg']))}.")],
                "And on the following day?", f"{fnum(float(d['daily'][nxt]['avg']))}.", float(d["daily"][nxt]["avg"]))
    for site, phrase, rules in DATA_GROUPS:
        for _ in range(4):
            d1 = date(2026, 5, 20) + timedelta(days=rng.randrange(80))
            d2 = d1 + timedelta(days=rng.randrange(1, 10))
            if d2 > date(2026, 8, 12):
                continue
            eod = lambda x: datetime.combine(x, datetime.max.time(), tzinfo=timezone.utc).replace(microsecond=0)
            v1, det1 = eng.verdict(site, rules, eod(d1))
            v2, det2 = eng.verdict(site, rules, eod(d2))
            add("anomaly_other_date", [(f"Was the {phrase} at {SITE[site]} anomalous on {d1.isoformat()} according to its AD-RT rules?", f"{v1}. " + "; ".join(det1))],
                f"What about on {d2.isoformat()}?", f"{v2}. " + "; ".join(det2), v2)
    for s in SITES:
        for (y, m, mname), (y2, m2, mname2) in zip(MONTHS[:-1], MONTHS[1:]):
            add("next_month", [(f"How many readings were recorded at {SITE[s]} in {mname} {y}?", f"{d['monthly'].get((s, y, m), 0)} readings.")],
                "And in the following month?", f"{d['monthly'].get((s, y2, m2), 0)} readings.", d["monthly"].get((s, y2, m2), 0))
    for a, c in rng.sample(list(itertools.permutations(SITES, 2)), 12):
        add("two_turn", [(f"What is the average temperature at {SITE[a]}?", f"{stat_ref(a, 'temperature', 'avg')}"),
                         ("What about " + SITE[c] + "?", f"{stat_ref(c, 'temperature', 'avg')}")],
            "And the maximum there?", stat_ref(c, "temperature", "mx"), float(d["stats"][(c, "temperature")]["mx"]))
    for s in ["baltanas", "lucretili", "delos"]:
        add("unanswerable", [(f"What is the average temperature at {SITE[s]}?", f"{stat_ref(s, 'temperature', 'avg')}")],
            "And the relative humidity?", f"Cannot be answered: no humidity data at {SITE[s]}.", None, answerable=False)


# ── sampling and output ────────────────────────────────────────────────────

QUOTAS = {
    "basic": {"node_count": 5, "sensor_count": 5, "reading_count": 5, "quantity_count": 4, "avg_quantity": 14,
              "max_quantity": 14, "min_quantity": 13, "obs_count": 15, "sensors_measuring": 15, "site_compare": 4,
              "unanswerable": 6},
    "spatial": {"farthest_pair": 5, "centroid": 5, "highest_node": 4, "lowest_node": 4, "altitude_range": 5,
                "northernmost": 4, "southernmost": 4, "pair_distance": 28, "nearest_node": 13, "within_radius": 15,
                "site_distance": 10, "unanswerable": 3},
    "temporal": {"first_reading": 5, "last_reading": 5, "span": 5, "latest_quantity": 8, "time_of_max": 8,
                 "monthly_count": 10, "relative_window": 8, "daily_avg": 10, "daily_max": 9, "daily_min": 9,
                 "hottest_day": 8, "range_avg": 12, "unanswerable": 3},
    "anomaly": {"verdict_on_date": 45, "verdict_latest": 5, "verdict_no_data": 15, "verdict_no_rule": 5,
                "threshold_lookup": 30},
    "followup": {"what_about_site": 12, "and_the_minimum": 9, "when_recorded": 9, "among_these": 9, "and_the_lowest": 5,
                 "what_about_site_spatial": 8, "next_day": 10, "anomaly_other_date": 12, "next_month": 8,
                 "two_turn": 15, "unanswerable": 3},
}


def sample(items, quotas, rng):
    by_t = defaultdict(list)
    seen = set()
    for it in items:
        key = (it["question"], json.dumps(it.get("history"), sort_keys=True))
        if key not in seen:
            seen.add(key)
            by_t[it["template"]].append(it)
    picked = []
    shortfall = 0
    for t, n in quotas.items():
        pool = by_t.get(t, [])
        take = min(n, len(pool))
        shortfall += n - take
        picked += rng.sample(pool, take)
    if shortfall:  # top up from the larger templates, never repeating a question
        rest = [it for t, lst in by_t.items() for it in lst if it not in picked]
        picked += rng.sample(rest, min(shortfall, len(rest)))
    return picked


def main():
    random.seed(SEED)
    rng = random.Random(SEED)
    con = psycopg.connect(DSN)
    con.execute("SET TIME ZONE 'UTC'")
    b = Bench(con)
    d = load(b)
    eng = RuleEngine(b, d)
    gen_basic(b, d)
    gen_spatial(b, d)
    gen_temporal(b, d)
    gen_anomaly(b, d, eng)
    gen_followup(b, d, eng)

    out, prefix = [], {"basic": "B", "spatial": "S", "temporal": "T", "anomaly": "A", "followup": "F"}
    for qtype in ["basic", "spatial", "temporal", "anomaly", "followup"]:
        chosen = sample(b.items[qtype], QUOTAS[qtype], rng)
        assert len(chosen) == PER_TYPE, (qtype, len(chosen))
        chosen.sort(key=lambda it: (list(QUOTAS[qtype]).index(it["template"]) if it["template"] in QUOTAS[qtype] else 99,
                                    it["question"]))
        for i, it in enumerate(chosen, 1):
            out.append({"id": f"{prefix[qtype]}{i:03d}", **it})

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "benchmark_500.json").write_text(json.dumps(out, indent=1, ensure_ascii=False, default=str))
    with open(OUT / "benchmark_500.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "type", "template", "answerable", "history", "question", "reference", "validated"])
        for it in out:
            hist = " || ".join(f"Q: {h['question']} A: {h['answer']}" for h in it.get("history") or [])
            w.writerow([it["id"], it["type"], it["template"], it["answerable"], hist, it["question"], it["reference"], ""])
    meta = {
        "snapshot": "argus_postgres_20261001_180439.dump (argus_snapshot, 1,316 epoch-timestamp rows removed)",
        "observations": 3737747, "data_start": ftime(min(d["span"][s][0] for s in SITES)), "data_end": ftime(d["end"]),
        "seed": SEED, "counts": {t: sum(1 for it in out if it["type"] == t) for t in prefix},
        "unanswerable": sum(1 for it in out if not it["answerable"]),
        "conventions": __doc__.split("Conventions (also written to benchmark_500.meta.json):")[1].strip(),
        "built_at": datetime.now(timezone.utc).isoformat(),
    }
    (OUT / "benchmark_500.meta.json").write_text(json.dumps(meta, indent=1))
    print(json.dumps(meta["counts"]), "unanswerable:", meta["unanswerable"])
    for qtype in prefix:
        tm = defaultdict(int)
        for it in out:
            if it["type"] == qtype:
                tm[it["template"]] += 1
        print(qtype, dict(tm))
    av = defaultdict(int)
    for it in out:
        if it["type"] == "anomaly" and it["template"].startswith("verdict"):
            av[it["reference_value"]] += 1
    print("anomaly verdicts:", dict(av))


if __name__ == "__main__":
    main()
