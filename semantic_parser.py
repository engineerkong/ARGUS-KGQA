"""
Step 1 — Semantic Parser.

Sends the NL query + ontology schema to the LLM and returns a structured
intent JSON that describes which SOSA/ARGUS classes and properties are needed.
"""

from __future__ import annotations
import json
import os
from openai import OpenAI

BASE_URL = os.environ.get("OLLAMA_BASE_URL", "https://ollama.fit.fraunhofer.de/api")
API_KEY  = os.environ.get("OPENAI_API_KEY", "no-key")
MODEL    = os.environ.get("OLLAMA_MODEL", "gpt-oss:120b")

ONTOLOGY_SCHEMA = """
ARGUS Sensor Readings Ontology

Namespaces:
  sosa:  <http://www.w3.org/ns/sosa/>
  argus: <http://www.argus-project.eu/ontology/>
  ex:    <http://www.argus-project.eu/resource/>
  rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
  xsd:   <http://www.w3.org/2001/XMLSchema#>

Classes:
  sosa:ObservationCollection  — a sensor reading event (one per API record, may contain multiple observations)
  sosa:Observation            — a single measured value within a reading
  sosa:Sensor                 — a physical sensor device
  argus:Site                  — a monitoring site (e.g. baltanas, lucretili, delos, ranverso)
  argus:Node                  — a sensor node grouping multiple sensors
  argus:ObservedProperty      — the physical quantity being measured (e.g. temperature, voltage, displacement)
  argus:EngineeringUnit       — the engineering unit of a reading

Properties of sosa:ObservationCollection (a reading):
  sosa:resultTime         (xsd:dateTime)  — when the reading was taken
  argus:hasSite           → argus:Site
  sosa:madeBySensor       → sosa:Sensor
  argus:hasNode           → argus:Node
  argus:hasObservation    → sosa:Observation
  argus:hasEngineeringUnit → argus:EngineeringUnit
  argus:readingType       (literal)

Properties of sosa:Observation:
  sosa:observedProperty   → argus:ObservedProperty
  sosa:hasSimpleResult    (xsd:decimal / xsd:integer / literal) — the measured value
  sosa:resultTime         (xsd:dateTime)

Properties of argus:Site / sosa:Sensor / argus:Node / argus:ObservedProperty / argus:EngineeringUnit:
  rdfs:label              (literal) — human-readable name

Known sites: baltanas, lucretili, delos, ranverso, schenkenberg, eurecat
Known quantities include: temperature, voltage, displacement, rainfall, humidity, soil_temperature,
  soil_water_potential, thermistor, potentiometer_displacement, pulse_counter, and many more.
"""

PARSE_SYSTEM = """You are a semantic parser for an ARGUS sensor readings knowledge graph.

Given a natural-language query, output ONLY a valid JSON object (no markdown fences)
with this exact schema:

{
  "target_class": "<class name, one of: ObservationCollection, Observation, Site, Sensor, Node, ObservedProperty, EngineeringUnit>",
  "filters": [
    {"property": "<property>", "op": "contains|equals|gt|lt|after|before", "value": "<string>"}
  ],
  "return_properties": ["<list of properties to SELECT>"],
  "joins": [
    {
      "class": "<related class>",
      "via": "<property name>",
      "direction": "outgoing|incoming",
      "return_properties": ["<properties of the related class>"],
      "filters": [
        {"property": "<property>", "op": "contains|equals|gt|lt|after|before", "value": "<string>"}
      ]
    }
  ],
  "aggregation": null or {"type": "count|min|max|avg|sum", "group_by": "<variable>", "target": "<variable>"},
  "order_by": null or {"variable": "<variable>", "direction": "ASC|DESC"},
  "limit": null or <integer>,
  "explanation": "<one sentence>"
}

Operator guide:
  contains  — case-insensitive substring match on string literals
  equals    — exact case-insensitive match
  gt / lt   — numeric comparison (for measured values)
  after     — datetime is after the given ISO value (for sosa:resultTime)
  before    — datetime is before the given ISO value

Common query patterns:
  - "readings per site" → target ObservationCollection, join Site, aggregate count group by site
  - "temperature values" → target Observation, join ObservedProperty (filter label = "temperature"), return hasSimpleResult
  - "which sensors at site X" → target Sensor, join ObservationCollection (incoming via madeBySensor), join Site (filter label)
  - "latest readings" → target ObservationCollection, order by resultTime DESC, limit N

Rules:
  - Use only class names and property names from the ontology schema above.
  - Always include rdfs:label in return_properties for Site, Sensor, Node, ObservedProperty.
  - For time-based queries use sosa:resultTime with after/before operators.
  - direction="outgoing" means target → related; "incoming" means related → target.
"""


def parse(query: str, feedback: str | None = None) -> dict:
    """Parse a NL query into a structured intent.

    If feedback is provided (from a failed previous attempt), it is appended
    to the user message so the LLM can correct its output.
    """
    client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

    user_content = f"Query: {query}"
    if feedback:
        user_content += (
            "\n\n--- FEEDBACK FROM PREVIOUS ATTEMPT ---\n"
            f"{feedback}\n"
            "Please fix the intent JSON based on this feedback. "
            "Use only SHORT property names (e.g. 'hasSite' not 'argus:hasSite', "
            "'label' not 'rdfs:label'). Output ONLY the corrected JSON."
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
            "return_properties": ["resultTime"],
            "joins": [{"class": "Site", "via": "hasSite", "direction": "outgoing",
                        "return_properties": ["label"], "filters": []}],
            "aggregation": None,
            "order_by": None,
            "limit": None,
            "explanation": f"Fallback intent for: {query}",
        }
