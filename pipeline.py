"""
ARGUS KGQA Pipeline — orchestrates the four steps:

  1. Semantic parsing  (NL query → structured intent)
  2. KG store          (SOSA/ARGUS readings graph, loaded once)
  3. SPARQL retrieval  (intent → SPARQL → results)
  4. NL answer         (results → natural-language response)

If Step 3 returns an error or empty results, the pipeline feeds the failure
back to Step 1 and retries (up to max_retries times).
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any

from rdflib import Graph

from semantic_parser import parse
from sparql_retriever import build_sparql, execute, unfold_results
from answer_generator import generate

DEFAULT_TTL = Path(__file__).resolve().parent / "data" / "argus_readings.ttl"
MAX_RETRIES = 2


def _is_failed(results: list[dict]) -> str | None:
    """Return a feedback string if results indicate failure, else None."""
    if not results:
        return "The SPARQL query returned 0 results. The query may be too restrictive or using wrong class/property names."
    if len(results) == 1 and "error" in results[0]:
        return f"SPARQL execution error: {results[0]['error']}"
    return None


class Pipeline:
    def __init__(
        self,
        verbose: bool = True,
        ttl_path: str | Path | None = None,
        max_retries: int = MAX_RETRIES,
    ):
        self.verbose = verbose
        self.max_retries = max_retries
        ttl = Path(ttl_path) if ttl_path else DEFAULT_TTL

        if self.verbose:
            print(f"[Pipeline] Loading KG from {ttl}…")

        self.graph = Graph()
        if ttl.exists():
            self.graph.parse(str(ttl), format="turtle")
        else:
            print(f"[Pipeline] WARNING: TTL file not found: {ttl}")
            print("[Pipeline] Run `python readings.py --max-records 500` to fetch data first.")

        if self.verbose:
            print(f"[Pipeline] Graph ready — {len(self.graph)} triples.")

    def run(self, query: str) -> dict[str, Any]:
        v = self.verbose
        sep = "─" * 60

        feedback = None
        intent = None
        sparql = None
        results = []

        for attempt in range(1 + self.max_retries):
            # ── Step 1: Semantic Parsing ─────────────────────────────
            if v:
                print(f"\n{sep}")
                if attempt == 0:
                    print(f"[Step 1] Semantic parsing: {query!r}")
                else:
                    print(f"[Step 1] Retry {attempt}/{self.max_retries} — re-parsing with feedback")
            intent = parse(query, feedback=feedback)
            if v:
                print("[Step 1] Intent:", json.dumps(intent, indent=2))

            # ── Step 3: SPARQL Retrieval ─────────────────────────────
            sparql = build_sparql(intent)
            if v:
                print(f"\n{sep}")
                print("[Step 3] SPARQL query:")
                print(sparql)

            results = execute(self.graph, sparql)
            if v:
                print(f"[Step 3] {len(results)} result(s) returned.")
                for r in results[:5]:
                    print("  ", r)
                if len(results) > 5:
                    print(f"  … and {len(results) - 5} more.")

            # ── Check if we need to retry ────────────────────────────
            failure = _is_failed(results)
            if failure is None:
                break

            if attempt < self.max_retries:
                feedback = (
                    f"Previous SPARQL query:\n{sparql}\n\n"
                    f"Problem: {failure}\n\n"
                    f"Previous intent:\n{json.dumps(intent, indent=2)}"
                )
                if v:
                    print(f"\n[Pipeline] Query failed — {failure}")
                    print(f"[Pipeline] Retrying with feedback…")
            else:
                if v:
                    print(f"\n[Pipeline] Query failed after {self.max_retries} retries — {failure}")

        # ── Step 3.5: Unfold results ─────────────────────────────────
        unfolded = unfold_results(self.graph, results)
        if v and unfolded != results:
            print(f"\n{sep}")
            print("[Step 3.5] Unfolded results (URIs resolved to linked properties):")
            for r in unfolded[:5]:
                print("  ", r)
            if len(unfolded) > 5:
                print(f"  … and {len(unfolded) - 5} more.")

        # ── Step 4: Natural Language Answer ──────────────────────────
        if v:
            print(f"\n{sep}")
            print("[Step 4] Generating natural language answer…")
        answer = generate(query, sparql, unfolded)
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
