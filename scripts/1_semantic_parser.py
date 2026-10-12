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

# The rules and examples of each deterministic layer come from that layer, so the
# parser is told exactly what the code that executes its intent does.
import importlib
_query = importlib.import_module("2_sparql_retriever")
import analysis_geo as _spatial
import analysis_ek as _anomaly
import analysis_temp as _temporal
TIME_OPERATORS, TIME_GUIDE, TIME_EXAMPLES = _temporal.PARSER_OPERATORS, _temporal.PARSER_GUIDE, _temporal.PARSER_EXAMPLES
QUERY_OPERATORS, QUERY_GUIDE, QUERY_EXAMPLES = _query.PARSER_OPERATORS, _query.PARSER_GUIDE, _query.PARSER_EXAMPLES
SPATIAL_SCHEMA, SPATIAL_GUIDE, SPATIAL_EXAMPLES = _spatial.PARSER_SCHEMA, _spatial.PARSER_GUIDE, _spatial.PARSER_EXAMPLES
ANOMALY_SCHEMA, ANOMALY_GUIDE, ANOMALY_EXAMPLES = _anomaly.PARSER_SCHEMA, _anomaly.PARSER_GUIDE, _anomaly.PARSER_EXAMPLES

BASE_URL = os.environ.get("OLLAMA_BASE_URL", "https://chat.kiconnect.nrw/api/v1")
API_KEY  = os.environ.get("OPENAI_API_KEY", "no-key")
MODEL    = os.environ.get("OLLAMA_MODEL", "openai-gpt-oss-120b")

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

Variable naming rule: the SPARQL variable for a join's return property is {ClassName}_{property}.
  Site.label → ?site_label        Observation.hasSimpleResult → ?observation_hassimpleresult
  Use this exact dotted form in group_by and order_by fields.\
"""

# Examples that belong to no single layer: follow-up resolution and a plain lookup.
_FEW_SHOT = """\
Q: "of those nodes, how many are above 700 m?"
   (follow-up; the previous turn asked "which nodes are at lucretili?" and returned 13 nodes)
   Inherit the set definition — target_class=Node plus the lucretili Site filter — then ADD the
   altitude constraint and count.
{
  "target_class": "Node",
  "filters": [{"property": "altitude", "op": "gt", "value": "700"}],
  "return_properties": [],
  "joins": [
    {"class": "ObservationCollection", "via": "hasNode", "direction": "incoming",
     "return_properties": [], "filters": []},
    {"class": "Site", "via": "hasSite", "direction": "outgoing",
     "return_properties": [], "filters": [{"property": "label", "op": "equals", "value": "lucretili"}]}
  ],
  "aggregation": {"type": "count", "group_by": null, "target": "node", "distinct": true},
  "order_by": null,
  "limit": null,
  "anomaly_check": false,
  "as_of": null,
  "explanation": "Count lucretili nodes (inherited set) above 700 m (added constraint)."
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
}"""

PARSE_SYSTEM = f"""You are a semantic parser for an ARGUS knowledge graph.

Given a natural-language query, output ONLY a valid JSON object (no markdown fences)
with this exact schema:

{{
  "target_class": "<class name, one of: {extract_class_list()}>",
  "filters": [
    {{"property": "<property>", "op": "contains|equals|in|gt|lt|from|until|after|before", "value": "<string, or a list for in>"}}
  ],
  "return_properties": ["<list of properties to SELECT>"],
  "joins": [
    {{
      "class": "<related class>",
      "via": "<property name>",
      "direction": "outgoing|incoming",
      "return_properties": ["<properties of the related class>"],
      "filters": [
        {{"property": "<property>", "op": "contains|equals|in|gt|lt|from|until|after|before", "value": "<string, or a list for in>"}}
      ]
    }}
  ],
  "aggregation": null or {{"type": "count|min|max|avg|sum|range", "group_by": "ClassName.property", "time_bucket": null|"day"|"month", "target": "<class or property>", "distinct": true|false}},
  "order_by": null or {{"variable": "ClassName.property", "direction": "ASC|DESC"}},
  "limit": null or <integer>,
  "anomaly_check": true|false,
  "as_of": null or "<ISO date or datetime, e.g. '2025-02-11'>",
  "relative_time": null or {{"amount": <integer>, "unit": "hours|days|weeks"}},
  "unanswerable": null or "<what the knowledge graph does not model>",
  "explanation": "<one sentence>"
}}

Operator guide:
{QUERY_OPERATORS}
{TIME_OPERATORS}

{_GRAPH_PATHS}

{SPATIAL_SCHEMA}

{ANOMALY_SCHEMA}

Rules:
  - Use only class names and property names from the ontology schema.
  - Only include in return_properties the fields that directly answer the question. Do not include internal metadata (deviceGroupId, readingType, sensorId, sensorModel, etc.) unless the user explicitly asked for them.
  - Always include label in return_properties for classes that have it (Site, ObservedProperty, Sensor, Node).
  - Always include hasSimpleResult in return_properties when querying measured values.
  - direction="outgoing" means the subject (anchor) → via → object (join class).  direction="incoming" means object (join class) → via → subject (anchor).
  - When asking to LIST instances of a class (e.g. "which sensors", "what sites"), set target_class to that class directly and join ObservationCollection as needed for filtering — EXCEPT for "what quantities/properties are measured/observed at site X": use target_class=ObservationCollection and forward-join Site (filtered), Observation, ObservedProperty (as in the examples).
  - The property "readingType" holds data-format codes ("reading", "eng_units") — NOT physical measurement types. To filter by measurement type (temperature, humidity, etc.), filter on ObservedProperty.label via the hasObservation → observedProperty chain.
  - "unanswerable": set (to a short reason) ONLY when the question needs something this knowledge graph does not model at all — e.g. ownership, costs, opening hours, construction materials, people — i.e. nothing in the schema or the label lists could hold it. Never for a quantity or period that might merely have no readings (that is decided by running the query), and never for an expert-rule/anomaly question (whether a rule applies is decided by the AD-RT rule evaluation). Leave the rest of the intent minimal when set.

Queries and aggregation (rules of the query compiler):
{QUERY_GUIDE}

Time (rules of the temporal layer):
{TIME_GUIDE}

Spatial questions (rules of the spatial analysis layer):
{SPATIAL_GUIDE}

Expert rules and anomalies (rules of the AD-RT rule evaluation):
{ANOMALY_GUIDE}

Follow-up handling (earlier turns may appear above as question → intent pairs):
  - Treat the current question as SELF-CONTAINED by default. If it can be understood on its own, IGNORE the earlier turns completely.
  - Use earlier turns ONLY to resolve what the current question leaves unresolved: pronouns ("there", "those", "it"), ellipsis ("what about <another site>?", "and the <other statistic>?"), or an omitted subject.
  - When resolving, copy only the specific missing piece. NEVER carry over filters, aggregations, limits, joins or target_class that the current question does not itself imply. A new site/quantity mentioned now REPLACES the old one — it does not add to it.
  - The output intent must always be complete and standalone, exactly as if the question had been asked with no history.
  - Relative periods in a follow-up ("the following day", "the next month", "the day before") are relative to the period of the previous turn — read its date from the previous intent and shift it: previous "on 2025-03-04" + "the following day" → from 2025-03-05, until 2025-03-05.
  - "among these / of those / from that set" narrows the PREVIOUS result set. That set is defined by the previous intent's target_class and filters, so inherit those and ADD the new constraint as an extra join/filter. Never try to filter the previously returned rows — build a complete new query instead.
  - A "[The previous query returned …]" note tells you how big that set was and which columns it had. Those columns are only what was displayed; they do NOT limit what you may query now. If the new question needs a property that was not returned, add whatever joins are required to reach it.

--- EXAMPLES ---

{QUERY_EXAMPLES}

{TIME_EXAMPLES}

{SPATIAL_EXAMPLES}

{ANOMALY_EXAMPLES}

{_FEW_SHOT}

--- END EXAMPLES ---
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
          temperature: float = 0.0, reference_time: str | None = None, vocabulary: str | None = None) -> dict:
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
        {"role": "system", "content": PARSE_SYSTEM + "\n\nOntology schema:\n" + ONTOLOGY_SCHEMA
                                      + (f"\n\n{vocabulary}" if vocabulary else "")},
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
        intent = json.loads(raw)
        if not isinstance(intent, dict):
            raise ValueError(f"expected one JSON object, got {type(intent).__name__}")
        return intent
    except (json.JSONDecodeError, ValueError) as e:
        print(f"[SemanticParser] JSON parse error: {e}. Raw: {raw[:200]}")
        # No query is run for an unparseable output: the pipeline treats
        # parse_error like an execution error (retry with feedback, else an
        # honest "could not interpret"), instead of answering from arbitrary rows.
        return {
            "parse_error": (f"Your output was not a single valid JSON object ({e}). Output exactly one JSON "
                            f"object following the schema, with nothing before or after it."),
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
                reference_time: str | None = None, vocabulary: str | None = None) -> tuple[dict, dict]:
    """n parses in parallel (one greedy, n-1 sampled), majority vote on the
    intent. Ties go to the greedy candidate. Returns (intent, vote info)."""
    temps = [0.0] + [VOTE_TEMPERATURE] * (n - 1)
    with ThreadPoolExecutor(n) as ex:
        candidates = list(ex.map(lambda t: parse(query, history=history, temperature=t,
                                                 reference_time=reference_time, vocabulary=vocabulary), temps))
    # A candidate that failed to parse as JSON only votes if nothing else did.
    valid = [c for c in candidates if not str(c.get("explanation", "")).startswith("Fallback intent")] or candidates
    counts = Counter(_vote_key(c) for c in valid)
    top = max(counts.values())
    winner = next(c for c in valid if counts[_vote_key(c)] == top)
    return winner, {"candidates": n, "distinct": len(counts), "winner_votes": top}
