"""
Step 1 — Semantic Parser.

Sends the NL query + ontology schema to the LLM and returns a structured
intent JSON that describes which Panoptes classes and properties are needed.
"""

from __future__ import annotations
import json
import os
from openai import OpenAI

BASE_URL = os.environ.get("OLLAMA_BASE_URL", "https://ollama.fit.fraunhofer.de/api")
API_KEY  = os.environ.get("OPENAI_API_KEY", "no-key")
MODEL    = os.environ.get("OLLAMA_MODEL", "gpt-oss:120b")

# ── Ontology schema summary given to the LLM ──────────────────────────────────
ONTOLOGY_SCHEMA = """
ARGUS Panoptes Ontology (namespace: http://www.argus-project.eu/)

Classes:
  Asset               — a cultural heritage site or object
  Event               — a real-world occurrence affecting an asset (earthquake, flood, fire…)
  Threat              — a risk scenario related to an asset
  RiskAssessment      — quantified risk analysis for an asset
  Measurement         — a single on-site sensor reading at a specific time and location
  Quantity            — the numeric value + unit of a measurement
  CulturalDocumentation — document or report about an asset
  Instrument          — a sensor or measurement device

Datatype properties of Asset:
  name, country, latitude (float), longitude (float), coordinates,
  construction_period, architectural_style, material_used, current_condition

Datatype properties of Event:
  name (description), event_date  (xsd:date, e.g. "2023-02-06")

Datatype properties of Threat:
  threat_description, threat_level   (high / medium / low)

Datatype properties of RiskAssessment:
  FrequencyA, LossB, FractionC, MagnitudeOfRisk

Datatype properties of Measurement:
  observation_time  (xsd:dateTime, e.g. "2023-02-06T14:30:00") — WHEN the reading was taken
  sensor_lat        (float) — latitude of the sensor
  sensor_lon        (float) — longitude of the sensor

Datatype properties of Quantity (linked from Measurement via pan:quantifies):
  name   — type of measurement (e.g. "seismic activity", "relative humidity", "surface temperature")
  quantity_value  (float)
  quantity_unit   — e.g. "Richter", "%", "°C", "degrees", "AQI"

Object properties:
  Asset       → hasEvent          → Event
  Asset       → isTriggeredBy     → Threat
  RiskAssessment.assessesRiskFor  → Asset
  Event       → generatesThreat   → Threat
  Measurement → measures          → Asset       (incoming from Asset's perspective)
  Measurement → quantifies        → Quantity    (outgoing from Measurement)
  CulturalDocumentation → documents → Asset
"""

PARSE_SYSTEM = """You are a semantic parser for a cultural-heritage sensor knowledge graph.

Given a natural-language query, output ONLY a valid JSON object (no markdown fences)
with this exact schema:

{
  "target_class": "<Panoptes class name>",
  "filters": [
    {"property": "<datatype property>", "op": "contains|equals|gt|lt|after|before", "value": "<string>"}
  ],
  "return_properties": ["<list of datatype properties to SELECT>"],
  "joins": [
    {
      "class": "<related class>",
      "via": "<object property name>",
      "direction": "outgoing|incoming",
      "return_properties": ["<properties of the related class>"],
      "filters": [
        {"property": "<property>", "op": "contains|equals|gt|lt|after|before", "value": "<string>"}
      ]
    }
  ],
  "explanation": "<one sentence>"
}

Operator guide:
  contains  — case-insensitive substring match on string literals
  equals    — exact case-insensitive match
  gt / lt   — numeric greater-than / less-than (for float properties)
  after     — datetime is after the given ISO value (for observation_time, event_date)
  before    — datetime is before the given ISO value

Temporal queries:
  - Use "after" / "before" with ISO 8601 values.
  - Example: readings after 2023-01-01 → {"property": "observation_time", "op": "after", "value": "2023-01-01T00:00:00"}
  - For event_date (xsd:date), still use "after"/"before" with "YYYY-MM-DD" values.

Spatial / location queries:
  - To filter by country: {"property": "country", "op": "equals", "value": "Italy"}
  - To return sensor position: include "sensor_lat" and "sensor_lon" in return_properties
    of the Measurement join (or as target if target_class is Measurement).
  - To return asset position: include "latitude" and "longitude" in Asset return_properties.

Measurement queries:
  - target_class = "Measurement" when asking about sensor readings directly.
  - Join to Asset (direction="outgoing", via="measures") to get asset name/country.
  - Join to Quantity (direction="outgoing", via="quantifies") to get value/unit/type.

Rules:
  - Use only class names and property names from the ontology schema above.
  - For Asset queries include "name" and "country" in return_properties.
  - For Measurement queries always include "observation_time", "sensor_lat", "sensor_lon".
  - direction="incoming" means the related class's property points TO the target.
"""


def parse(query: str) -> dict:
    client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

    messages = [
        {"role": "system", "content": PARSE_SYSTEM + "\n\nOntology schema:\n" + ONTOLOGY_SCHEMA},
        {"role": "user",   "content": f"Query: {query}"},
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.0,
    )
    raw = response.choices[0].message.content.strip()

    # Strip accidental markdown fences
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
            "target_class": "Asset",
            "filters": [],
            "return_properties": ["name", "country", "current_condition"],
            "joins": [],
            "explanation": f"Fallback intent for: {query}",
        }
