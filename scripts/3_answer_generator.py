"""
Step 3 — turn results into an answer. The LLM receives the query, the SPARQL,
the full result rows and the pre-computed spatial/temporal analysis, and is
asked to reason over them rather than reformat them.
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

Statistics:
- When the query already computed an aggregate (a count/avg/min/max/sum column), report that value — it is the authoritative one.
- Otherwise the rows are a de-duplicated listing, so do NOT compute an average, total or record count from them; give the values, ranges or examples the rows support and leave it there.
- With many rows, summarise and name a few representative examples rather than enumerating everything.
"""


def _dedupe(results: list) -> list:
    seen = set()
    out = []
    for row in results:
        key = tuple(sorted(row.items()))
        if key not in seen:
            seen.add(key)
            out.append(row)
    return out


def prompt_row_stats(results: list) -> tuple[int, int]:
    # What the LLM will actually receive, so the caller can warn about slow turns.
    deduped = _dedupe(results)
    return len(deduped), len(json.dumps(deduped, indent=2, ensure_ascii=False))


def generate(query: str, sparql: str, results: list) -> str:
    client = _get_client()

    analysis = analyze(results)
    deduped = _dedupe(results)
    results_text = json.dumps(deduped, indent=2, ensure_ascii=False)

    user_msg = (
        f"User question:\n{query}\n\n"
        f"SPARQL query executed:\n```sparql\n{sparql}\n```\n\n"
        f"Results — all {len(deduped)} distinct rows ({len(results)} total):\n{results_text}\n\n"
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
