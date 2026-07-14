"""
Step 1 — Semantic Parser.

Sends the NL query + ontology schema to the LLM and returns a structured
intent JSON that describes which SOSA/ARGUS classes and properties are needed.
"""

from __future__ import annotations
import json
import os
from openai import OpenAI
from ontology_schema import get_ontology_schema, extract_class_list

BASE_URL = os.environ.get("OLLAMA_BASE_URL", "https://ollama.fit.fraunhofer.de/api")
API_KEY  = os.environ.get("OPENAI_API_KEY", "no-key")
MODEL    = os.environ.get("OLLAMA_MODEL", "gpt-oss:120b")

ONTOLOGY_SCHEMA = get_ontology_schema()

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

Variable naming rule: the SPARQL variable for a join's return property is {ClassName}_{property}.
  Site.label → ?site_label        Observation.hasSimpleResult → ?observation_hassimpleresult
  Use this exact dotted form in group_by and order_by fields.\
"""

_FEW_SHOT = """\
--- EXAMPLES ---

Q: "How many readings are available per site?"
{
  "target_class": "ObservationCollection",
  "filters": [],
  "return_properties": [],
  "joins": [
    {"class": "Site", "via": "hasSite", "direction": "outgoing",
     "return_properties": ["label"], "filters": []}
  ],
  "aggregation": {"type": "count", "group_by": "Site.label",
                  "target": "observationcollection", "distinct": true},
  "order_by": null, "limit": null,
  "explanation": "Count distinct ObservationCollections per site."
}

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
  "aggregation": {"type": "avg", "group_by": "Site.label",
                  "target": "hasSimpleResult", "distinct": false},
  "order_by": null, "limit": null,
  "explanation": "Average temperature per site via ObservedProperty filter."
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
  "target_class": "ObservationCollection",
  "filters": [],
  "return_properties": ["resultTime"],
  "joins": [
    {"class": "Observation", "via": "hasObservation", "direction": "outgoing",
     "return_properties": ["hasSimpleResult"], "filters": []},
    {"class": "Site", "via": "hasSite", "direction": "outgoing",
     "return_properties": ["label"], "filters": []}
  ],
  "aggregation": null,
  "order_by": {"variable": "ObservationCollection.resultTime", "direction": "DESC"},
  "limit": 10,
  "explanation": "10 most recent ObservationCollections with value and site."
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
  - group_by and order_by variables MUST use the dotted "ClassName.property" form (e.g. "Site.label", "ObservationCollection.resultTime"). The join for that class MUST be present and include the property in return_properties.
  - When asking to LIST instances of a class (e.g. "which sensors", "what sites"), set target_class to that class directly and join ObservationCollection as needed for filtering — EXCEPT for "what quantities/properties are measured/observed at site X": use target_class=ObservationCollection and forward-join Site (filtered), Observation, ObservedProperty (as shown in example 5).
  - The property "readingType" holds data-format codes ("reading", "eng_units") — NOT physical measurement types. To filter by measurement type (temperature, humidity, etc.), filter on ObservedProperty.label via the hasObservation → observedProperty chain.

{_FEW_SHOT}
"""


def parse(query: str, feedback: str | None = None) -> dict:
    client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

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
        {"role": "user",   "content": user_content},
    ]

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
