"""
Step 3 — Natural Language Answer Generator.

Passes the original query, SPARQL, unfolded results, and pre-computed
spatial/temporal analysis to the LLM, asking it to reason — not just reformat.
"""

from __future__ import annotations
import json
import os
from openai import OpenAI

from geo_analysis import analyze

BASE_URL = os.environ.get("OLLAMA_BASE_URL", "https://ollama.fit.fraunhofer.de/api")
API_KEY  = os.environ.get("OPENAI_API_KEY", "no-key")
MODEL    = os.environ.get("OLLAMA_MODEL", "gpt-oss:120b")

# The SDK default is a 600s timeout with silent retries, so a stalled endpoint
# hangs the pipeline for many minutes with no output.
LLM_TIMEOUT     = float(os.environ.get("ARGUS_LLM_TIMEOUT", "120"))
LLM_MAX_RETRIES = int(os.environ.get("ARGUS_LLM_MAX_RETRIES", "2"))

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(
            base_url=BASE_URL, api_key=API_KEY,
            timeout=LLM_TIMEOUT, max_retries=LLM_MAX_RETRIES,
        )
    return _client

SYSTEM = """You are a concise sensor data analyst for the ARGUS cultural heritage monitoring system.

You are given a user question, SPARQL results, and a numeric summary.

Rules:
- Answer the question directly in 1-3 short sentences.
- Include key numbers from the results (counts, values, site names).
- If results are tabular, present them as a compact list or table.
- If results are empty or contain an error, say so in one sentence and suggest a rephrased query.
- Do NOT output URIs or internal identifiers — use human-readable names and labels only.
- Do NOT explain the SPARQL query, the ontology, or how the system works.
- Do NOT add follow-up suggestions or next steps.
"""


def generate(query: str, sparql: str, results: list) -> str:
    client = _get_client()

    analysis = analyze(results)

    # Deduplicate rows before serialising so repeated observations of the same
    # entity don't dominate the MAX_RESULT_CHARS budget and hide other rows.
    seen = set()
    deduped = []
    for row in results:
        key = tuple(sorted(row.items()))
        if key not in seen:
            seen.add(key)
            deduped.append(row)

    results_text = json.dumps(deduped, indent=2, ensure_ascii=False)

    user_msg = (
        f"User question:\n{query}\n\n"
        f"SPARQL query executed:\n```sparql\n{sparql}\n```\n\n"
        f"Raw results ({len(results)} rows):\n{results_text}\n\n"
        f"Pre-computed spatial & temporal analysis:\n"
        f"{analysis['summary_text']}"
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user",   "content": user_msg},
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()
