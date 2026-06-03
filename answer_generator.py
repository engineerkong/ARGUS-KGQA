"""
Step 4 — Natural Language Answer Generator.

Given the original query, the SPARQL that was run, and the retrieved results,
asks the LLM to produce a concise, grounded natural-language answer.
"""

from __future__ import annotations
import json
import os
from openai import OpenAI

BASE_URL = os.environ.get("OLLAMA_BASE_URL", "https://ollama.fit.fraunhofer.de/api")
API_KEY  = os.environ.get("OPENAI_API_KEY", "no-key")
MODEL    = os.environ.get("OLLAMA_MODEL", "gpt-oss:120b")

SYSTEM = """You are a cultural-heritage assistant.
You are given a user question, the SPARQL query that was executed against the
knowledge graph, and the results returned by the query.

Your job: write a clear, concise natural-language answer that:
- Directly addresses the user's question.
- Is grounded exclusively in the provided query results (do not hallucinate facts).
- Lists specific site names, values, and relevant details from the results.
- If the results are empty, say so and suggest what the user might try instead.
"""


def generate(query: str, sparql: str, results: list) -> str:
    client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

    results_text = json.dumps(results, indent=2, ensure_ascii=False)
    if len(results_text) > 4000:
        results_text = results_text[:4000] + "\n... (truncated)"

    user_msg = (
        f"User question: {query}\n\n"
        f"SPARQL query executed:\n```sparql\n{sparql}\n```\n\n"
        f"Query results ({len(results)} rows):\n{results_text}"
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user",   "content": user_msg},
        ],
        temperature=0.3,
    )

    answer = response.choices[0].message.content.strip()
    return answer
