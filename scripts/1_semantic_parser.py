"""
Step 1 — NL query + ontology schema → structured intent JSON naming the
SOSA/ARGUS classes and properties needed. Prior turns may be passed as history
so follow-up questions resolve against them.
"""

from __future__ import annotations
import json
import os
from openai import OpenAI
from ontology_schema import get_ontology_schema, extract_class_list

BASE_URL = os.environ.get("OLLAMA_BASE_URL", "https://ollama.fit.fraunhofer.de/api")
API_KEY  = os.environ.get("OPENAI_API_KEY", "no-key")
MODEL    = os.environ.get("OLLAMA_MODEL", "qwen3.6:35b")

# The SDK default is a 600s timeout with silent retries, so a stalled endpoint
# hangs the pipeline for many minutes with no output.
LLM_TIMEOUT     = float(os.environ.get("ARGUS_LLM_TIMEOUT", "120"))
LLM_MAX_RETRIES = int(os.environ.get("ARGUS_LLM_MAX_RETRIES", "2"))

ONTOLOGY_SCHEMA = get_ontology_schema()

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(
            base_url=BASE_URL, api_key=API_KEY,
            timeout=LLM_TIMEOUT, max_retries=LLM_MAX_RETRIES,
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
  Use this exact dotted form in group_by and order_by fields.\
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
  "explanation": "Count baltanas sensors (inherited set) that observe temperature (added constraint)."
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


def parse(query: str, feedback: str | None = None, history: list[dict] | None = None) -> dict:
    client = _get_client()

    user_content = f"Query: {query}"
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
        temperature=0.0,
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
            "explanation": f"Fallback intent for: {query}",
        }
