"""
Reference answers for the "user" questions: real questions put to the ARGUS assistant
(ask_events.jsonl, 2026-08-21 … 2026-10-14) that the router sent to the knowledge graph / sensor
data, answered on the frozen snapshot with the conventions of build_benchmark.py.

    python scripts/build_user_questions.py

Selection (103 questions routed to the KG, deduplicated by normalised text; 80 kept):
  - kept: one question per exact duplicate (the "1." "2." numbered copies were dropped); rewordings
    of the same request are kept (paraphrase_group) — they test robustness to wording;
  - dropped: questions that are not about the KG (27, 29, 37, 48 — mis-routed document questions),
    too vague to have one answer (25, 44), and a question that is an Interactive-KBQA demo (99,
    the Baltanas 1-hour rainfall threshold; excluded from the benchmark for the same reason);
  - added: two sensor-data questions the router had sent to "fallback" (devices per site, displacement
    measurements), to make 80.
Conventions (as in the benchmark):
  - "latest", "live", "most recent": the latest data in the snapshot (it ends 2026-08-12 09:15 UTC);
  - "per site", "all ARGUS sites": the five pilot sites (not the partner pseudo-sites eurecat and
    lorawan); a total over the whole KG accepts the five-site figure too;
  - sensors / nodes at a site: those with readings there; a quantity is an observed property;
  - anomaly checks: the AD-RT rule evaluation of build_benchmark.py (RuleEngine), latest data;
  - data the snapshot does not hold (wind, humidity, soil moisture, rainfall at Delos/Baltanas — the
    LoRaWAN channels, see the partner correspondence) has the reference "no such data".
Each item carries `must` (values an answer has to state: numbers, "YYYY-MM-DD HH:MM" timestamps,
labels) and `score_mode`: all | any | verdict | negative (an answer saying the data/thing does not
exist) | decline (unanswerable) | manual (a list too long or a question needing interpretation:
judged by hand).

Output: material/benchmark_user.json and material/verify/user.md (each item with its SQL and result).
"""

from __future__ import annotations

import json
import os
import re
from datetime import timezone
from pathlib import Path

import psycopg

from build_benchmark import SITES, Bench, RuleEngine, fnum, ftime

DSN = os.environ.get("ARGUS_SNAPSHOT_DSN", "postgresql://argus:argus@localhost:5432/argus_snapshot")
MATERIAL = Path(__file__).resolve().parent.parent / "material"
SITE = {s: s.capitalize() for s in SITES}
MASKS = "n.label ILIKE 'H. Masks%%' OR n.label ILIKE '%%H. Masks_Mask%%'"   # House of Masks nodes (Delos)
MAX_LISTED = 15   # longer lists are judged by hand

# (source index in ask_events_new_questions.json order, question, kind, params[, history source, paraphrase group])
ITEMS = [
    (1, "How many sensors are deployed per site?", "per_site", {"metric": "sensors"}),
    (2, "How many readings are available in total?", "total", {"metric": "readings"}),
    (3, "what are the most recent readings in delos?", "latest_site", {"site": "delos"}, None, "latest-delos"),
    (4, "How many readings are available per site?", "per_site", {"metric": "readings"}),
    (5, "Which site has the most readings?", "argmax_site", {"metric": "readings"}),
    (6, "What is the average voltage per site?", "per_site_avg", {"prop": "voltage"}),
    (7, "Check Baltanas vibration PPV anomaly using the AD-RT vibration policy.", "verdict",
     {"site": "baltanas", "rules": ["R1_ppv"]}, None, "baltanas-ppv"),
    (8, "What are the latest 20 readings?", "latest_overall", {"n": 20}),
    (9, "What are the risks for Delos Island based on Argus Database?", "threats", {"site": "delos"}),
    (10, "Which nodes are available per site?", "nodes_per_site", {}),
    (11, "Check Baltanas soil moisture anomaly using the soil moisture policy.", "verdict",
     {"site": "baltanas", "rules": ["R4a_soil_high", "R4b_soil_range"]}),
    (12, "whats the situation in Temperature in the House of Masks", "latest_site",
     {"site": "delos", "prop": "temperature", "masks": True}, None, "masks-temperature"),
    (13, "How many temperature sensors do we have installed in The House Masks in Delos?", "count_sensors_q",
     {"site": "delos", "prop": "temperature", "masks": True}, None, "masks-temperature"),
    (14, "How many of those installed sensors in Delos are for temperature?", "count_sensors_q",
     {"site": "delos", "prop": "temperature"}, 13, "delos-temperature-sensors"),
    (15, "How many readings are available per observed quantity?", "per_quantity", {}),
    (16, "Give me the last temperature measurements for Delos Island.", "latest_site",
     {"site": "delos", "prop": "temperature"}, None, "latest-delos-temperature"),
    (17, "How many temperature sensors are there in Delos?", "count_sensors_q",
     {"site": "delos", "prop": "temperature"}, None, "delos-temperature-sensors"),
    (18, "Give me the names of the temperature sensors in Delos.", "list_sensors_q",
     {"site": "delos", "prop": "temperature"}, None, "delos-temperature-sensor-names"),
    (19, "Check Delos wind anomaly using the wind policy.", "verdict", {"site": "delos", "rules": ["R2_wind"]},
     None, "delos-wind-anomaly"),
    (20, "Check Baltanas vibration PPV anomaly using the vibration policy.", "verdict",
     {"site": "baltanas", "rules": ["R1_ppv"]}, None, "baltanas-ppv"),
    (21, "Do you have any measurements for the House of Masks?", "quantities", {"site": "delos", "masks": True}),
    (22, "how many sensors are there in delos?", "count_sensors", {"site": "delos"}, None, "delos-sensors"),
    (23, "which sensor is about temperature?", "list_sensors_q", {"site": "delos", "prop": "temperature"}, 22,
     "delos-temperature-sensor-names"),
    (24, "Check Delos rainfall anomaly using the rainfall 1 hour policy.", "verdict",
     {"site": "delos", "rules": ["R1a_rain_1h"]}),
    (26, "What is the latest reading timestamp overall?", "latest_time", {}),
    (28, "Check Baltanas rainfall anomaly using the rainfall 1 hour policy.", "verdict",
     {"site": "baltanas", "rules": ["R6_rain_1h"]}, None, "baltanas-rain-anomaly"),
    (30, "give me live temperature data from all ARGUS sites", "latest_per_site", {"prop": "temperature"}),
    (31, "give me the latest temperature data from Delos", "latest_site", {"site": "delos", "prop": "temperature"},
     None, "latest-delos-temperature"),
    (32, "latest wind dir from baltanas", "no_data", {"what": "wind direction", "site": "baltanas"},
     None, "baltanas-wind-direction"),
    (33, "give me live wind data from all ARGUS sites", "no_data", {"what": "wind"}, None, "wind-all-sites"),
    (34, "Show live temperature statistics per site", "per_site_stats", {"prop": "temperature"}),
    (35, "Do you have any crack displacement measurements at Ranverso?", "no_data",
     {"what": "crack displacement", "site": "ranverso"}, None, "ranverso-crack"),
    (36, "give me latest rainfall data from Baltanas", "no_data", {"what": "rainfall", "site": "baltanas"}),
    (38, "Which sensors are available at the baltanas site?", "list_sensors", {"site": "baltanas"}, None,
     "baltanas-sensors"),
    (39, "Where are the sensor nodes at the baltanas site?", "node_locations", {"site": "baltanas"}),
    (40, "How does the voltage range at delos compare to baltanas?", "range_compare",
     {"prop": "voltage", "sites": ["delos", "baltanas"]}),
    (41, "Has the temperature range at lucretili exceeded its threshold?", "verdict",
     {"site": "lucretili", "rules": ["R9a_temp_lt"]}),
    (42, "How does the rainfall range at Delos compare to Baltanas?", "range_compare",
     {"prop": "rainfall", "sites": ["delos", "baltanas"]}),
    (43, "Which instruments measure wind direction?", "no_data", {"what": "wind direction"}),
    (45, "Which instruments are installed in Room 214?", "unanswerable",
     {"reason": "rooms are not modelled in the knowledge graph"}),
    (46, "Which device types exist in the live ARGUS KG?", "device_types", {}),
    (47, "Which measurement protocols are used by each installed instrument?", "unanswerable",
     {"reason": "measurement protocols are not modelled in the knowledge graph"}),
    (54, "Check wind anomaly at Schenkenberg using the wind policy.", "no_rule",
     {"site": "schenkenberg", "what": "wind"}),
    (56, "5. Give me the latest wind direction from Baltanas.", "no_data", {"what": "wind direction", "site": "baltanas"},
     None, "baltanas-wind-direction"),
    (57, "6. What are the latest humidity readings from Ranverso?", "no_data", {"what": "humidity", "site": "ranverso"}),
    (58, "7. Show me the latest soil moisture data from Delos.", "no_data", {"what": "soil moisture", "site": "delos"}),
    (59, "8. How many observations are available in the live ARGUS KG?", "total", {"metric": "observations"}),
    (60, "9. How many readings are available for Delos Island?", "count_readings", {"site": "delos"}),
    (61, "10. What measurements are available at Baltanas?", "quantities", {"site": "baltanas"}),
    (62, "11. What measurements are available at Ranverso?", "quantities", {"site": "ranverso"}),
    (64, "14. Does crack displacement exist in the ARGUS database?", "crack", {"ask": "exists"}, None, "crack-exists"),
    (76, "Where is crack displacement measured?", "crack", {"ask": "where"}, None, "crack-exists"),
    (77, "Compare the temperature range between Delos and Schenkenberg.", "range_compare",
     {"prop": "temperature", "sites": ["delos", "schenkenberg"]}),
    (78, "What is the humidity range at Ranverso?", "no_data", {"what": "humidity", "site": "ranverso"}),
    (79, "What is the average rainfall at Baltanas?", "no_data", {"what": "rainfall", "site": "baltanas"}),
    (80, "Which site has the most observations?", "argmax_site", {"metric": "observations"}),
    (81, "How many observations are available per measurement?", "per_quantity", {}),
    (82, "Which measurements have the most readings?", "top_quantity", {}),
    (83, "How many wind observations are available per site?", "no_data", {"what": "wind"}, None, "wind-all-sites"),
    (84, "What is the latest value for each measurement at Delos?", "latest_each_quantity", {"site": "delos"}),
    (85, "Which instruments measure air temperature?", "list_sensors_q", {"prop": "temperature"}),
    (86, "Which instruments measure rainfall?", "list_sensors_q", {"prop": "rainfall"}),
    (87, "Which instruments measure soil moisture?", "no_data", {"what": "soil moisture"}),
    (88, "Which instruments measure crack displacement?", "crack", {"ask": "instruments"}),
    (89, "Which instruments are installed at the House of Masks?", "nodes", {"site": "delos", "masks": True}),
    (90, "Which sensors are available at Baltanas?", "list_sensors", {"site": "baltanas"}, None, "baltanas-sensors"),
    (91, "Which sensors are available at Delos?", "list_sensors", {"site": "delos"}),
    (92, "Which installed instruments are associated with Weather Stations?", "no_data", {"what": "weather station"},
     None, "weather-stations"),
    (93, "What physical quantities are monitored by weather stations?", "no_data", {"what": "weather station"},
     None, "weather-stations"),
    (94, "Which sites have wind sensors?", "no_data", {"what": "wind"}, None, "wind-all-sites"),
    (95, "Is there a rainfall anomaly at Baltanas?", "verdict", {"site": "baltanas", "rules": ["R6_rain_1h"]},
     None, "baltanas-rain-anomaly"),
    (96, "Is the latest wind speed at Delos anomalous?", "verdict", {"site": "delos", "rules": ["R2_wind"]},
     None, "delos-wind-anomaly"),
    (97, "Which AD-RT policies are available for Baltanas?", "policies", {"site": "baltanas"}),
    (98, "Which policy applies to rainfall at Baltanas?", "policy_for", {"site": "baltanas", "rule": "R6_rain_1h"}),
    (100, "Which policies are defined for Delos?", "policies", {"site": "delos"}),
    (101, "Compare wind speed readings across ARGUS sites.", "no_data", {"what": "wind speed"}, None, "wind-all-sites"),
    (102, "how many sensors are there in delos pilot?", "count_sensors", {"site": "delos"}, None, "delos-sensors"),
    (103, "how many sensors are in delos site", "count_sensors", {"site": "delos"}, None, "delos-sensors"),
    # two questions the router did not send to the KG (route "fallback") but that ask about the sensor data,
    # added to reach 80; "devices" read as sensor nodes (as the benchmark's node counts)
    (("fallback", 45), "How many devices are installed per ARGUS site?", "per_site", {"metric": "nodes"}),
    (("fallback", 49), "Which displacement measurements are available?", "displacement_quantities", {}),
]
DROPPED = {
    25: "too vague to have one answer (\"sensor values that may need attention\")",
    27: "not about the KG (how sensors are used in heritage preservation)",
    29: "not about the KG (greeting / general knowledge about Delos)",
    37: "not about the KG (general knowledge about Delos and the project)",
    44: "too vague (\"locations associated with Delos instruments\")",
    48: "not about the KG (about the system's architecture)",
    99: "an Interactive-KBQA demo (Baltanas 1-hour rainfall threshold), excluded as in the benchmark",
}
DUPLICATE_OF = {49: 4, 50: 31, 51: 33, 52: 42, 53: 35, 55: 36, 63: 21, 65: 35, 66: 33, 67: 36, 68: 56,
                69: 57, 70: 58, 71: 59, 72: 60, 73: 61, 74: 62, 75: 64}


def _literal(v) -> str:
    if isinstance(v, (list, tuple)):
        return "ARRAY[" + ", ".join(_literal(x) for x in v) + "]"
    if isinstance(v, (int, float)):
        return str(v)
    if hasattr(v, "isoformat"):
        return f"'{v.isoformat()}'"
    return "'" + str(v).replace("'", "''") + "'"


def _runnable(sql: str, args) -> str:
    """The query as psql runs it: parameters inlined, psycopg's %% unescaped, indentation normalised."""
    parts = sql.strip().split("%s")
    out = parts[0] + "".join(_literal(a) + p for a, p in zip(args, parts[1:]))
    lines = [ln.strip() for ln in out.replace("%%", "%").splitlines()]
    return "\n".join(lines) + ";"


def ts(t) -> str:
    return t.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M")


class Builder:
    def __init__(self, con):
        self.con = con
        self.b = Bench(con)
        end = self.one("SELECT max(result_time) FROM observations")
        self.end = end
        self.eng = RuleEngine(self.b, {"end": end})

    def rows(self, sql, *args):
        self.sql.append(_runnable(sql, args))
        return self.con.execute(sql, args).fetchall()

    def one(self, sql, *args):
        return self.con.execute(sql, args).fetchone()[0]

    # ── kinds: each returns (reference text, must, score_mode, status note) ───────────────────────
    def per_site(self, metric):
        col = {"sensors": "count(DISTINCT r.sensor_id)", "nodes": "count(DISTINCT r.node_id)",
               "readings": "count(*)"}.get(metric)
        if metric == "observations":
            res = self.rows("""SELECT r.site_id, count(*) FROM observations o JOIN readings r USING (reading_id)
                               WHERE r.site_id = ANY(%s) GROUP BY 1 ORDER BY 1""", SITES)
        else:
            res = self.rows(f"SELECT r.site_id, {col} FROM readings r WHERE r.site_id = ANY(%s) GROUP BY 1 ORDER BY 1",
                            SITES)
        return ("; ".join(f"{SITE[s]} {n:,}" for s, n in res) + ".", [n for _, n in res], "all", None)

    def total(self, metric):
        if metric == "readings":
            a = self.rows("SELECT count(*) FROM readings")[0][0]
            p = self.rows("SELECT count(*) FROM readings WHERE site_id = ANY(%s)", SITES)[0][0]
        else:
            a = self.rows("SELECT count(*) FROM observations")[0][0]
            p = self.rows("""SELECT count(*) FROM observations o JOIN readings r USING (reading_id)
                             WHERE r.site_id = ANY(%s)""", SITES)[0][0]
        return (f"{a:,} {metric} in the knowledge graph ({p:,} at the five pilot sites).", [a, p], "any", None)

    def argmax_site(self, metric):
        res = self.per_site(metric)
        vals = dict(zip(SITES, res[1]))
        s = max(vals, key=vals.get)
        return (f"{SITE[s]} ({vals[s]:,} {metric}).", [SITE[s]], "all", None)

    def per_site_avg(self, prop):
        res = self.rows("""SELECT r.site_id, avg(o.value) FROM observations o JOIN readings r USING (reading_id)
                           WHERE o.property_id = %s AND o.value IS NOT NULL AND r.site_id = ANY(%s)
                           GROUP BY 1 ORDER BY 1""", prop, SITES)
        return ("; ".join(f"{SITE[s]} {fnum(float(a))}" for s, a in res) + ".",
                [round(float(a), 3) for _, a in res], "all", None)

    def per_site_stats(self, prop):
        res = self.rows("""SELECT r.site_id, count(*), min(o.value), avg(o.value), max(o.value)
                           FROM observations o JOIN readings r USING (reading_id)
                           WHERE o.property_id = %s AND o.value IS NOT NULL AND r.site_id = ANY(%s)
                           GROUP BY 1 ORDER BY 1""", prop, SITES)
        text = "; ".join(f"{SITE[s]}: {n:,} observations, min {fnum(float(mn))}, mean {fnum(float(a))}, "
                         f"max {fnum(float(mx))}" for s, n, mn, a, mx in res)
        return (text + ".", [round(float(a), 3) for _, _, _, a, _ in res], "manual",
                "\"statistics\" is open: the reference gives count, min, mean and max per site; judged by hand")

    def _where(self, site, prop, masks, values=True):
        """values=False for counts and lists (as the benchmark counts sensors and quantities:
        any observation); values=True where a value is used (latest, range, mean)."""
        w, args = (["o.value IS NOT NULL"] if values else ["TRUE"]), []
        if site:
            w.append("r.site_id = %s")
            args.append(site)
        else:
            w.append("r.site_id = ANY(%s)")
            args.append(SITES)
        if prop:
            w.append("o.property_id = %s")
            args.append(prop)
        if masks:
            w.append(f"({MASKS})")
        return " AND ".join(w), args

    def latest_site(self, site, prop=None, masks=False):
        w, a = self._where(site, prop, masks)
        t = self.rows(f"""SELECT max(o.result_time) FROM observations o JOIN readings r USING (reading_id)
                          JOIN nodes n USING (node_id) WHERE {w}""", *a)[0][0]
        res = self.rows(f"""SELECT n.label, se.label, o.property_id, o.value FROM observations o
                            JOIN readings r USING (reading_id) JOIN nodes n USING (node_id) JOIN sensors se USING (sensor_id)
                            WHERE {w} AND o.result_time = %s ORDER BY 1, 3""", *a, t)
        vals = "; ".join(f"{lbl} {p} {fnum(float(v))}" for lbl, _, p, v in res[:12])
        more = f" … and {len(res) - 12} more" if len(res) > 12 else ""
        where = "the House of Masks" if masks else SITE[site]
        return (f"Latest {prop or 'readings'} at {where}: {ts(t)} UTC — {vals}{more}.", [ts(t)], "all", None)

    def latest_per_site(self, prop):
        res = self.rows("""SELECT r.site_id, max(o.result_time) FROM observations o JOIN readings r USING (reading_id)
                           WHERE o.property_id = %s AND o.value IS NOT NULL AND r.site_id = ANY(%s)
                           GROUP BY 1 ORDER BY 1""", prop, SITES)
        return ("Latest " + prop + " per site: " + "; ".join(f"{SITE[s]} {ts(t)} UTC" for s, t in res) + ".",
                [ts(t) for _, t in res], "all", "the values at those times are in the SQL result")

    def latest_overall(self, n):
        res = self.rows("""SELECT r.result_time, r.site_id, n.label FROM readings r JOIN nodes n USING (node_id)
                           WHERE EXISTS (SELECT 1 FROM observations o WHERE o.reading_id = r.reading_id)
                           ORDER BY r.result_time DESC LIMIT %s""", n)
        sites = sorted({SITE.get(s, s) for _, s, _ in res})
        return (f"The latest {n} readings run from {ts(res[-1][0])} to {ts(res[0][0])} UTC, at {', '.join(sites)}.",
                [ts(res[0][0])], "all", "readings with observations (the KG's latest data); the list is in the SQL result")

    def latest_time(self):
        t = self.rows("SELECT max(result_time) FROM observations")[0][0]
        t2 = self.rows("SELECT max(result_time) FROM readings")[0][0]
        return (f"{ts(t)} UTC (latest observation; the latest reading record, a LoRaWAN reading without values, "
                f"is {ts(t2)} UTC).", [ts(t), ts(t2)], "any", None)

    def count_sensors_q(self, site, prop, masks=False):
        w, a = self._where(site, prop, masks, values=False)
        n = self.rows(f"""SELECT count(DISTINCT r.sensor_id) FROM observations o JOIN readings r USING (reading_id)
                          JOIN nodes n USING (node_id) WHERE {w}""", *a)[0][0]
        where = "the House of Masks" if masks else SITE[site]
        return (f"{n} sensors measure {prop} at {where}.", [n], "all", None)

    def list_sensors_q(self, prop, site=None):
        w, a = self._where(site, prop, False, values=False)
        res = self.rows(f"""SELECT DISTINCT r.site_id, r.sensor_id, se.label FROM observations o
                            JOIN readings r USING (reading_id) JOIN sensors se USING (sensor_id) WHERE {w} ORDER BY 1, 3""", *a)
        res = [(s, lbl) for s, _, lbl in res]
        labels = [lbl for _, lbl in res]
        where = SITE[site] if site else "the five sites"
        text = f"{len(labels)} sensors measure {prop} at {where}: " + ", ".join(
            (f"{lbl}" if site else f"{lbl} ({SITE[s]})") for s, lbl in res) + "."
        return (text, labels, "all" if len(labels) <= MAX_LISTED else "manual",
                None if len(labels) <= MAX_LISTED else f"{len(labels)} sensors: judged by hand")

    def count_sensors(self, site):
        n = self.rows("SELECT count(DISTINCT sensor_id) FROM readings WHERE site_id = %s", site)[0][0]
        return (f"{n} sensors have readings at {SITE[site]}.", [n], "all", None)

    def count_readings(self, site):
        n = self.rows("SELECT count(*) FROM readings WHERE site_id = %s", site)[0][0]
        return (f"{n:,} readings.", [n], "all", None)

    def list_sensors(self, site):
        res = self.rows("""SELECT DISTINCT r.sensor_id, se.label FROM readings r JOIN sensors se USING (sensor_id)
                           WHERE r.site_id = %s ORDER BY 2""", site)
        labels = sorted({lbl for _, lbl in res})
        return (f"{len(res)} sensors ({len(labels)} distinct names): " + ", ".join(labels) + ".", labels,
                "all" if len(labels) <= MAX_LISTED else "manual",
                None if len(labels) <= MAX_LISTED else f"{len(labels)} sensors: judged by hand")

    def quantities(self, site, masks=False):
        w, a = self._where(site, None, masks, values=False)
        res = self.rows(f"""SELECT o.property_id, count(*) FROM observations o JOIN readings r USING (reading_id)
                            JOIN nodes n USING (node_id) WHERE {w} GROUP BY 1 ORDER BY 1""", *a)
        names = [p for p, _ in res]
        where = "the House of Masks" if masks else SITE[site]
        return (f"{len(names)} quantities are measured at {where}: " + ", ".join(names) + ".", names,
                "all" if len(names) <= MAX_LISTED else "manual",
                None if len(names) <= MAX_LISTED else f"{len(names)} quantities: judged by hand")

    def nodes(self, site, masks=False):
        res = self.rows(f"""SELECT DISTINCT n.label FROM nodes n JOIN readings r USING (node_id)
                            WHERE r.site_id = %s {"AND (" + MASKS + ")" if masks else ""} ORDER BY 1""", site)
        labels = [r[0] for r in res]
        return (f"{len(labels)} sensor nodes: " + ", ".join(labels) + ".", labels,
                "all" if len(labels) <= MAX_LISTED else "manual", None)

    def nodes_per_site(self):
        res = self.rows("""SELECT r.site_id, count(DISTINCT n.node_id), string_agg(DISTINCT n.label, ', ')
                           FROM nodes n JOIN readings r USING (node_id) WHERE r.site_id = ANY(%s) GROUP BY 1 ORDER BY 1""",
                        SITES)
        return ("; ".join(f"{SITE[s]} ({k}): {lbls}" for s, k, lbls in res) + ".", [k for _, k, _ in res], "manual",
                "58 node names: judged by hand (must lists the node count per site)")

    def node_locations(self, site):
        res = self.rows("""SELECT DISTINCT n.label, n.latitude, n.longitude, n.altitude FROM nodes n
                           JOIN readings r USING (node_id) WHERE r.site_id = %s ORDER BY 1""", site)
        located = [(lbl, la, lo, al) for lbl, la, lo, al in res if la is not None]
        text = "; ".join(f"{lbl} ({float(la):.6f}, {float(lo):.6f}" + (f", {float(al):.2f} m)" if al is not None else ")")
                         for lbl, la, lo, al in located)
        return (f"{len(located)} located nodes: {text}.", [lbl for lbl, *_ in located], "manual",
                f"{len(located)} nodes with coordinates: judged by hand")

    def per_quantity(self):
        res = self.rows("""SELECT o.property_id, count(*) FROM observations o JOIN readings r USING (reading_id)
                           WHERE r.site_id = ANY(%s) GROUP BY 1 ORDER BY 2 DESC""", SITES)
        top = "; ".join(f"{p} {n:,}" for p, n in res[:10])
        return (f"{len(res)} quantities; the most frequent: {top} … (full list in the SQL result).",
                [p for p, _ in res[:3]], "manual", f"{len(res)} quantities: judged by hand")

    def top_quantity(self):
        res = self.rows("""SELECT o.property_id, count(*) FROM observations o JOIN readings r USING (reading_id)
                           WHERE r.site_id = ANY(%s) GROUP BY 1 ORDER BY 2 DESC LIMIT 5""", SITES)
        return (f"{res[0][0]} ({res[0][1]:,} observations), then " +
                ", ".join(f"{p} ({n:,})" for p, n in res[1:]) + ".", [res[0][0]], "all", None)

    def latest_each_quantity(self, site):
        res = self.rows("""SELECT DISTINCT ON (o.property_id) o.property_id, o.result_time, o.value
                           FROM observations o JOIN readings r USING (reading_id)
                           WHERE r.site_id = %s AND o.value IS NOT NULL ORDER BY o.property_id, o.result_time DESC""",
                        site)
        return ("; ".join(f"{p} {fnum(float(v))} at {ts(t)}" for p, t, v in res) + " (UTC).", [p for p, *_ in res],
                "manual", f"{len(res)} quantities (several sensors each): judged by hand")

    def range_compare(self, prop, sites):
        res = {s: (mn, mx) for s, mn, mx in self.rows(
            """SELECT r.site_id, min(o.value), max(o.value) FROM observations o JOIN readings r USING (reading_id)
               WHERE o.property_id = %s AND o.value IS NOT NULL AND r.site_id = ANY(%s) GROUP BY 1""", prop, sites)}
        parts, must = [], []
        for s in sites:
            if s in res:
                mn, mx = (float(x) for x in res[s])
                parts.append(f"{SITE[s]} {fnum(mn)} to {fnum(mx)}")
                must += [round(mn, 3), round(mx, 3)]
            else:
                parts.append(f"{SITE[s]}: no {prop} data in the snapshot")
        mode = "all" if must else "negative"
        return ("; ".join(parts) + ".", must, mode, None if must else "neither site has data")

    LORAWAN = ("wind", "humidity", "rainfall", "soil moisture", "weather station")

    def no_data(self, what, site=None):
        where = f" at {SITE[site]}" if site else ""
        why = (" (these channels come from LoRaWAN devices whose values were not ingested)"
               if any(what.startswith(k) for k in self.LORAWAN) else "")
        return (f"No {what} data{where} in the snapshot{why}.", [], "negative", None)

    def no_rule(self, site, what):
        rules = self.rows("SELECT rule_id FROM policies WHERE site_id = %s AND left(label, 5) = 'AD-RT' ORDER BY 1",
                          site)
        return (f"Cannot be determined: no AD-RT rule is defined for {what} at {SITE[site]} (its rules: "
                f"{', '.join(r[0] for r in rules)}).", ["Cannot be determined"], "verdict", None)

    def verdict(self, site, rules):
        self.sql.append(f"-- AD-RT rule evaluation (build_benchmark.RuleEngine) at {SITE[site]}, rules {rules}, "
                        f"latest data (windows ending {ts(self.end)} UTC); see verify/anomaly.md for the rule SQL")
        from build_benchmark import EVALUABLE
        evaluable = [r for r in rules if (site, r) in EVALUABLE]
        missing = [f"{r}: no readings in the snapshot" for r in rules if (site, r) not in EVALUABLE]
        if evaluable:
            v, det = self.eng.verdict(site, evaluable, None)
        else:   # as the benchmark's verdict_no_data questions
            v, det = "Cannot be determined", []
        return (f"{v}. " + "; ".join(det + missing), [v], "verdict", None)

    def policies(self, site):
        res = self.rows("""SELECT rule_id, label, threshold_value, threshold_json FROM policies
                           WHERE site_id = %s AND left(label, 5) = 'AD-RT' ORDER BY 1""", site)
        return (f"{len(res)} AD-RT policies: " + "; ".join(f"{r} ({lbl.split(' - ', 1)[-1]})" for r, lbl, *_ in res) + ".",
                [r for r, *_ in res], "all", None)

    def policy_for(self, site, rule):
        res = self.rows("""SELECT rule_id, label, threshold_value FROM policies WHERE site_id = %s AND rule_id = %s""",
                        site, rule)
        r, lbl, tv = res[0]
        return (f"{r} ({lbl}).", [r], "all", None)

    def threats(self, site):
        res = self.rows("SELECT label FROM threats WHERE label ILIKE %s ORDER BY 1", f"%{site}%")
        return (f"{len(res)} threats (risk scenarios) concern {SITE[site]}: " + "; ".join(r[0] for r in res) + ".",
                [r[0] for r in res], "manual", f"{len(res)} risk scenarios: judged by hand")

    def device_types(self):
        res = self.rows("SELECT model, count(*) FROM nodes WHERE model IS NOT NULL GROUP BY 1 ORDER BY 2 DESC")
        return ("Node (device) models: " + "; ".join(f"{m} ({n})" for m, n in res) + ".", [m for m, _ in res],
                "manual", "\"device types\" read as node models; judged by hand")

    def displacement_quantities(self):
        res = self.rows("""SELECT r.site_id, o.property_id, count(*) FROM observations o JOIN readings r USING (reading_id)
                           WHERE o.property_id ILIKE '%%displacement%%' AND r.site_id = ANY(%s) GROUP BY 1, 2 ORDER BY 1, 2""",
                        SITES)
        return (f"{len(res)} displacement quantities: " + "; ".join(f"{p} at {SITE[s]} ({n:,} observations)"
                                                                    for s, p, n in res) + ".",
                [p for _, p, _ in res], "all", None)

    def crack(self, ask):
        res = self.rows("""SELECT r.site_id, o.property_id, string_agg(DISTINCT n.label, ' | '),
                                  string_agg(DISTINCT se.label, ' | '), count(*)
                           FROM observations o JOIN readings r USING (reading_id) JOIN nodes n USING (node_id)
                           JOIN sensors se USING (sensor_id)
                           WHERE o.property_id ILIKE '%%potentiometer%%' GROUP BY 1, 2""")
        crackmeters = self.rows("""SELECT DISTINCT r.site_id, n.label FROM nodes n JOIN readings r USING (node_id)
                                   WHERE n.label ILIKE '%%crack%%' ORDER BY 2""")
        text = ("No quantity is called crack displacement. Displacement is measured by potentiometers at Delos, House of "
                "Masks (" + "; ".join(f"{p} on {nodes}" for _, p, nodes, _, _ in res) + "). Lucretili has crackmeter "
                "nodes (" + ", ".join(lbl for _, lbl in crackmeters) + ") but no displacement values.")
        return (text, ["potentiometer_displacement"], "manual",
                "whether potentiometer displacement counts as crack displacement needs the partner's confirmation")

    def unanswerable(self, reason):
        return (f"Cannot be answered from the knowledge graph: {reason}.", [], "decline", None)


def main():
    src = json.load(open(MATERIAL.parent.parent / "experiments" / "ask_events_new_questions.json"))
    kg = [o["question"] for o in src if o["category"].startswith("KG")]
    fallback = [o["question"] for o in src if o["category"].startswith("fallback")]
    con = psycopg.connect(DSN)
    con.execute("SET TIME ZONE 'UTC'")
    B = Builder(con)
    items, by_src, md = [], {}, []
    for k, entry in enumerate(ITEMS, 1):
        n, q, kind, params, *rest = entry
        hist_src = rest[0] if rest else None
        group = rest[1] if len(rest) > 1 else None
        group_src, n_src = n if isinstance(n, tuple) else ("KG", n)
        pool = fallback if group_src == "fallback" else kg
        assert pool[n_src - 1].strip() == q, (n, pool[n_src - 1], q)
        B.sql = []
        ref, must, mode, note = getattr(B, kind)(**params)
        q_clean = re.sub(r"^\d+\.\s+", "", q)   # the user's own list numbering ("5. Give me …")
        item = {"id": f"U{k:03d}", "type": "user", "template": kind, "question": q_clean, "reference": ref,
                "reference_value": must, "score_mode": mode, "answerable": mode != "decline",
                "source": f"ask_events.jsonl ({group_src} question {n_src})"}
        if group:
            item["paraphrase_group"] = group
        if hist_src:
            prev = by_src[hist_src]
            item["history"] = [{"question": prev["question"], "answer": prev["reference"]}]
        items.append(item)
        by_src[n] = item
        status = "MANUAL" if mode == "manual" else "COMPUTED"
        md += [f"## {item['id']} · {kind}", "", f"**Question:** {q_clean}  "]
        if hist_src:
            md.append(f"**Earlier turn:** {item['history'][0]['question']}  ")
        md += [f"**Reference:** {ref}  ", f"**Must state:** {must if must else '—'}  ",
               f"**Scoring:** {mode} → **{status}**" + (f" ({note})" if note else ""), ""]
        if B.sql:
            md += ["```sql", "\n\n".join(B.sql), "```", ""]
        md += ["---", ""]
    head = ["# Verification — user questions", "",
            f"{len(items)} questions from ask_events.jsonl (real questions routed to the knowledge graph, and two sensor-data "
            "questions the router had sent to fallback), answered on "
            "the snapshot. COMPUTED: the reference is the SQL result shown. MANUAL: a long list or a question that needs "
            "interpretation — the reference is computed, its scoring is judged by hand.", "",
            "Dropped: " + "; ".join(f"{k} ({v})" for k, v in sorted(DROPPED.items())) + ".", "",
            "Exact duplicates merged (question → kept copy): "
            + ", ".join(f"{k}→{v}" for k, v in sorted(DUPLICATE_OF.items())) + ".", "",
            "In psql, run `SET TIME ZONE 'UTC';` first.", "", "---", ""]
    (MATERIAL / "benchmark_user.json").write_text(json.dumps(items, indent=1, ensure_ascii=False, default=str))
    (MATERIAL / "verify" / "user.md").write_text("\n".join(head + md))
    covered = {e[0] for e in ITEMS if not isinstance(e[0], tuple)} | set(DROPPED) | set(DUPLICATE_OF)
    assert covered == set(range(1, len(kg) + 1)), sorted(set(range(1, len(kg) + 1)) - covered)
    from collections import Counter
    print(len(items), "items", dict(Counter(i["score_mode"] for i in items)))


if __name__ == "__main__":
    main()
