"""
Step 1 — NL query + ontology schema → structured intent JSON naming the
SOSA/ARGUS classes and properties needed. Prior turns may be passed as history
so follow-up questions resolve against them.
"""

from __future__ import annotations
import json
import os
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI
from ontology_schema import get_ontology_schema, extract_class_list

BASE_URL = os.environ.get("OLLAMA_BASE_URL", "https://ollama.fit.fraunhofer.de/api")
API_KEY  = os.environ.get("OPENAI_API_KEY", "no-key")
MODEL    = os.environ.get("OLLAMA_MODEL", "llama3.3:70b")

# The SDK default is a 600s timeout with silent retries, so a stalled endpoint
# hangs the pipeline for many minutes with no output.
LLM_TIMEOUT     = float(os.environ.get("ARGUS_LLM_TIMEOUT", "120"))
LLM_MAX_RETRIES = int(os.environ.get("ARGUS_LLM_MAX_RETRIES", "2"))

ONTOLOGY_SCHEMA = get_ontology_schema()

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        http_client = None
        # Temporary escape hatch for an expired cert on the remote endpoint —
        # unset/false keeps normal verification. Never enable this by default.
        insecure = os.environ.get("ARGUS_OPENAI_COMPATIBLE_INSECURE_SSL", "").strip().lower() in {"1", "true", "yes", "on"}
        if insecure:
            import httpx
            http_client = httpx.Client(verify=False)
        _client = OpenAI(
            base_url=BASE_URL, api_key=API_KEY,
            timeout=LLM_TIMEOUT, max_retries=LLM_MAX_RETRIES,
            http_client=http_client,
        )
    return _client

_GRAPH_PATHS = """\
Key graph paths (direct edges — use these for joins):
  ObservationCollection —[hasSite]→       Site
  ObservationCollection —[madeBySensor]→  Sensor
  ObservationCollection —[hasObservation]→ Observation
  ObservationCollection —[hasNode]→       Node
  Observation           —[observedProperty]→ ObservedProperty

Multi-hop paths (always route through ALL intermediates in order):
  Sensor        ↔ Site            : Sensor ←[madeBySensor]← ObservationCollection —[hasSite]→ Site
  ObservedProperty ↔ Site         : ObservedProperty ←[observedProperty]← Observation ←[hasObservation]← ObservationCollection —[hasSite]→ Site
  ObservedProperty ↔ Sensor       : ObservedProperty ←[observedProperty]← Observation ←[hasObservation]← ObservationCollection —[madeBySensor]→ Sensor

Node geo-location (datatype properties on Node; currently populated for baltanas only):
  Node.latitude    (decimal degrees, WGS84)
  Node.longitude   (decimal degrees, WGS84)
  Node.altitude    (metres)
  For location/distance/elevation questions, return these Node properties. Distances,
  nearest/farthest pairs, centroid and spread are computed downstream from the
  coordinates — you only need to RETURN latitude/longitude/altitude, not compute them.

Variable naming rule: the SPARQL variable for a join's return property is {ClassName}_{property}.
  Site.label → ?site_label        Observation.hasSimpleResult → ?observation_hassimpleresult
  Use this exact dotted form in group_by and order_by fields.

Governance graph (expert-rule thresholds and pilot metadata — separate from the
sensor-reading graph above, joined to it only through Site):
  Policy   —[appliesToSite]→  Site     (policyDescription, ruleId, threatName, thresholdValue, thresholdJson)
  Asset    —[atSite]→        Site     (assetDescription, assetCode, pilotNumber, country, sourceUrl)
  Threat   (threatDescription, threatLevel) — standalone, not yet linked to Policy/Asset by ID.
  Decision (decisionDescription, urgency) — standalone, not linked to Policy/Asset/Threat by ID.
  thresholdValue is only set when a rule has exactly one threshold parameter; multi-parameter
  rules (e.g. "R3_hum_cross": {"R3_hum_th": 75, "R3_cross": 9}) carry thresholdJson instead —
  do not attempt to filter/aggregate on thresholdJson's contents, only return it as-is.\
"""

_FEW_SHOT = """\
--- EXAMPLES ---

Q: "What are the temperature values recorded at each site?"
{
  "target_class": "ObservationCollection",
  "filters": [],
  "return_properties": [],
  "joins": [
    {"class": "Observation", "via": "hasObservation", "direction": "outgoing",
     "return_properties": ["hasSimpleResult"], "filters": []},
    {"class": "ObservedProperty", "via": "observedProperty", "direction": "outgoing",
     "return_properties": [], "filters": [{"property": "label", "op": "contains", "value": "temperature"}]},
    {"class": "Site", "via": "hasSite", "direction": "outgoing",
     "return_properties": ["label"], "filters": []}
  ],
  "aggregation": null,
  "order_by": null, "limit": null,
  "anomaly_check": false,
  "as_of": null,
  "explanation": "Lists the individual values, so no aggregation — contrast with 'average temperature', which must aggregate."
}

Q: "What is the average temperature at each site?"
{
  "target_class": "ObservationCollection",
  "filters": [],
  "return_properties": [],
  "joins": [
    {"class": "Observation", "via": "hasObservation", "direction": "outgoing",
     "return_properties": [], "filters": []},
    {"class": "ObservedProperty", "via": "observedProperty", "direction": "outgoing",
     "return_properties": [], "filters": [{"property": "label", "op": "equals", "value": "temperature"}]},
    {"class": "Site", "via": "hasSite", "direction": "outgoing",
     "return_properties": ["label"], "filters": []}
  ],
  "aggregation": {"type": "avg", "group_by": "Site.label",
                  "target": "hasSimpleResult", "distinct": false},
  "order_by": null, "limit": null,
  "anomaly_check": false,
  "as_of": null,
  "explanation": "AVG computed in the query over every observation, so de-duplication of detail rows cannot skew it."
}

Q: "How many sensors are deployed per site?"
{
  "target_class": "ObservationCollection",
  "filters": [],
  "return_properties": [],
  "joins": [
    {"class": "Sensor", "via": "madeBySensor", "direction": "outgoing",
     "return_properties": [], "filters": []},
    {"class": "Site", "via": "hasSite", "direction": "outgoing",
     "return_properties": ["label"], "filters": []}
  ],
  "aggregation": {"type": "count", "group_by": "Site.label",
                  "target": "sensor", "distinct": true},
  "order_by": null, "limit": null,
  "anomaly_check": false,
  "as_of": null,
  "explanation": "Count distinct sensors per site."
}

Q: "What are the latest 10 readings?"
{
  "target_class": "Observation",
  "filters": [],
  "return_properties": ["hasSimpleResult"],
  "joins": [
    {"class": "ObservationCollection", "via": "hasObservation", "direction": "incoming",
     "return_properties": ["resultTime"], "filters": []},
    {"class": "Site", "via": "hasSite", "direction": "outgoing",
     "return_properties": ["label"], "filters": []}
  ],
  "aggregation": null,
  "order_by": {"variable": "ObservationCollection.resultTime", "direction": "DESC"},
  "limit": 10,
  "anomaly_check": false,
  "as_of": null,
  "explanation": "10 most recent individual readings (Observations), ranked by their collection's resultTime so LIMIT counts readings, not collections."
}

Q: "Which physical quantities are measured at the delos site?"
{
  "target_class": "ObservationCollection",
  "filters": [],
  "return_properties": [],
  "joins": [
    {"class": "Site", "via": "hasSite", "direction": "outgoing",
     "return_properties": [], "filters": [{"property": "label", "op": "equals", "value": "delos"}]},
    {"class": "Observation", "via": "hasObservation", "direction": "outgoing",
     "return_properties": [], "filters": []},
    {"class": "ObservedProperty", "via": "observedProperty", "direction": "outgoing",
     "return_properties": ["label"], "filters": []}
  ],
  "aggregation": null,
  "order_by": null,
  "limit": null,
  "anomaly_check": false,
  "as_of": null,
  "explanation": "Forward-traverse from ObservationCollection to Site (filtered) → Observation → ObservedProperty to list distinct measured quantities."
}

Q: "Where are the sensor nodes at the baltanas site?"
{
  "target_class": "Node",
  "filters": [],
  "return_properties": ["label", "latitude", "longitude", "altitude"],
  "joins": [
    {"class": "ObservationCollection", "via": "hasNode", "direction": "incoming",
     "return_properties": [], "filters": []},
    {"class": "Site", "via": "hasSite", "direction": "outgoing",
     "return_properties": [], "filters": [{"property": "label", "op": "equals", "value": "baltanas"}]}
  ],
  "aggregation": null,
  "order_by": null,
  "limit": null,
  "anomaly_check": false,
  "as_of": null,
  "explanation": "List baltanas nodes with their coordinates; spatial metrics are derived downstream from lat/long/altitude."
}

Q: "among these sensors, how many are about temperature?"
   (follow-up; the previous turn asked "how many sensors are in baltanas?" and returned 28 sensors)
   Inherit the set definition — target_class=Sensor plus the baltanas Site filter — then ADD the
   ObservedProperty constraint. The previous rows held no property information, so the new joins
   are required.
{
  "target_class": "Sensor",
  "filters": [],
  "return_properties": [],
  "joins": [
    {"class": "ObservationCollection", "via": "madeBySensor", "direction": "incoming",
     "return_properties": [], "filters": []},
    {"class": "Site", "via": "hasSite", "direction": "outgoing",
     "return_properties": [], "filters": [{"property": "label", "op": "equals", "value": "baltanas"}]},
    {"class": "Observation", "via": "hasObservation", "direction": "outgoing",
     "return_properties": [], "filters": []},
    {"class": "ObservedProperty", "via": "observedProperty", "direction": "outgoing",
     "return_properties": [], "filters": [{"property": "label", "op": "contains", "value": "temperature"}]}
  ],
  "aggregation": {"type": "count", "group_by": null, "target": "sensor", "distinct": true},
  "order_by": null,
  "limit": null,
  "anomaly_check": false,
  "as_of": null,
  "explanation": "Count baltanas sensors (inherited set) that observe temperature (added constraint)."
}

Q: "What is the rainfall alarm threshold at delos?"
{
  "target_class": "Policy",
  "filters": [{"property": "ruleId", "op": "contains", "value": "rain"}],
  "return_properties": ["policyDescription", "ruleId", "thresholdValue", "thresholdJson"],
  "joins": [
    {"class": "Site", "via": "appliesToSite", "direction": "outgoing",
     "return_properties": ["label"], "filters": [{"property": "label", "op": "equals", "value": "delos"}]}
  ],
  "aggregation": null,
  "order_by": null, "limit": null,
  "anomaly_check": false,
  "as_of": null,
  "explanation": "Wants the threshold definition, not a verdict, so Policy is the right target_class and anomaly_check stays false."
}

Q: "Has the temperature range at lucretili exceeded its AD-RT threshold?"
{
  "target_class": "Policy",
  "filters": [{"property": "ruleId", "op": "contains", "value": "temp"}],
  "return_properties": ["policyDescription", "ruleId", "thresholdValue", "thresholdJson"],
  "joins": [
    {"class": "Site", "via": "appliesToSite", "direction": "outgoing",
     "return_properties": ["label"], "filters": [{"property": "label", "op": "equals", "value": "lucretili"}]}
  ],
  "aggregation": null,
  "order_by": null, "limit": null,
  "anomaly_check": true,
  "as_of": null,
  "explanation": "Retrieve the applicable AD-RT rule(s) and their thresholds first (target_class=Policy) — the same as a pure threshold lookup. anomaly_check=true tells the pipeline to follow up with a separate deterministic step (outside this JSON) that runs each retrieved rule's own windowed/per-sensor Observation queries and compares against these thresholds; do NOT try to also join or aggregate Observation data yourself here."
}

Q: "Was the temperature range at lucretili anomalous on 2026-05-15?"
{
  "target_class": "Policy",
  "filters": [{"property": "ruleId", "op": "contains", "value": "temp"}],
  "return_properties": ["policyDescription", "ruleId", "thresholdValue", "thresholdJson"],
  "joins": [
    {"class": "Site", "via": "appliesToSite", "direction": "outgoing",
     "return_properties": ["label"], "filters": [{"property": "label", "op": "equals", "value": "lucretili"}]}
  ],
  "aggregation": null,
  "order_by": null, "limit": null,
  "anomaly_check": true,
  "as_of": "2026-05-15",
  "explanation": "Same Policy lookup as any anomaly_check question — the date is NOT a filter here (Policy has no resultTime), it goes in as_of so the deterministic step checks the rule against readings as of that day instead of the latest available."
}

Q: "Which country is the Lucretili pilot in, and what threats affect it?"
{
  "target_class": "Asset",
  "filters": [{"property": "label", "op": "contains", "value": "Lucretili"}],
  "return_properties": ["label", "country", "assetDescription"],
  "joins": [],
  "aggregation": null,
  "order_by": null, "limit": null,
  "anomaly_check": false,
  "as_of": null,
  "explanation": "Asset carries the pilot's country. Threat has no ID-based link to a specific Asset in this data, so it cannot be joined here — a separate Threat query is needed if the user wants that list."
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
}

--- END EXAMPLES ---\
"""

PARSE_SYSTEM = f"""You are a semantic parser for an ARGUS knowledge graph.

Given a natural-language query, output ONLY a valid JSON object (no markdown fences)
with this exact schema:

{{
  "target_class": "<class name, one of: {extract_class_list()}>",
  "filters": [
    {{"property": "<property>", "op": "contains|equals|gt|lt|after|before", "value": "<string>"}}
  ],
  "return_properties": ["<list of properties to SELECT>"],
  "joins": [
    {{
      "class": "<related class>",
      "via": "<property name>",
      "direction": "outgoing|incoming",
      "return_properties": ["<properties of the related class>"],
      "filters": [
        {{"property": "<property>", "op": "contains|equals|gt|lt|after|before", "value": "<string>"}}
      ]
    }}
  ],
  "aggregation": null or {{"type": "count|min|max|avg|sum", "group_by": "ClassName.property", "target": "<class or property>", "distinct": true|false}},
  "order_by": null or {{"variable": "ClassName.property", "direction": "ASC|DESC"}},
  "limit": null or <integer>,
  "anomaly_check": true|false,
  "as_of": null or "<ISO date or datetime, e.g. '2026-05-15'>",
  "relative_time": null or {{"amount": <integer>, "unit": "hours|days|weeks"}},
  "explanation": "<one sentence>"
}}

Operator guide:
  contains  — case-insensitive substring match on string literals
  equals    — exact case-insensitive match
  gt / lt   — numeric comparison (for measured values)
  after     — datetime is after the given ISO value (for resultTime)
  before    — datetime is before the given ISO value

{_GRAPH_PATHS}

Rules:
  - Use only class names and property names from the ontology schema.
  - Only include in return_properties the fields that directly answer the question. Do not include internal metadata (deviceGroupId, readingType, sensorId, sensorModel, etc.) unless the user explicitly asked for them.
  - Always include label in return_properties for classes that have it (Site, ObservedProperty, Sensor, Node).
  - Always include hasSimpleResult in return_properties when querying measured values.
  - For time-based queries use resultTime with after/before operators.
  - direction="outgoing" means the subject (anchor) → via → object (join class).  direction="incoming" means object (join class) → via → subject (anchor).
  - For COUNT aggregations: set "target" to the class name in lowercase (e.g. "sensor"), distinct=true. For min/max/avg/sum: set "target" to the property name (e.g. "hasSimpleResult"), distinct=false.
  - AGGREGATE FIRST — this is a correctness rule, not an optimisation. If the question asks for a statistic ("average", "mean", "total", "sum", "how many", "highest", "lowest", "maximum", "minimum"), you MUST set "aggregation" so the statistic is computed inside the query. Detail rows go through DISTINCT de-duplication, so any average, sum or count derived from them afterwards is WRONG (measured: 15% error on an average). Only omit "aggregation" when the user genuinely wants the individual values listed.
  - When aggregating on a property, put it in "aggregation.target" only — it does not also need to be in return_properties. Set group_by to null for a single overall figure, or to "ClassName.property" for a per-group breakdown.
  - group_by and order_by variables MUST use the dotted "ClassName.property" form (e.g. "Site.label", "ObservationCollection.resultTime"). The join for that class MUST be present and include the property in return_properties.
  - When asking to LIST instances of a class (e.g. "which sensors", "what sites"), set target_class to that class directly and join ObservationCollection as needed for filtering — EXCEPT for "what quantities/properties are measured/observed at site X": use target_class=ObservationCollection and forward-join Site (filtered), Observation, ObservedProperty (as shown in example 5).
  - The property "readingType" holds data-format codes ("reading", "eng_units") — NOT physical measurement types. To filter by measurement type (temperature, humidity, etc.), filter on ObservedProperty.label via the hasObservation → observedProperty chain.
  - "latest/most recent N readings/values/measurements": one reading = one Observation, so set target_class=Observation (NOT ObservationCollection) and limit=N; join ObservationCollection via hasObservation (incoming) returning resultTime, and order_by ObservationCollection.resultTime DESC. This makes LIMIT count individual readings. (A timestamp lives on the ObservationCollection, so reach it through that join.)
  - Location/where/distance/nearest/elevation questions: set target_class=Node and return_properties=["label","latitude","longitude","altitude"]; link to a Site by joining ObservationCollection via hasNode (incoming) then Site via hasSite (outgoing, filtered). Do NOT try to compute distances/centroids in the query — just return the coordinates; the analysis layer computes spatial metrics.
  - "anomaly_check": true only for a yes/no verdict against a known threshold ("has X exceeded threshold", "is there an anomaly"). False for a plain "what is the threshold for X" lookup, which wants the definition, not a verdict.
  - When anomaly_check is true: build the intent exactly like a Policy threshold lookup (target_class=Policy, filter by ruleId/label contains the quantity, join Site via appliesToSite) — do NOT join or aggregate Observation data yourself. A separate deterministic step (outside this JSON) takes the rule(s) this query returns and checks each against its threshold; it needs the rule identity first, which is what this query provides. Do not switch off target_class=Policy just because the question mentions a quantity/site.
  - "relative_time": set for a window that ends now ("in the last 24 hours", "over the past 7 days", "this past week" = 1 week). "Now" is the latest reading in the knowledge graph (given with the query as the reference time), not today's date; the window is turned into a resultTime filter downstream, so do NOT also add resultTime filters for it. Null otherwise.
  - "as_of": set only when the question names a specific point in time ("on 2026-05-15", "last Tuesday" — resolve relative phrases to an absolute ISO date against the reference time). Null for "currently"/"now"/unstated, which defaults to the latest available reading. Never put a date into "filters" for an anomaly_check question (Policy has no resultTime) — as_of is the only place it belongs.

Follow-up handling (earlier turns may appear above as question → intent pairs):
  - Treat the current question as SELF-CONTAINED by default. If it can be understood on its own, IGNORE the earlier turns completely.
  - Use earlier turns ONLY to resolve what the current question leaves unresolved: pronouns ("there", "those", "it"), ellipsis ("what about delos?", "and the maximum?"), or an omitted subject.
  - When resolving, copy only the specific missing piece. NEVER carry over filters, aggregations, limits, joins or target_class that the current question does not itself imply. A new site/quantity mentioned now REPLACES the old one — it does not add to it.
  - The output intent must always be complete and standalone, exactly as if the question had been asked with no history.
  - "among these / of those / from that set" narrows the PREVIOUS result set. That set is defined by the previous intent's target_class and filters, so inherit those and ADD the new constraint as an extra join/filter. Never try to filter the previously returned rows — build a complete new query instead.
  - A "[The previous query returned …]" note tells you how big that set was and which columns it had. Those columns are only what was displayed; they do NOT limit what you may query now. If the new question needs a property that was not returned, add whatever joins are required to reach it.

{_FEW_SHOT}
"""


def _format_result_summary(summary: dict | None) -> str | None:
    if not summary or not summary.get("row_count"):
        return None
    parts = [f"[The previous query returned {summary['row_count']} row(s)"]
    if summary.get("columns"):
        parts.append(f"columns: {', '.join(summary['columns'])}")
    if summary.get("sample_values"):
        parts.append(f"e.g. {summary.get('sample_of') or 'value'} = "
                     f"{', '.join(summary['sample_values'])}")
    return "; ".join(parts) + "]"


def parse(query: str, feedback: str | None = None, history: list[dict] | None = None,
          temperature: float = 0.0, reference_time: str | None = None) -> dict:
    client = _get_client()

    user_content = f"Query: {query}"
    if reference_time:
        user_content = (f"[Reference time — the latest reading in the knowledge graph: {reference_time} UTC. "
                        f"Relative time expressions refer to this time, not to today's date.]\n{user_content}")
    if feedback:
        user_content += (
            "\n\n--- FEEDBACK FROM PREVIOUS ATTEMPT ---\n"
            f"{feedback}\n"
            "Please fix the intent JSON based on this feedback. "
            "Use only SHORT property names without namespace prefix. "
            "Output ONLY the corrected JSON."
        )

    messages = [
        {"role": "system", "content": PARSE_SYSTEM + "\n\nOntology schema:\n" + ONTOLOGY_SCHEMA},
    ]
    # Prior turns as (question → intent) pairs, so the model can resolve references
    # in a follow-up. Each turn's result shape is prepended to the NEXT question, so
    # "among these" has a concrete referent. The system prompt forbids inheriting
    # anything the current question does not itself imply.
    prev_summary = None
    for turn in history or []:
        content = f"Query: {turn['query']}"
        if prev_summary:
            content = f"{prev_summary}\n{content}"
        messages.append({"role": "user", "content": content})
        messages.append({"role": "assistant", "content": json.dumps(turn["intent"], ensure_ascii=False)})
        prev_summary = _format_result_summary(turn.get("result_summary"))

    if prev_summary:
        user_content = f"{prev_summary}\n{user_content}"
    messages.append({"role": "user", "content": user_content})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature,
    )
    raw = response.choices[0].message.content.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"[SemanticParser] JSON parse error: {e}. Raw: {raw[:200]}")
        return {
            "target_class": "ObservationCollection",
            "filters": [],
            "return_properties": [],
            "joins": [],
            "aggregation": None,
            "order_by": None,
            "limit": 10,
            "anomaly_check": False,
            "as_of": None,
            "explanation": f"Fallback intent for: {query}",
        }


# Sampling temperature for the extra candidates of a voted parse; the first
# candidate is always the greedy (temperature 0) one.
VOTE_TEMPERATURE = float(os.environ.get("ARGUS_VOTE_TEMPERATURE", "0.7"))


def _vote_key(intent: dict) -> str:
    # Two intents vote together when they would compile to the same query —
    # the free-text explanation does not count.
    return json.dumps({k: v for k, v in intent.items() if k != "explanation"}, sort_keys=True)


def parse_voted(query: str, n: int, history: list[dict] | None = None,
                reference_time: str | None = None) -> tuple[dict, dict]:
    """n parses in parallel (one greedy, n-1 sampled), majority vote on the
    intent. Ties go to the greedy candidate. Returns (intent, vote info)."""
    temps = [0.0] + [VOTE_TEMPERATURE] * (n - 1)
    with ThreadPoolExecutor(n) as ex:
        candidates = list(ex.map(lambda t: parse(query, history=history, temperature=t,
                                                 reference_time=reference_time), temps))
    # A candidate that failed to parse as JSON only votes if nothing else did.
    valid = [c for c in candidates if not str(c.get("explanation", "")).startswith("Fallback intent")] or candidates
    counts = Counter(_vote_key(c) for c in valid)
    top = max(counts.values())
    winner = next(c for c in valid if counts[_vote_key(c)] == top)
    return winner, {"candidates": n, "distinct": len(counts), "winner_votes": top}
