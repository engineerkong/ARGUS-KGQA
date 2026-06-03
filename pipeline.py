"""
ARGUS KGQA Pipeline — orchestrates the four steps:

  1. Semantic parsing  (NL query → structured intent)
  2. KG instance store (panoptes3.owl + dummy instances, loaded once)
  3. SPARQL retrieval  (intent → SPARQL → results)
  4. NL answer         (results → natural-language response)
"""

from __future__ import annotations
from typing import Any

from kg_store        import build_graph
from semantic_parser import parse
from sparql_retriever import build_sparql, execute
from answer_generator import generate


class Pipeline:
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        if self.verbose:
            print("[Pipeline] Loading KG store (panoptes3.owl + instances)…")
        self.graph = build_graph()
        if self.verbose:
            print(f"[Pipeline] Graph ready — {len(self.graph)} triples.")

    def run(self, query: str) -> dict[str, Any]:
        v = self.verbose
        sep = "─" * 60

        # ── Step 1: Semantic Parsing ──────────────────────────────────────────
        if v:
            print(f"\n{sep}")
            print(f"[Step 1] Semantic parsing: {query!r}")
        intent = parse(query)
        if v:
            import json
            print("[Step 1] Intent:", json.dumps(intent, indent=2))

        # ── Step 2 (store already loaded) ─────────────────────────────────────
        # The graph is pre-built; nothing to do per-query.

        # ── Step 3: SPARQL Retrieval ──────────────────────────────────────────
        sparql = build_sparql(intent)
        if v:
            print(f"\n{sep}")
            print("[Step 3] SPARQL query:")
            print(sparql)

        results = execute(self.graph, sparql)
        if v:
            print(f"[Step 3] {len(results)} result(s) returned.")
            for r in results[:3]:
                print("  ", r)
            if len(results) > 3:
                print(f"  … and {len(results) - 3} more.")

        # ── Step 4: Natural Language Answer ───────────────────────────────────
        if v:
            print(f"\n{sep}")
            print("[Step 4] Generating natural language answer…")
        answer = generate(query, sparql, results)
        if v:
            print("[Step 4] Answer:")
            print(answer)

        return {
            "query":   query,
            "intent":  intent,
            "sparql":  sparql,
            "results": results,
            "answer":  answer,
        }
