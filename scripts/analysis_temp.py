"""
Temporal layer: what time means in this system, in one place.

  - Time filters: the semantics of from/until/after/before on resultTime
    (bare dates are whole UTC days) and of per-day/per-month buckets — used by
    the query compiler (2_sparql_retriever.py) when it writes the SPARQL.
  - Relative windows ("last 24 hours") end at the latest reading in the
    knowledge graph, not at the wall clock; a window wholly outside the
    readings is declined instead of answered with a confident 0.
  - Temporal facts of a result set (newest/oldest timestamp, span, recency),
    part of the pre-computed analysis the answer is written from.
  - What the parser and the answer generator are told about all of this
    (PARSER_* and ANSWER_GUIDE), so the LLM is told what this code does.
"""

from __future__ import annotations
import json
import re
from datetime import date, datetime, timedelta, timezone
from typing import Any, Callable

TIME_OPS = ("after", "before", "from", "until")
TIME_BUCKETS = {"day": 10, "month": 7}   # length of the ISO prefix that names the bucket
TIME_CLASSES = ("ObservationCollection", "Observation")   # the classes that carry resultTime
_DATE_ONLY = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_REL_HOURS = {"hour": 1, "hours": 1, "day": 24, "days": 24, "week": 168, "weeks": 168}
_MAX_RECENCY_ROWS = 20


# ── Time filters (used by the query compiler) ────────────────────────────────

def time_bounds(op: str, val) -> tuple[str, str]:
    """A time filter as (comparison, value) on the endpoint's lexical form
    (2026-06-30T23:45:00+00:00), which compares correctly as a string.
    A bare date names a whole UTC day: "from" and "until" include it, so
    "in August" is from 08-01 until 08-31. "after"/"before" a bare date are
    read the way the parser writes them for periods — "after 2026-08-01" for
    a range that starts on 08-01 (88 of 93 such filters in our runs), "before
    2026-09-01" for one that ends on 08-31 — i.e. as >= and < that day.
    A datetime is a point: from/after are >= / >, until/before are <= / < —
    except "after <day>T00:00:00", which means from the start of that day."""
    v = str(val).strip()
    if _DATE_ONLY.match(v):
        d = date.fromisoformat(v)
        if op == "until":
            return "<", (d + timedelta(days=1)).isoformat()
        return (">=" if op in ("from", "after") else "<"), d.isoformat()
    m = re.match(r"^(\d{4}-\d{2}-\d{2})[T ](\d{2}:\d{2})(:\d{2})?(\.\d+)?(Z|[+-]\d{2}:?\d{2})?$", v)
    if not m:
        return {"after": ">", "before": "<", "from": ">=", "until": "<="}[op], v
    day, hm, sec, frac, tz = m.groups()
    v = f"{day}T{hm}{sec or ':00'}{frac or ''}{'+00:00' if tz in (None, 'Z') else tz}"
    if op == "after" and f"{hm}{sec or ':00'}" == "00:00:00" and not frac:
        return ">=", v
    return {"after": ">", "before": "<", "from": ">=", "until": "<="}[op], v


def bucket_bind(time_var: str, bucket: str) -> str:
    """The SPARQL that names a reading's UTC day/month: the ISO prefix of its
    resultTime (lexical form 2026-06-30T23:45:00+00:00, i.e. UTC)."""
    return f"BIND(SUBSTR(STR({time_var}), 1, {TIME_BUCKETS[bucket]}) AS ?{bucket})"


# ── Windows: relative to the latest reading, and against the data's range ────

def iso(t: datetime) -> str:
    # Same lexical form as the endpoint's xsd:dateTime values, so the string
    # comparison the "after"/"before" filters compile to stays correct.
    return t.astimezone(timezone.utc).isoformat()


def fmt(t: datetime) -> str:
    return t.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def apply_relative_time(intent: dict, latest: datetime | None):
    """A relative window ("last 24 hours") ends at the latest reading in the KG,
    not at the wall clock: turn the parser's relative_time into an absolute
    resultTime filter. Returns (intent, (start, end) or None, problem or None)."""
    rt = intent.get("relative_time")
    if not rt or intent.get("anomaly_check") or latest is None:
        return intent, None, None
    try:
        hours = float(rt.get("amount")) * _REL_HOURS[str(rt.get("unit", "")).lower()]
    except (AttributeError, KeyError, TypeError, ValueError):
        return intent, None, (f"Invalid relative_time {rt!r}; use {{\"amount\": <integer>, "
                              f"\"unit\": \"hours|days|weeks\"}}.")
    start = latest - timedelta(hours=hours)
    flt = {"property": "resultTime", "op": "after", "value": iso(start)}
    intent = json.loads(json.dumps(intent))
    if intent.get("target_class") in TIME_CLASSES:
        intent.setdefault("filters", []).append(flt)
    else:
        j = next((j for j in intent.get("joins") or [] if j.get("class") in TIME_CLASSES), None)
        if j is None:
            return intent, None, ("relative_time needs readings: join ObservationCollection "
                                  "(it carries resultTime) or target it directly.")
        j.setdefault("filters", []).append(flt)
    return intent, (start, latest), None


def time_filters(intent: dict | None) -> list[dict]:
    fs = [*((intent or {}).get("filters") or []),
          *[f for j in (intent or {}).get("joins") or [] for f in j.get("filters") or []]]
    return [f for f in fs if str(f.get("property", "")).lower().endswith("resulttime") and f.get("op") in TIME_OPS]


def requested_window(intent: dict | None):
    """The resultTime window the intent's filters ask for, as ((cmp, bound) or
    None, (cmp, bound) or None) in the endpoint's lexical form; bare dates are
    resolved the way the compiler resolves them."""
    lo = hi = None
    for f in time_filters(intent):
        cmp, bound = time_bounds(f["op"], f.get("value"))
        if cmp in (">", ">="):
            lo = max(lo, (cmp, bound), key=lambda b: b[1]) if lo else (cmp, bound)
        else:
            hi = min(hi, (cmp, bound), key=lambda b: b[1]) if hi else (cmp, bound)
    return lo, hi


def outside_data(intent: dict | None, earliest: datetime | None, latest: datetime | None) -> str | None:
    """A decline when the requested window lies wholly outside the readings in
    the KG — a count over it would otherwise come back as a confident 0."""
    if not intent or intent.get("anomaly_check") or not earliest or not latest:
        return None
    lo, hi = requested_window(intent)
    first, last = iso(earliest), iso(latest)
    if (lo and (lo[1] > last or (lo[0] == ">" and lo[1] >= last))) or \
       (hi and (hi[1] < first or (hi[0] == "<" and hi[1] <= first))):
        return (f"Cannot be answered: the knowledge graph has readings from {fmt(earliest)} to "
                f"{fmt(latest)}, and the period the question asks about lies outside that range.")
    return None


def data_note(intent: dict | None, latest: datetime | None, window) -> str:
    """Which data the answer rests on — appended to every answer, so it always
    states the timestamp of the data used rather than leaving it to the model."""
    if window:
        return f"(Data: readings from {fmt(window[0])} to {fmt(window[1])}.)"
    if intent and intent.get("anomaly_check") and intent.get("as_of"):
        return f"(Data: readings up to {intent['as_of']}, the date the question names.)"
    lo, hi = requested_window(intent)
    if lo or hi:
        return (f"(Data: readings{' from ' + lo[1] if lo else ''}"
                f"{' up to ' + ('and including ' if hi[0] == '<=' else '') + hi[1] if hi else ''}.)")
    if latest is not None:
        return f"(Data: readings up to {fmt(latest)}, the latest in the knowledge graph.)"
    return ""


# ── Temporal facts of a result set (part of the pre-computed analysis) ───────

def _parse_dt(v: str) -> datetime | None:
    if not v:
        return None
    s = v.strip().replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(s)
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _extract_time(row: dict) -> datetime | None:
    for k in row:
        if "time" in k.lower() or "date" in k.lower():
            dt = _parse_dt(str(row.get(k) or ""))
            if dt:
                return dt
    return None


def temporal_facts(results: list[dict[str, Any]], now: datetime,
                   row_label: Callable[[dict], str]) -> tuple[list[dict], list[str]]:
    """(recency, summary lines): every timestamped row newest first, with its
    age relative to `now` (the latest reading in the KG), and the newest/oldest
    timestamp and span of the result set."""
    timed = []
    for row in results:
        ts = _extract_time(row)
        timed.append((ts, row))
    with_time = sorted((t for t in timed if t[0] is not None),
                       key=lambda t: t[0], reverse=True)

    recency = [
        {"label": row_label(r), "timestamp": ts.isoformat(),
         "days_ago": (now - ts).days}
        for ts, r in with_time
    ]
    lines = []
    if recency:
        span_new = with_time[0][0]
        span_old = with_time[-1][0]
        lines.append(f"\n=== Temporal ({len(recency)} timestamped rows) ===")
        lines.append(f"  newest: {span_new.isoformat()}")
        lines.append(f"  oldest: {span_old.isoformat()}")
        lines.append(f"  span:   {span_new - span_old}")
        lines.append("  most recent first:")
        for r in recency[:_MAX_RECENCY_ROWS]:
            lines.append(f"    {r['label']:40s}  {r['timestamp']}")
        if len(recency) > _MAX_RECENCY_ROWS:
            lines.append(f"    … and {len(recency) - _MAX_RECENCY_ROWS} more")
    return recency, lines


# ── What the parser and the answer generator are told about this layer ───────

PARSER_OPERATORS = """\
  from      — resultTime on or after the value; a bare date (2025-01-10) means from the start of that day
  until     — resultTime on or before the value; a bare date (2025-01-16) INCLUDES that whole day
  after     — resultTime after the value (a bare date: from the start of that day)
  before    — resultTime before the value (a bare date: up to the start of that day, excluding it)"""

PARSER_GUIDE = """\
  - Time periods are resultTime filters, written with bare dates and from/until, both ends inclusive:
      "on 2025-03-04"                 → from 2025-03-04, until 2025-03-04
      "in February 2025"              → from 2025-02-01, until 2025-02-28
      "between 2025-01-10 and 01-16"  → from 2025-01-10, until 2025-01-16
    Use after/before only for "after"/"before" a point in time. Every question that names a day, month or
    period MUST carry these filters — without them the statistic runs over all data.
  - "relative_time": set for a window that ends now ("in the last 24 hours", "over the past 7 days", "this past week" = 1 week). "Now" is the latest reading in the knowledge graph (given with the query as the reference time), not today's date; the window is turned into a resultTime filter downstream, so do NOT also add resultTime filters for it. Null otherwise.
  - WHICH DAY / MONTH has the highest or lowest daily/monthly statistic ("on which day was the mean humidity lowest"): aggregate per period with "time_bucket": "day" (or "month"), group_by null, order_by the aggregate with limit 1 — each row is then one day with its statistic."""

PARSER_EXAMPLES = """\
Q: "How many temperature observations were made at ranverso in February 2025?"
{
  "target_class": "ObservationCollection",
  "filters": [{"property": "resultTime", "op": "from", "value": "2025-02-01"},
              {"property": "resultTime", "op": "until", "value": "2025-02-28"}],
  "return_properties": [],
  "joins": [
    {"class": "Observation", "via": "hasObservation", "direction": "outgoing",
     "return_properties": [], "filters": []},
    {"class": "ObservedProperty", "via": "observedProperty", "direction": "outgoing",
     "return_properties": [], "filters": [{"property": "label", "op": "equals", "value": "temperature"}]},
    {"class": "Site", "via": "hasSite", "direction": "outgoing",
     "return_properties": [], "filters": [{"property": "label", "op": "equals", "value": "ranverso"}]}
  ],
  "aggregation": {"type": "count", "group_by": null, "target": "observation", "distinct": true},
  "order_by": null, "limit": null,
  "anomaly_check": false,
  "as_of": null,
  "explanation": "A calendar month is from its first to its last day, both inclusive."
}

Q: "In which month of 2025 was the mean soil temperature at lucretili lowest?"
{
  "target_class": "ObservationCollection",
  "filters": [{"property": "resultTime", "op": "from", "value": "2025-01-01"},
              {"property": "resultTime", "op": "until", "value": "2025-12-31"}],
  "return_properties": [],
  "joins": [
    {"class": "Observation", "via": "hasObservation", "direction": "outgoing",
     "return_properties": [], "filters": []},
    {"class": "ObservedProperty", "via": "observedProperty", "direction": "outgoing",
     "return_properties": [], "filters": [{"property": "label", "op": "equals", "value": "soil_temperature"}]},
    {"class": "Site", "via": "hasSite", "direction": "outgoing",
     "return_properties": [], "filters": [{"property": "label", "op": "equals", "value": "lucretili"}]}
  ],
  "aggregation": {"type": "avg", "group_by": null, "time_bucket": "month", "target": "hasSimpleResult", "distinct": false},
  "order_by": {"variable": "avg", "direction": "ASC"}, "limit": 1,
  "anomaly_check": false,
  "as_of": null,
  "explanation": "One mean per UTC month of 2025, ranked lowest first; the top row is the month and its mean."
}

Q: "How many readings were recorded at ranverso in the last 48 hours?"
{
  "target_class": "ObservationCollection",
  "filters": [],
  "return_properties": [],
  "joins": [
    {"class": "Site", "via": "hasSite", "direction": "outgoing",
     "return_properties": [], "filters": [{"property": "label", "op": "equals", "value": "ranverso"}]}
  ],
  "aggregation": {"type": "count", "group_by": null, "target": "observationcollection", "distinct": true},
  "order_by": null, "limit": null,
  "anomaly_check": false,
  "as_of": null,
  "relative_time": {"amount": 48, "unit": "hours"},
  "explanation": "A window ending at the latest reading; it becomes a resultTime filter downstream, so no date is written here."
}"""

ANSWER_GUIDE = """\
Time:
- For "when" questions give the timestamp from the results to the minute."""
