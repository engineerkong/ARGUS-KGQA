"""
Step 1 — Semantic Parser.

Sends the NL query + ontology schema to the LLM and returns a structured
intent JSON that describes which SOSA/ARGUS classes and properties are needed.
"""

from __future__ import annotations
import json
import os
from openai import OpenAI
from ontology_schema import get_ontology_schema, extract_class_list, extract_graph_connectivity

BASE_URL = os.environ.get("OLLAMA_BASE_URL", "https://ollama.fit.fraunhofer.de/api")
API_KEY  = os.environ.get("OPENAI_API_KEY", "no-key")
MODEL    = os.environ.get("OLLAMA_MODEL", "gpt-oss:120b")

ONTOLOGY_SCHEMA = get_ontology_schema()

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
  "aggregation": null or {{"type": "count|min|max|avg|sum", "group_by": "<variable>", "target": "<variable>"}},
  "order_by": null or {{"variable": "<variable>", "direction": "ASC|DESC"}},
  "limit": null or <integer>,
  "explanation": "<one sentence>"
}}

Operator guide:
  contains  — case-insensitive substring match on string literals
  equals    — exact case-insensitive match
  gt / lt   — numeric comparison (for measured values)
  after     — datetime is after the given ISO value (for resultTime)
  before    — datetime is before the given ISO value

{extract_graph_connectivity()}

Rules:
  - Use only class names and property names from the ontology schema above.
  - Always include label in return_properties for classes that have it.
  - Always include hasSimpleResult in return_properties when querying measured values.
  - For time-based queries use resultTime with after/before operators.
  - direction="outgoing" means target → related; "incoming" means related → target.
  - When two classes are not directly connected, follow the "Indirect paths" section to route through the required intermediate class.
  - Use SHORT property names without namespace prefix (e.g. "hasSite" not "argus:hasSite", "label" not "rdfs:label").
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
            "return_properties": [],
            "joins": [],
            "aggregation": None,
            "order_by": None,
            "limit": 10,
            "explanation": f"Fallback intent for: {query}",
        }
