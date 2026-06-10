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

SYSTEM = """You are a cultural-heritage analyst with expertise in sensor networks
and heritage site monitoring.

You are given:
1. A user question.
2. The raw SPARQL query results.
3. A pre-computed spatial/temporal analysis of those results.

Your task is to write an ANALYTICAL answer that:
- Directly answers the user's question.
- Uses the pre-computed distances and timestamps to reason concretely — e.g.
  "Site A is 320 km from the pilot site, which is the farthest among the results."
- Identifies which sites/sensors are spatially close to each other and which
  are far from the pilot site, using the cluster analysis.
- Ranks or highlights observations by recency — e.g. "The most recent reading
  was taken 12 days ago at Hagia Sophia; the Pompeii data is over 2 years old."
- Points out any patterns, anomalies, or operationally relevant insights
  (e.g. a high seismic reading close to the pilot site, or an outdated sensor).
- Is grounded exclusively in the provided data (no hallucination).
- If results are empty, explains clearly and suggests alternatives.

Write in clear paragraphs. Use specific numbers from the analysis.
"""


def generate(
    query: str,
    sparql: str,
    results: list,
    pilot_lat: float = 37.9715,
    pilot_lon: float = 23.7267,
    pilot_name: str = "Parthenon (pilot site)",
) -> str:
    client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

    # Pre-compute spatial / temporal analysis
    analysis = analyze(results, pilot_lat, pilot_lon, pilot_name)

    # Truncate raw results for token budget
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
