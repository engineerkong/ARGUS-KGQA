"""
Deterministic AD-RT expert-rule evaluation (Step "Anomaly" in the pipeline,
see pipeline.py) — checks a Policy's threshold against real Observation data,
so the LLM reports a computed verdict instead of eyeballing raw rows.

Policy and Observation aren't linked by any ontology edge, only a shared Site
and a free-text keyword, so this module runs its own SPARQL (policies, then
per-rule readings) rather than reusing the caller's retrieved rows.

RULE_SPECS ports AD-RT/RT/rules.py's per-rule column matcher and computation
shape, not the loose Policy label text. Four tiers:
  - direct:  a raw reading vs. a fixed threshold.
  - windows: SUM/MEAN/RANGE over a time window ending at the latest reading
             (or `as_of`, if the question named a date) for that site+quantity.
  - zscore:  |latest - mean| / std over all available matching data.
  - custom:  rate-of-change, normalized step/offset, ratio, day-over-day
             change, a reduced derived score, or a composite two-column rule
             — see CUSTOM_EVALUATORS.
  - neither: reported as "not evaluated" rather than misapplied as a direct
             comparison (a threshold for a *daily range* is meaningless
             compared against one raw reading).

Per-sensor grouping: a site can have several physical sensors sharing one
ObservedProperty label (e.g. each instrument's own diagnostic "temperature").
Pooling them before computing a range/diff/mean isn't an approximation of
anything AD-RT computes — it's a different, meaningless number. So every
windows/zscore/custom evaluator groups by sosa:madeBySensor first, computes
per sensor, and combines via max()/min() across sensors — mirroring AD-RT's
own per-column iteration + elementwise-max combination. The "direct" tier and
the two "two_col_*" rules still pick a single latest reading with no sensor
grouping (lower risk than range/diff, but can land on an arbitrary sensor
among ties).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any
import json
import re

KNOWN_PILOT_SITES = ["delos", "baltanas", "lucretili", "ranverso", "schenkenberg"]

RECENT_WINDOW = 20  # most recent observations to check per direct-shape rule

_PREFIXES = """\
PREFIX sosa:     <http://www.w3.org/ns/sosa/>
PREFIX argus:    <http://www.argus-project.eu/ontology/>
PREFIX panoptes: <http://www.argus-project.eu/panoptes#>
PREFIX rdfs:     <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd:      <http://www.w3.org/2001/XMLSchema#>
"""


@dataclass(frozen=True)
class WindowAgg:
    duration: str          # "1h", "3h", "6h", "24h", "7d" — parsed by _parse_duration
    agg: str                # "sum" | "mean" | "range"
    threshold_key: str      # key into the Policy's thresholdJson dict


@dataclass
class RuleSpec:
    direct: bool
    # ObservedProperty label must contain at least one of any_of (if non-empty),
    # ALL of all_of, and NONE of excludes — mirrors the df.columns list
    # comprehension in AD-RT/RT/rules.py for this rule.
    any_of: tuple[str, ...] = ()
    all_of: tuple[str, ...] = ()
    excludes: tuple[str, ...] = ()
    direction: str = "gt"  # 'gt' or 'lt'
    windows: tuple[WindowAgg, ...] = ()  # non-empty => windowed-aggregate rule
    zscore: bool = False   # True => |latest - mean| / std over ALL available matching data
    custom: str | None = None       # name of a CUSTOM_EVALUATORS entry
    custom_params: dict = field(default_factory=dict)
    second_any_of: tuple[str, ...] = ()  # for two-column custom rules: the 2nd quantity's matcher
    second_all_of: tuple[str, ...] = ()
    shape: str = "direct"  # human label for the "not evaluated" message
    note: str = ""


# (site, ruleId) -> RuleSpec. ruleId is the Policy's argus:ruleId, taken
# straight from the /policies API records (37 total as of 2026-08-21).
RULE_SPECS: dict[tuple[str, str], RuleSpec] = {
    # ---- delos ----
    ("delos", "R1a_rain_1h"): RuleSpec(False, any_of=("rain",), excludes=("acc",),
        windows=(WindowAgg("1h", "sum", "R1a_rain_1h"),),
        shape="1h rolling SUM of rain"),
    ("delos", "R1b_rain_3h"): RuleSpec(False, any_of=("rain",), excludes=("acc",),
        windows=(WindowAgg("3h", "sum", "R1b_rain_3h"),),
        shape="3h rolling SUM of rain"),
    ("delos", "R2_wind"): RuleSpec(True, any_of=("wind_speed",), excludes=("dir",)),
    ("delos", "R3_hum_cross"): RuleSpec(False, any_of=("hum",),
        shape="threshold-crossing count over a double-smoothed value, 3-day window",
        note="Not evaluated: needs a 12h rolling smooth THEN a 3-sample smooth on top, both "
             "resample-bin-based on AD-RT's assumed fixed sample frequency. Approximating this "
             "on irregular raw timestamps risks a materially different crossing count from what "
             "AD-RT would report, so it is left unevaluated rather than guessed."),

    # ---- baltanas ----
    ("baltanas", "R1_ppv"): RuleSpec(True, any_of=("acc_int_ppv",)),
    ("baltanas", "R2_hum_daily_range"): RuleSpec(False, any_of=("hum",), excludes=("ee3", "hum1"),
        windows=(WindowAgg("24h", "range", "R2_hum_daily_range"),),
        shape="daily range (max-min per day)",
        note="approximated here as a rolling 24h window, not a calendar-day boundary"),
    ("baltanas", "R3_gnss_change"): RuleSpec(False, any_of=("long_term",),
        custom="day_over_day_change", custom_params={"threshold_key": "R3_gnss_change"},
        shape="day-over-day change of the daily mean",
        note="approximated as |mean(trailing 24h) - mean(the 24h before that)|, not calendar-day means"),
    ("baltanas", "R4a_soil_high"): RuleSpec(True, any_of=("soil_moisture",),
        note="AD-RT matches columns literally containing 'soil_moisture' — "
             "this KG currently only has 'soil_water_potential' under this site, "
             "a different quantity, so this will usually find no data."),
    ("baltanas", "R4b_soil_range"): RuleSpec(False, any_of=("soil_moisture",),
        windows=(WindowAgg("24h", "range", "R4b_soil_daily_range"),),
        shape="daily range (max-min per day)",
        note="Same column-name caveat as R4a_soil_high; also approximated as a rolling 24h window."),
    ("baltanas", "R5a_airflow_const"): RuleSpec(False, any_of=("airflow",),
        custom="airflow_const", custom_params={"threshold_key": "R5a_airflow_const", "window": "24h"},
        shape="derived constancy score compared to a fixed 0.5 cutoff, not to its own threshold value",
        note="Algebraically, firing metric_const>0.5 reduces to daily_max_diff < threshold/2 — "
             "evaluated here as that reduced form, over a rolling 24h window of consecutive-sample "
             "differences rather than a calendar day."),
    ("baltanas", "R5b_airflow_range"): RuleSpec(False, any_of=("airflow",),
        windows=(WindowAgg("24h", "range", "R5b_airflow_range"),),
        shape="daily range (max-min per day)",
        note="approximated here as a rolling 24h window, not a calendar-day boundary"),
    ("baltanas", "R6_rain_1h"): RuleSpec(False, any_of=("rain",), excludes=("acc",),
        windows=(WindowAgg("1h", "mean", "R6_rain_1h"),),
        shape="1h rolling MEAN of rain (note: different aggregation than delos's R1a_rain_1h, which is a SUM)"),

    # ---- lucretili ----
    ("lucretili", "R1a_crack_step"): RuleSpec(False, any_of=("crack",),
        custom="step_range_ratio", custom_params={"threshold_key": "R1a_crack_step", "short": "1h", "long": "24h"},
        shape="1h step range normalized by 24h range"),
    ("lucretili", "R1b_crack_offset"): RuleSpec(False, any_of=("crack",),
        custom="offset_ratio", custom_params={"threshold_key": "R1b_crack_offset", "short": "24h", "long": "24h"},
        shape="offset from 24h rolling mean, normalized by 24h range"),
    ("lucretili", "R2a_tilt_step"): RuleSpec(False, any_of=("tilt",),
        custom="step_range_ratio", custom_params={"threshold_key": "R2a_tilt_step", "short": "1h", "long": "24h"},
        shape="1h step range normalized by 24h range"),
    ("lucretili", "R2b_tilt_offset"): RuleSpec(False, any_of=("tilt",),
        custom="offset_ratio", custom_params={"threshold_key": "R2b_tilt_offset", "short": "24h", "long": "24h"},
        shape="offset from 24h rolling mean, normalized by 24h range"),
    ("lucretili", "R3_vib_zscore"): RuleSpec(False, any_of=("acc",), zscore=True,
        shape="z-score against the series' own mean/std"),
    ("lucretili", "R4a_hum_spike_6h"): RuleSpec(False, any_of=("hum",),
        windows=(WindowAgg("6h", "mean", "R4a_hum_spike_6h"),),
        shape="6h rolling mean"),
    ("lucretili", "R4b_hum_persist_7d"): RuleSpec(False, any_of=("hum",),
        windows=(WindowAgg("7d", "mean", "R4b_hum_persist_7d"),),
        shape="7-day rolling mean of daily means",
        note="approximated here as a plain mean over the raw 7-day window, not a mean-of-daily-means"),
    ("lucretili", "R4c_hum_rapid_1h"): RuleSpec(False, any_of=("hum",),
        custom="rate_of_change", custom_params={"threshold_key": "R4c_hum_rapid_1h", "window": "1h"},
        shape="max absolute 1h change (rate of change)",
        note="approximated as the max |consecutive-sample difference| within a rolling real-time "
             "1h window, not AD-RT's resample-bin-based rolling window"),
    ("lucretili", "R5_visitors"): RuleSpec(True, any_of=("counter",)),
    ("lucretili", "R6a_rain"): RuleSpec(False, any_of=("rain",),
        windows=(WindowAgg("1h", "mean", "R6a_rain_1h"), WindowAgg("24h", "mean", "R6a_rain_24h")),
        shape="max of 1h and 24h rolling means, vs max of the two thresholds"),
    ("lucretili", "R6b_rain_cum7d"): RuleSpec(False, any_of=("rain",),
        windows=(WindowAgg("7d", "sum", "R6b_rain_cum7d"),),
        shape="7-day rolling sum of daily sums",
        note="approximated here as a plain sum over the raw 7-day window"),
    ("lucretili", "R7_wind"): RuleSpec(False, any_of=("wind",), excludes=("dir",),
        custom="peak_ratio", custom_params={"threshold_key": "R7a_wind_peak_ratio", "window": "24h"},
        shape="peak-to-24h-baseline ratio"),
    ("lucretili", "R8_baro"): RuleSpec(False, any_of=("baro",),
        windows=(WindowAgg("6h", "range", "R8_baro_range"),),
        shape="6h rolling range (max-min)"),
    ("lucretili", "R9a_temp_lt"): RuleSpec(False, any_of=("temp",),
        windows=(WindowAgg("24h", "range", "R9a_temp_lt"),),
        shape="daily range (max-min per day)",
        note="Despite the '_lt' in the name this is a RANGE rule, not a less-than rule; "
             "approximated here as a rolling 24h window."),
    ("lucretili", "R9b_temp_st"): RuleSpec(False, any_of=("temp",),
        custom="rate_of_change", custom_params={"threshold_key": "R9b_temp_st", "window": "1h"},
        shape="max absolute 1h change (rate of change)",
        note="approximated as the max |consecutive-sample difference| within a rolling real-time "
             "1h window, not AD-RT's resample-bin-based rolling window"),
    ("lucretili", "R10_solar_zscore"): RuleSpec(False, any_of=("gnss",),
        shape="daily z-score (deviation of each day's mean from the mean of daily means, "
              "normalized by that day's OWN intra-day std — not a plain whole-series z-score)",
        note="Despite the 'solar' in the name this rule matches columns containing 'gnss', not 'solar'. "
             "Deliberately left unevaluated rather than approximated as a plain z-score: the two are "
             "different formulas and could disagree on the verdict."),

    # ---- ranverso ----
    ("ranverso", "R1_hum_inside"): RuleSpec(True, all_of=("hum", "in")),
    ("ranverso", "R2_rain_7d"): RuleSpec(False, any_of=("rain",), excludes=("acc",),
        windows=(WindowAgg("7d", "sum", "R2_rain_7d_diff"),),
        shape="7-day rolling sum",
        note="threshold_overrides key is 'R2_rain_7d_diff' but AD-RT computes a rolling SUM, not a diff."),
    ("ranverso", "R3_temp_nodiff"): RuleSpec(False, all_of=("soilmoisture_temp",),
        second_all_of=("weather", "temp"),
        custom="two_col_closeness", custom_params={"threshold_key": "R3_temp_nodiff"},
        shape="derived closeness score (|soil temp - weather temp|) compared to a fixed 0.5 cutoff, needs two paired columns",
        note="Algebraically, firing metric>0.5 reduces to |t1-t2| < threshold/2 — evaluated as that "
             "reduced form. The two readings are paired as 'latest of each', not matched to the same "
             "timestamp like AD-RT's aligned series."),
    ("ranverso", "R4a_soil_high"): RuleSpec(True, any_of=("moisture",), excludes=("temp", "hum"),
        note="AD-RT only evaluates this from 2025-11-15 onward; not enforced here."),
    ("ranverso", "R4b_soil_low"): RuleSpec(True, any_of=("moisture",), excludes=("temp", "hum"), direction="lt",
        note="AD-RT only evaluates this from 2025-11-15 onward; not enforced here."),

    # ---- schenkenberg ----
    ("schenkenberg", "R1_temp_hum"): RuleSpec(False, all_of=("temp",),
        second_any_of=("hum",),
        custom="two_col_composite", custom_params={"t_key": "R1_temp_low", "h_key": "R1_hum_high"},
        shape="composite rule (temp < threshold AND humidity > threshold, same timestamp) — needs two paired columns",
        note="The two readings are paired as 'latest of each', not matched to the same timestamp "
             "like AD-RT's aligned series."),
    ("schenkenberg", "R2_crack_step"): RuleSpec(False, any_of=("crack",),
        custom="offset_ratio", custom_params={"threshold_key": "R2_crack_step", "short": "1h", "long": "24h"},
        shape="deviation from 1h rolling mean, normalized by 24h range"),
    ("schenkenberg", "R3_vib_zscore"): RuleSpec(False, any_of=("pga", "rms"), zscore=True,
        shape="z-score against the series' own mean/std"),
    ("schenkenberg", "R4_pga"): RuleSpec(False, any_of=("pga",), zscore=True,
        shape="z-score against the series' own mean/std",
        note="Same column pattern as R3_vib_zscore at this site (both match 'pga') — different threshold, same underlying z-score."),
}


def _esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def _column_filter_expr(spec: RuleSpec) -> str:
    conds = []
    if spec.any_of:
        ors = " || ".join(f'CONTAINS(LCASE(STR(?proplabel)), "{_esc(s)}")' for s in spec.any_of)
        conds.append(f"({ors})")
    for s in spec.all_of:
        conds.append(f'CONTAINS(LCASE(STR(?proplabel)), "{_esc(s)}")')
    for s in spec.excludes:
        conds.append(f'!CONTAINS(LCASE(STR(?proplabel)), "{_esc(s)}")')
    return " && ".join(conds) if conds else "true"


def _filter_values(filters: list[dict] | None) -> list[str]:
    return [str(f.get("value", "")).strip() for f in (filters or []) if f.get("value")]


_DATE_LIKE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}")


def extract_context(intent: dict) -> tuple[str | None, str | None]:
    """Pull (site, quantity_keyword) out of a Step-1 intent — used only to
    pick which Policy row(s) are relevant; the observation lookup uses
    RULE_SPECS's column matcher instead. Date-shaped values are skipped (see
    extract_as_of) so a resultTime filter is never mistaken for the keyword."""
    values = list(_filter_values(intent.get("filters")))
    for j in intent.get("joins", []) or []:
        values.extend(_filter_values(j.get("filters")))

    site = None
    keywords = []
    for v in values:
        low = v.lower()
        if _DATE_LIKE_RE.match(low):
            continue
        if low in KNOWN_PILOT_SITES:
            site = low
        else:
            keywords.append(low)

    return site, (keywords[0] if keywords else None)


def _normalize_as_of(value: str) -> str:
    """A bare 'YYYY-MM-DD' is valid xsd:date but not valid xsd:dateTime, and
    every query here casts as_of with ^^xsd:dateTime — a malformed cast fails
    the <= comparison silently (0 rows, indistinguishable from 'no data that
    far back'). So a bare date means end-of-day: 'on 2026-05-15' = through
    the end of that day."""
    if re.match(r"^\d{4}-\d{2}-\d{2}$", value):
        return value + "T23:59:59"
    return value


def extract_as_of(intent: dict) -> str | None:
    """Pull the intent's "as_of" field (a point in time the question named,
    e.g. 'on 2026-05-15'), falling back to a date-shaped filter value for
    older/malformed intents. None means 'as of the latest available reading'
    — the default every evaluator uses when a question names no date."""
    explicit = intent.get("as_of")
    if isinstance(explicit, str) and explicit.strip():
        return _normalize_as_of(explicit.strip())

    values = list(_filter_values(intent.get("filters")))
    for j in intent.get("joins", []) or []:
        values.extend(_filter_values(j.get("filters")))
    for v in values:
        if _DATE_LIKE_RE.match(v):
            return _normalize_as_of(v)
    return None


def _query_policies(backend, site: str, keyword: str) -> list[dict[str, Any]]:
    site_e, kw_e = _esc(site), _esc(keyword)
    sparql = _PREFIXES + f"""\
SELECT ?policy ?label ?ruleid ?threshold ?thresholdjson WHERE {{
  ?policy a panoptes:Policy ; argus:appliesToSite ?site ; rdfs:label ?label .
  ?site rdfs:label "{site_e}" .
  OPTIONAL {{ ?policy argus:ruleId ?ruleid . }}
  OPTIONAL {{ ?policy argus:thresholdValue ?threshold . }}
  OPTIONAL {{ ?policy argus:thresholdJson ?thresholdjson . }}
  OPTIONAL {{ ?policy argus:threatName ?threatname . }}
  FILTER(
    CONTAINS(LCASE(STR(?label)), "{kw_e}") ||
    (BOUND(?ruleid) && CONTAINS(LCASE(STR(?ruleid)), "{kw_e}")) ||
    (BOUND(?threatname) && CONTAINS(LCASE(STR(?threatname)), "{kw_e}"))
  )
}}
"""
    return [r for r in backend.query(sparql) if "error" not in r]


def _query_recent_observations_for_spec(backend, site: str, spec: RuleSpec, limit: int,
                                         before: str | None = None) -> list[dict[str, Any]]:
    """Like _query_recent_observations, but the FILTER is built from the
    rule's own column matcher (RuleSpec), not the caller's free-text keyword —
    this is the fix for matching the wrong ObservedProperty (e.g. 'soil' loosely
    catching soil_water_potential when the rule actually means soil_moisture).
    `before`, when given, restricts to readings at or before that point in
    time — 'latest as of <before>' instead of the true latest."""
    site_e = _esc(site)
    filter_expr = _column_filter_expr(spec)
    before_filter = f'FILTER(?time <= "{_esc(before)}"^^xsd:dateTime)' if before else ""

    sparql = _PREFIXES + f"""\
SELECT ?value ?time WHERE {{
  ?oc a sosa:ObservationCollection ; argus:hasSite ?site ; argus:hasObservation ?obs ;
      sosa:resultTime ?time .
  ?site rdfs:label "{site_e}" .
  ?obs sosa:observedProperty ?prop ; sosa:hasSimpleResult ?value .
  ?prop rdfs:label ?proplabel .
  FILTER({filter_expr})
  {before_filter}
}}
ORDER BY DESC(?time)
LIMIT {int(limit)}
"""
    return [r for r in backend.query(sparql) if "error" not in r]


def _query_latest_time(backend, site: str, spec: RuleSpec, before: str | None = None) -> str | None:
    """Latest reading timestamp for this site+rule's columns — or, when
    `before` is given, the latest one at or before that point in time. Every
    windowed/custom/zscore evaluator anchors its window to whatever this
    returns, so `before` is how a question naming a specific date ('was X
    anomalous on 2026-05-15') gets honoured instead of silently ignored."""
    site_e = _esc(site)
    filter_expr = _column_filter_expr(spec)
    before_filter = f'FILTER(?time <= "{_esc(before)}"^^xsd:dateTime)' if before else ""
    sparql = _PREFIXES + f"""\
SELECT (MAX(?time) AS ?maxtime) WHERE {{
  ?oc a sosa:ObservationCollection ; argus:hasSite ?site ; argus:hasObservation ?obs ;
      sosa:resultTime ?time .
  ?site rdfs:label "{site_e}" .
  ?obs sosa:observedProperty ?prop ; sosa:hasSimpleResult ?value .
  ?prop rdfs:label ?proplabel .
  FILTER({filter_expr})
  {before_filter}
}}
"""
    rows = [r for r in backend.query(sparql) if "error" not in r]
    return rows[0].get("maxtime") if rows else None


_DURATION_RE = re.compile(r"^(\d+)([hd])$")


def _parse_duration(s: str) -> timedelta:
    m = _DURATION_RE.match(s)
    if not m:
        raise ValueError(f"Unsupported duration format: {s!r}")
    n, unit = int(m.group(1)), m.group(2)
    return timedelta(hours=n) if unit == "h" else timedelta(days=n)


def _to_float(s: Any) -> float | None:
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def _thresholds_from_json(thresholdjson: str | None) -> dict[str, float]:
    if not thresholdjson:
        return {}
    try:
        raw = json.loads(thresholdjson)
    except json.JSONDecodeError:
        return {}
    out = {}
    for k, v in raw.items():
        f = _to_float(v)
        if f is not None:
            out[k] = f
    return out


# ---------------------------------------------------------------------------
# Sensor-aware raw fetch and per-sensor aggregation — see the module
# docstring's "Per-sensor grouping" note for why this groups by sensor first.
# ---------------------------------------------------------------------------

def _query_raw_window(backend, site: str, spec: RuleSpec,
                      start_iso: str | None, end_iso: str | None) -> list[tuple[float, str, str]]:
    """(value, time, sensor) triples, ascending by time. Either bound may be
    None: end_iso=None with start_iso set means 'from start onward'; both None
    means no time bound at all (z-score's whole-series baseline when no as_of
    is given); start_iso=None with end_iso set means 'everything up to end'
    (z-score's baseline when an as_of point-in-time IS given)."""
    site_e = _esc(site)
    filter_expr = _column_filter_expr(spec)
    bounds = []
    if start_iso:
        bounds.append(f'?time >= "{_esc(start_iso)}"^^xsd:dateTime')
    if end_iso:
        bounds.append(f'?time <= "{_esc(end_iso)}"^^xsd:dateTime')
    time_filter = f"FILTER({' && '.join(bounds)})" if bounds else ""
    sparql = _PREFIXES + f"""\
SELECT ?value ?time ?sensor WHERE {{
  ?oc a sosa:ObservationCollection ; argus:hasSite ?site ; argus:hasObservation ?obs ;
      sosa:resultTime ?time ; sosa:madeBySensor ?sensor .
  ?site rdfs:label "{site_e}" .
  ?obs sosa:observedProperty ?prop ; sosa:hasSimpleResult ?value .
  ?prop rdfs:label ?proplabel .
  FILTER({filter_expr})
  {time_filter}
}}
ORDER BY ASC(?time)
"""
    rows = [r for r in backend.query(sparql) if "error" not in r]
    out = []
    for r in rows:
        v = _to_float(r.get("value"))
        if v is not None:
            out.append((v, r.get("time"), r.get("sensor") or "(unknown sensor)"))
    return out


def _group_by_sensor(triples: list[tuple[float, str, str]]) -> dict[str, list[tuple[float, str]]]:
    groups: dict[str, list[tuple[float, str]]] = {}
    for v, t, s in triples:
        groups.setdefault(s, []).append((v, t))
    return groups  # each list stays ascending-by-time since the input was sorted


def _sensor_stat(vals: list[tuple[float, str]], agg: str) -> float | None:
    if not vals:
        return None
    xs = [v for v, _ in vals]
    if agg == "sum":
        return sum(xs)
    if agg == "mean":
        return sum(xs) / len(xs)
    if agg == "range":
        return max(xs) - min(xs)
    if agg == "max_abs_diff":
        return None if len(xs) < 2 else max(abs(xs[i] - xs[i - 1]) for i in range(1, len(xs)))
    raise ValueError(f"Unsupported agg: {agg!r}")


def _combine_max(per_sensor: dict[str, float]) -> tuple[float, str, int] | None:
    """AD-RT keeps whichever sensor scored highest (_max_aligned) — mirrors
    that for a 'gt'-direction / higher-is-more-anomalous metric."""
    if not per_sensor:
        return None
    sensor, val = max(per_sensor.items(), key=lambda kv: kv[1])
    return val, sensor, len(per_sensor)


def _combine_min(per_sensor: dict[str, float]) -> tuple[float, str, int] | None:
    """For metrics where SMALLER is more anomalous (e.g. airflow_const's
    reduced form) — the sensor with the highest AD-RT score is the one with
    the smallest raw metric, so combine via min instead of max."""
    if not per_sensor:
        return None
    sensor, val = min(per_sensor.items(), key=lambda kv: kv[1])
    return val, sensor, len(per_sensor)


def _sensors_note(n: int) -> str:
    return f", max of {n} sensor(s)" if n > 1 else ""


def _evaluate_zscore(backend, site: str, rule: str, spec: RuleSpec, threshold: float | None,
                     thresholdjson: str | None, as_of: str | None = None) -> str:
    note = f" ({spec.note})" if spec.note else ""
    if threshold is None:
        return (f"  - {rule}: z-score rule but has no single numeric threshold on record "
                f"({thresholdjson}) — skipped.{note}")

    triples = _query_raw_window(backend, site, spec, None, as_of)
    groups = _group_by_sensor(triples)
    if not groups:
        return f"  - {rule}: z-score rule, but no matching readings were found.{note}"

    per_sensor_z: dict[str, float] = {}
    detail: dict[str, tuple[float, float, float, float, str]] = {}  # sensor -> (z, mean, std, latest, time)
    for sensor, vals in groups.items():
        if len(vals) < 2:
            continue
        xs = [v for v, _ in vals]
        mean = sum(xs) / len(xs)
        var = sum((x - mean) ** 2 for x in xs) / len(xs)
        if var <= 1e-12:
            continue
        std = var ** 0.5
        latest_value, latest_time = vals[-1]
        z = abs(latest_value - mean) / std
        per_sensor_z[sensor] = z
        detail[sensor] = (z, mean, std, latest_value, latest_time)

    if not per_sensor_z:
        return (f"  - {rule}: z-score rule, but no single sensor (out of {len(groups)}) had enough "
                f"readings/variance to establish a baseline.{note}")

    _, sensor, n_sensors = _combine_max(per_sensor_z)
    z, mean, std, latest_value, latest_time = detail[sensor]
    fired = z > threshold
    verdict = "EXCEEDS" if fired else "within"
    return (f"  - {rule}: z-score rule, threshold={threshold}. Worst sensor{_sensors_note(n_sensors)}: "
            f"mean={mean:.4g}, std={std:.4g}, latest={latest_value:.4g} (at {latest_time}) "
            f"→ z={z:.3g} → {verdict} threshold.{note}")


def _evaluate_windowed(backend, site: str, rule: str, spec: RuleSpec, thresholdjson: str | None,
                       as_of: str | None = None) -> str:
    thresholds = _thresholds_from_json(thresholdjson)
    latest_iso = _query_latest_time(backend, site, spec, before=as_of)
    note = f" ({spec.note})" if spec.note else ""

    if latest_iso is None:
        return (f"  - {rule}: {spec.shape} rule, but no matching readings were found "
                f"to compute the window from.{note}")

    try:
        latest_dt = datetime.fromisoformat(latest_iso)
    except ValueError:
        return f"  - {rule}: could not parse latest timestamp {latest_iso!r} — skipped.{note}"

    metric_values, threshold_values, per_window_desc = [], [], []
    for w in spec.windows:
        start_iso = (latest_dt - _parse_duration(w.duration)).isoformat()
        triples = _query_raw_window(backend, site, spec, start_iso, latest_iso)
        groups = _group_by_sensor(triples)
        thr = thresholds.get(w.threshold_key)
        if not groups or thr is None:
            per_window_desc.append(f"{w.duration} {w.agg}: no data/threshold")
            continue
        per_sensor = {s: v for s, vals in groups.items()
                      if (v := _sensor_stat(vals, w.agg)) is not None}
        combined = _combine_max(per_sensor)
        if combined is None:
            per_window_desc.append(f"{w.duration} {w.agg}: no data")
            continue
        val, _, n_sensors = combined
        metric_values.append(val)
        threshold_values.append(thr)
        per_window_desc.append(f"{w.duration} {w.agg}={val:.4g} (thr {thr:.4g}{_sensors_note(n_sensors)})")

    if not metric_values:
        return (f"  - {rule}: {spec.shape}, but no window produced both a value and a threshold "
                f"[{'; '.join(per_window_desc)}].{note}")

    metric = max(metric_values)
    threshold = max(threshold_values)
    fired = metric > threshold if spec.direction != "lt" else metric < threshold
    verdict = ("EXCEEDS" if spec.direction != "lt" else "BELOW") if fired else "within"
    return (f"  - {rule}: {spec.shape}. Window(s) ending {latest_iso}: {'; '.join(per_window_desc)} "
            f"→ combined metric {metric:.4g} vs threshold {threshold:.4g} → {verdict}.{note}")


def _evaluate_direct(backend, site: str, rule: str, spec: RuleSpec, threshold: float | None,
                     thresholdjson: str | None, as_of: str | None = None) -> str:
    note = f" ({spec.note})" if spec.note else ""
    if threshold is None:
        return (f"  - {rule}: marked as a direct rule but has no single numeric threshold "
                f"on record ({thresholdjson}) — skipped.{note}")

    observations = _query_recent_observations_for_spec(backend, site, spec, RECENT_WINDOW, before=as_of)
    values = [(_to_float(o.get("value")), o.get("time")) for o in observations]
    values = [(v, t) for v, t in values if v is not None]
    values.sort(key=lambda vt: vt[1] or "", reverse=True)

    if not values:
        return (f"  - {rule}: threshold={threshold} ({spec.direction}), but no matching "
                f"recent readings were found to compare against it.{note}")

    latest_value, latest_time = values[0]
    if spec.direction == "lt":
        fired = lambda v: v < threshold
        verdict_word = "BELOW"
    else:
        fired = lambda v: v > threshold
        verdict_word = "EXCEEDS"
    exceed_count = sum(1 for v, _ in values if fired(v))
    verdict = verdict_word if fired(latest_value) else "within"
    return (f"  - {rule}: threshold={threshold} ({spec.direction}). Latest reading = {latest_value} "
            f"(at {latest_time}) → {verdict} threshold. "
            f"{exceed_count}/{len(values)} of the last {len(values)} readings fired.{note}")


# ---------------------------------------------------------------------------
# Custom evaluators — the remaining rule shapes that don't fit a plain
# direct/windowed/zscore comparison. Each groups by sensor first (see note
# above _query_raw_window), computes the metric per sensor, and combines via
# max()/min() across sensors — never by pooling raw values across sensors.
# ---------------------------------------------------------------------------

def _get_threshold_value(threshold: float | None, thresholdjson: str | None, key: str) -> float | None:
    thr_map = _thresholds_from_json(thresholdjson)
    return thr_map.get(key, threshold)


def _custom_step_range_ratio(backend, site, rule, spec, threshold, thresholdjson, as_of: str | None = None) -> str:
    p = spec.custom_params
    note = f" ({spec.note})" if spec.note else ""
    thr = _get_threshold_value(threshold, thresholdjson, p["threshold_key"])
    if thr is None:
        return f"  - {rule}: {spec.shape}, but no threshold on record — skipped.{note}"
    latest_iso = _query_latest_time(backend, site, spec, before=as_of)
    if latest_iso is None:
        return f"  - {rule}: {spec.shape} rule, but no matching readings were found.{note}"
    latest_dt = datetime.fromisoformat(latest_iso)
    short_groups = _group_by_sensor(_query_raw_window(
        backend, site, spec, (latest_dt - _parse_duration(p["short"])).isoformat(), latest_iso))
    long_groups = _group_by_sensor(_query_raw_window(
        backend, site, spec, (latest_dt - _parse_duration(p["long"])).isoformat(), latest_iso))
    per_sensor = {}
    for sensor in set(short_groups) & set(long_groups):
        sr, lr = _sensor_stat(short_groups[sensor], "range"), _sensor_stat(long_groups[sensor], "range")
        if sr is not None and lr is not None:
            per_sensor[sensor] = sr / (lr + 1e-9)
    combined = _combine_max(per_sensor)
    if combined is None:
        return f"  - {rule}: {spec.shape}, but not enough data in the {p['short']}/{p['long']} windows.{note}"
    metric, _, n_sensors = combined
    fired = metric > thr
    verdict = "EXCEEDS" if fired else "within"
    return (f"  - {rule}: {spec.shape}. metric={metric:.4g}{_sensors_note(n_sensors)} "
            f"vs threshold {thr:.4g} → {verdict}.{note}")


def _custom_offset_ratio(backend, site, rule, spec, threshold, thresholdjson, as_of: str | None = None) -> str:
    p = spec.custom_params
    note = f" ({spec.note})" if spec.note else ""
    thr = _get_threshold_value(threshold, thresholdjson, p["threshold_key"])
    if thr is None:
        return f"  - {rule}: {spec.shape}, but no threshold on record — skipped.{note}"
    latest_iso = _query_latest_time(backend, site, spec, before=as_of)
    if latest_iso is None:
        return f"  - {rule}: {spec.shape} rule, but no matching readings were found.{note}"
    latest_dt = datetime.fromisoformat(latest_iso)
    short_groups = _group_by_sensor(_query_raw_window(
        backend, site, spec, (latest_dt - _parse_duration(p["short"])).isoformat(), latest_iso))
    long_groups = _group_by_sensor(_query_raw_window(
        backend, site, spec, (latest_dt - _parse_duration(p["long"])).isoformat(), latest_iso))
    per_sensor = {}
    for sensor in set(short_groups) & set(long_groups):
        short_vals = short_groups[sensor]
        if not short_vals:
            continue
        latest_value = short_vals[-1][0]  # this sensor's own most recent reading in the short window
        short_mean = _sensor_stat(short_vals, "mean")
        long_range = _sensor_stat(long_groups[sensor], "range")
        if short_mean is not None and long_range is not None:
            per_sensor[sensor] = abs(latest_value - short_mean) / (long_range + 1e-9)
    combined = _combine_max(per_sensor)
    if combined is None:
        return f"  - {rule}: {spec.shape}, but not enough data to compute it.{note}"
    metric, _, n_sensors = combined
    fired = metric > thr
    verdict = "EXCEEDS" if fired else "within"
    return (f"  - {rule}: {spec.shape}. metric={metric:.4g}{_sensors_note(n_sensors)} "
            f"vs threshold {thr:.4g} → {verdict}.{note}")


def _custom_peak_ratio(backend, site, rule, spec, threshold, thresholdjson, as_of: str | None = None) -> str:
    p = spec.custom_params
    note = f" ({spec.note})" if spec.note else ""
    thr = _get_threshold_value(threshold, thresholdjson, p["threshold_key"])
    if thr is None:
        return f"  - {rule}: {spec.shape}, but no threshold on record — skipped.{note}"
    latest_iso = _query_latest_time(backend, site, spec, before=as_of)
    if latest_iso is None:
        return f"  - {rule}: {spec.shape} rule, but no matching readings were found.{note}"
    latest_dt = datetime.fromisoformat(latest_iso)
    groups = _group_by_sensor(_query_raw_window(
        backend, site, spec, (latest_dt - _parse_duration(p["window"])).isoformat(), latest_iso))
    per_sensor = {}
    for sensor, vals in groups.items():
        if not vals:
            continue
        baseline = _sensor_stat(vals, "mean")
        if baseline is not None:
            per_sensor[sensor] = vals[-1][0] / (baseline + 1e-9)
    combined = _combine_max(per_sensor)
    if combined is None:
        return f"  - {rule}: {spec.shape}, but not enough data to compute it.{note}"
    metric, _, n_sensors = combined
    fired = metric > thr
    verdict = "EXCEEDS" if fired else "within"
    return (f"  - {rule}: {spec.shape}. ratio={metric:.4g}{_sensors_note(n_sensors)} "
            f"vs threshold {thr:.4g} → {verdict}.{note}")


def _custom_day_over_day_change(backend, site, rule, spec, threshold, thresholdjson, as_of: str | None = None) -> str:
    p = spec.custom_params
    note = f" ({spec.note})" if spec.note else ""
    thr = _get_threshold_value(threshold, thresholdjson, p["threshold_key"])
    if thr is None:
        return f"  - {rule}: {spec.shape}, but no threshold on record — skipped.{note}"
    latest_iso = _query_latest_time(backend, site, spec, before=as_of)
    if latest_iso is None:
        return f"  - {rule}: {spec.shape} rule, but no matching readings were found.{note}"
    latest_dt = datetime.fromisoformat(latest_iso)
    day1_start, day2_start = latest_dt - timedelta(hours=24), latest_dt - timedelta(hours=48)
    groups1 = _group_by_sensor(_query_raw_window(backend, site, spec, day1_start.isoformat(), latest_dt.isoformat()))
    groups2 = _group_by_sensor(_query_raw_window(backend, site, spec, day2_start.isoformat(), day1_start.isoformat()))
    per_sensor = {}
    for sensor in set(groups1) & set(groups2):
        m1, m2 = _sensor_stat(groups1[sensor], "mean"), _sensor_stat(groups2[sensor], "mean")
        if m1 is not None and m2 is not None:
            per_sensor[sensor] = abs(m1 - m2)
    combined = _combine_max(per_sensor)
    if combined is None:
        return f"  - {rule}: {spec.shape}, but not enough data across two trailing 24h windows.{note}"
    metric, _, n_sensors = combined
    fired = metric > thr
    verdict = "EXCEEDS" if fired else "within"
    return (f"  - {rule}: {spec.shape}. |Δ|={metric:.4g}{_sensors_note(n_sensors)} "
            f"vs threshold {thr:.4g} → {verdict}.{note}")


def _custom_rate_of_change(backend, site, rule, spec, threshold, thresholdjson, as_of: str | None = None) -> str:
    p = spec.custom_params
    note = f" ({spec.note})" if spec.note else ""
    thr = _get_threshold_value(threshold, thresholdjson, p["threshold_key"])
    if thr is None:
        return f"  - {rule}: {spec.shape}, but no threshold on record — skipped.{note}"
    latest_iso = _query_latest_time(backend, site, spec, before=as_of)
    if latest_iso is None:
        return f"  - {rule}: {spec.shape} rule, but no matching readings were found.{note}"
    latest_dt = datetime.fromisoformat(latest_iso)
    groups = _group_by_sensor(_query_raw_window(
        backend, site, spec, (latest_dt - _parse_duration(p["window"])).isoformat(), latest_iso))
    per_sensor = {s: v for s, vals in groups.items()
                  if (v := _sensor_stat(vals, "max_abs_diff")) is not None}
    combined = _combine_max(per_sensor)
    if combined is None:
        return (f"  - {rule}: {spec.shape}, but no single sensor had at least 2 readings "
                f"in the {p['window']} window.{note}")
    metric, _, n_sensors = combined
    fired = metric > thr
    verdict = "EXCEEDS" if fired else "within"
    return (f"  - {rule}: {spec.shape}. max |consecutive Δ| over {p['window']} = {metric:.4g}"
            f"{_sensors_note(n_sensors)} vs threshold {thr:.4g} → {verdict}.{note}")


def _custom_airflow_const(backend, site, rule, spec, threshold, thresholdjson, as_of: str | None = None) -> str:
    p = spec.custom_params
    note = f" ({spec.note})" if spec.note else ""
    thr = _get_threshold_value(threshold, thresholdjson, p["threshold_key"])
    if thr is None:
        return f"  - {rule}: {spec.shape}, but no threshold on record — skipped.{note}"
    latest_iso = _query_latest_time(backend, site, spec, before=as_of)
    if latest_iso is None:
        return f"  - {rule}: {spec.shape} rule, but no matching readings were found.{note}"
    latest_dt = datetime.fromisoformat(latest_iso)
    groups = _group_by_sensor(_query_raw_window(
        backend, site, spec, (latest_dt - _parse_duration(p["window"])).isoformat(), latest_iso))
    per_sensor = {s: v for s, vals in groups.items()
                  if (v := _sensor_stat(vals, "max_abs_diff")) is not None}
    # "fires" (suspiciously constant) when the metric is SMALL -> combine via
    # min (the sensor with the smallest max|Δ| is the one AD-RT would score
    # highest for this inverted rule).
    combined = _combine_min(per_sensor)
    if combined is None:
        return (f"  - {rule}: {spec.shape}, but no single sensor had at least 2 readings "
                f"in the {p['window']} window.{note}")
    daily_max_diff, _, n_sensors = combined
    half_thr = thr / 2
    fired = daily_max_diff < half_thr  # inverted formula — see custom_params note
    verdict = "FIRES (suspiciously constant)" if fired else "within (normal variability)"
    sensors_note = f" (min across {n_sensors} sensor(s))" if n_sensors > 1 else ""
    return (f"  - {rule}: {spec.shape}. max |consecutive Δ| = {daily_max_diff:.4g}{sensors_note} "
            f"vs threshold/2 = {half_thr:.4g} → {verdict}.{note}")


def _custom_two_col_closeness(backend, site, rule, spec, threshold, thresholdjson, as_of: str | None = None) -> str:
    p = spec.custom_params
    note = f" ({spec.note})" if spec.note else ""
    thr = _get_threshold_value(threshold, thresholdjson, p["threshold_key"])
    if thr is None:
        return f"  - {rule}: {spec.shape}, but no threshold on record — skipped.{note}"
    spec_b = RuleSpec(False, any_of=spec.second_any_of, all_of=spec.second_all_of)
    rows_a = _query_recent_observations_for_spec(backend, site, spec, 1, before=as_of)
    rows_b = _query_recent_observations_for_spec(backend, site, spec_b, 1, before=as_of)
    if not rows_a or not rows_b:
        return f"  - {rule}: {spec.shape}, but one or both quantities have no matching data.{note}"
    va, vb = _to_float(rows_a[0].get("value")), _to_float(rows_b[0].get("value"))
    if va is None or vb is None:
        return f"  - {rule}: {spec.shape}, but could not parse both readings.{note}"
    diff = abs(va - vb)
    half_thr = thr / 2
    fired = diff < half_thr  # inverted formula — see custom_params note
    verdict = "FIRES (suspiciously close)" if fired else "within (normal difference)"
    return (f"  - {rule}: {spec.shape}. |{va:.4g} - {vb:.4g}| = {diff:.4g} vs threshold/2 = {half_thr:.4g} "
            f"(at {rows_a[0].get('time')} / {rows_b[0].get('time')}) → {verdict}.{note}")


def _custom_two_col_composite(backend, site, rule, spec, threshold, thresholdjson, as_of: str | None = None) -> str:
    p = spec.custom_params
    note = f" ({spec.note})" if spec.note else ""
    thresholds = _thresholds_from_json(thresholdjson)
    thr_t, thr_h = thresholds.get(p["t_key"]), thresholds.get(p["h_key"])
    if thr_t is None or thr_h is None:
        return (f"  - {rule}: {spec.shape}, but thresholds for both quantities are not on record "
                f"({thresholdjson}).{note}")
    spec_h = RuleSpec(False, any_of=spec.second_any_of, all_of=spec.second_all_of)
    rows_t = _query_recent_observations_for_spec(backend, site, spec, 1, before=as_of)
    rows_h = _query_recent_observations_for_spec(backend, site, spec_h, 1, before=as_of)
    if not rows_t or not rows_h:
        return f"  - {rule}: {spec.shape}, but one or both quantities have no matching data.{note}"
    t, h = _to_float(rows_t[0].get("value")), _to_float(rows_h[0].get("value"))
    if t is None or h is None:
        return f"  - {rule}: {spec.shape}, but could not parse both readings.{note}"
    fired = (t < thr_t) and (h > thr_h)
    verdict = "FIRES" if fired else "within"
    return (f"  - {rule}: {spec.shape}. temp={t:.4g} (thr<{thr_t:.4g}), hum={h:.4g} (thr>{thr_h:.4g}) "
            f"(at {rows_t[0].get('time')} / {rows_h[0].get('time')}) → {verdict}.{note}")


CUSTOM_EVALUATORS = {
    "step_range_ratio": _custom_step_range_ratio,
    "offset_ratio": _custom_offset_ratio,
    "peak_ratio": _custom_peak_ratio,
    "day_over_day_change": _custom_day_over_day_change,
    "rate_of_change": _custom_rate_of_change,
    "airflow_const": _custom_airflow_const,
    "two_col_closeness": _custom_two_col_closeness,
    "two_col_composite": _custom_two_col_composite,
}


def evaluate(backend, intent: dict) -> dict[str, Any]:
    """Returns {"summary_text": str}. Empty string when the intent carries no
    recognisable site+quantity pair — the caller should skip this section then,
    same convention as geo_analysis.analyze()'s per-section omission."""
    site, keyword = extract_context(intent)
    if not site or not keyword:
        return {"summary_text": ""}

    as_of = extract_as_of(intent)

    policies = _query_policies(backend, site, keyword)
    if not policies:
        return {"summary_text": (
            f"AD-RT rule check: no expert-rule policy found for site={site!r} "
            f"matching quantity {keyword!r} — this cannot be assessed against a "
            f"known AD-RT threshold."
        )}

    as_of_desc = f", as of {as_of}" if as_of else ""
    lines = [f"AD-RT rule check for site={site!r}, quantity~{keyword!r}{as_of_desc} "
             f"(computed here, not by the model):"]
    for p in policies:
        rule = p.get("ruleid") or p.get("label")
        threshold = _to_float(p.get("threshold"))
        spec = RULE_SPECS.get((site, rule))

        if spec is None:
            lines.append(f"  - {rule}: unrecognised rule id — not in the AD-RT rule table used here, "
                         f"not evaluated numerically.")
        elif spec.windows:
            lines.append(_evaluate_windowed(backend, site, rule, spec, p.get("thresholdjson"), as_of=as_of))
        elif spec.zscore:
            lines.append(_evaluate_zscore(backend, site, rule, spec, threshold, p.get("thresholdjson"), as_of=as_of))
        elif spec.custom:
            lines.append(CUSTOM_EVALUATORS[spec.custom](
                backend, site, rule, spec, threshold, p.get("thresholdjson"), as_of=as_of))
        elif spec.direct:
            lines.append(_evaluate_direct(backend, site, rule, spec, threshold, p.get("thresholdjson"), as_of=as_of))
        else:
            thr_display = threshold if threshold is not None else p.get("thresholdjson")
            note = f" ({spec.note})" if spec.note else ""
            lines.append(f"  - {rule}: threshold={thr_display}, but this rule is a "
                         f"{spec.shape} — not a direct reading-vs-threshold comparison, "
                         f"so it is not evaluated numerically here, only the definition is known.{note}")

    return {"summary_text": "\n".join(lines)}
