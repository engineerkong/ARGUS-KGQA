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
  Measurement         — a sensor observation linked to an asset
  Quantity            — the numeric value + unit of a measurement
  Prediction          — a forecast about an asset
  CulturalDocumentation — document or report about an asset
  Policy              — a management or protection policy
  Decision            — a management decision
  Instrument          — a sensor or measurement device

Key datatype properties of Asset:
  name, country, coordinates, construction_period,
  architectural_style, material_used, current_condition

Key datatype properties of Event:
  name (description), event_date

Key datatype properties of Threat:
  threat_description, threat_level   (high / medium / low)

Key datatype properties of RiskAssessment:
  FrequencyA, LossB, FractionC, MagnitudeOfRisk

Key datatype properties of Measurement / Quantity:
  name (type of measurement), quantity_value, quantity_unit

Key object properties:
  Asset  → hasEvent      → Event
  Asset  → isTriggeredBy → Threat
  Asset  → (via RiskAssessment.assessesRiskFor) → RiskAssessment
  Event  → generatesThreat → Threat
  Measurement → measures → Asset
  CulturalDocumentation → documents → Asset
"""

PARSE_SYSTEM = """You are a semantic parser for a cultural-heritage knowledge graph.

Given a natural-language query, output ONLY a valid JSON object (no markdown fences)
with this exact schema:

{
  "target_class": "<Panoptes class name, e.g. Asset>",
  "filters": [
    {"property": "<datatype property>", "op": "contains|equals|gt|lt", "value": "<string>"}
  ],
  "return_properties": ["<list of datatype properties to SELECT>"],
  "joins": [
    {
      "class": "<related class>",
      "via": "<object property from target to related class, e.g. hasEvent>",
      "direction": "outgoing|incoming",
      "return_properties": ["<properties of the related class>"],
      "filters": []
    }
  ],
  "explanation": "<one sentence>"
}

Rules:
- Use only class names and property names from the ontology schema provided.
- For Asset queries, always include "name" and "country" in return_properties.
- For joins, "direction": "incoming" means the related class points TO the target
  (e.g. Measurement.measures → Asset, so to get measurements of an asset use
   direction="incoming", via="measures").
- Keep it minimal: only add joins that are needed to answer the question.
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
        # Best-effort: return a fallback intent
        print(f"[SemanticParser] JSON parse error: {e}. Raw: {raw[:200]}")
        return {
            "target_class": "Asset",
            "filters": [],
            "return_properties": ["name", "country", "current_condition"],
            "joins": [],
            "explanation": f"Fallback intent for: {query}",
        }
