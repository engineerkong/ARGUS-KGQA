"""
Step 4 — Natural Language Answer Generator.

Passes the original query, SPARQL, raw results, AND pre-computed spatial/
temporal analysis to the LLM, asking it to reason — not just reformat.
"""

from __future__ import annotations
import json
import os
from openai import OpenAI

from geo_analysis import analyze

BASE_URL = os.environ.get("OLLAMA_BASE_URL", "https://ollama.fit.fraunhofer.de/api")
API_KEY  = os.environ.get("OPENAI_API_KEY", "no-key")
MODEL    = os.environ.get("OLLAMA_MODEL", "gpt-oss:120b")

SYSTEM = """You are a concise sensor data analyst for the ARGUS cultural heritage monitoring system.

You are given a user question, SPARQL results, and a numeric summary.

Rules:
- Answer the question directly in 1-3 short sentences.
- Include key numbers from the results (counts, values, site names).
- If results are tabular, present them as a compact list or table.
- If results are empty or contain an error, say so in one sentence and suggest a rephrased query.
- Do NOT explain the SPARQL query, the ontology, or how the system works.
- Do NOT add follow-up suggestions or next steps.
"""


def generate(query: str, sparql: str, results: list) -> str:
    client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

    analysis = analyze(results)

    results_text = json.dumps(results, indent=2, ensure_ascii=False)
    if len(results_text) > 3000:
        results_text = results_text[:3000] + "\n... (truncated)"

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
