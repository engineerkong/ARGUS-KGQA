"""
ARGUS KGQA Pipeline — orchestrates three steps per query:

  Step 0. KG store          (SOSA/ARGUS readings graph, loaded once at init)
  Step 1. Semantic parsing  (NL query → structured intent)
  Step 2. SPARQL retrieval  (intent → SPARQL → raw results → unfolded results)
  Step 3. NL answer         (unfolded results → natural-language response)

If Step 2 returns an error or empty results, the pipeline feeds the failure
back to Step 1 and retries (up to max_retries times).
"""

from __future__ import annotations
import importlib
import json
import os
from pathlib import Path
from typing import Any

from rdflib import Graph

_sp = importlib.import_module("1_semantic_parser")
parse = _sp.parse

_sr = importlib.import_module("2_sparql_retriever")
build_sparql = _sr.build_sparql
execute      = _sr.execute
unfold_results = _sr.unfold_results

_ag = importlib.import_module("3_answer_generator")
generate = _ag.generate

_DEFAULT_TTL_PATH = Path(__file__).resolve().parent.parent / "data_500" / "argus_readings.ttl"
DEFAULT_TTL = Path(os.environ.get("ARGUS_TTL_PATH", str(_DEFAULT_TTL_PATH)))
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

        # ── Step 0: Load KG store (once) ────────────────────────────────────
        if self.verbose:
            print(f"[Step 0] Loading KG from {ttl}…")

        self.graph = Graph()
        if ttl.exists():
            self.graph.parse(str(ttl), format="turtle")
        else:
            print(f"[Step 0] WARNING: TTL file not found: {ttl}")
            print("[Step 0] Run `python scripts/0_readings.py --max-records 500` to fetch data first.")

        if self.verbose:
            print(f"[Step 0] Graph ready — {len(self.graph)} triples.")

    def run(self, query: str) -> dict[str, Any]:
        v = self.verbose
        sep = "─" * 60

        feedback = None
        intent = None
        sparql = None
        raw_results = []

        for attempt in range(1 + self.max_retries):
            # ── Step 1: Semantic Parsing ─────────────────────────────────────
            if v:
                print(f"\n{sep}")
                if attempt == 0:
                    print(f"[Step 1] Semantic parsing: {query!r}")
                else:
                    print(f"[Step 1] Retry {attempt}/{self.max_retries} — re-parsing with feedback")
            intent = parse(query, feedback=feedback)
            if v:
                print("[Step 1] Intent:", json.dumps(intent, indent=2))

            # ── Step 2: SPARQL Retrieval + Result Unfolding ──────────────────
            sparql = build_sparql(intent)
            if v:
                print(f"\n{sep}")
                print("[Step 2] SPARQL query:")
                print(sparql)

            raw_results = execute(self.graph, sparql)
            if v:
                print(f"[Step 2] {len(raw_results)} raw result(s) returned.")

            # ── Check if we need to retry ────────────────────────────────────
            failure = _is_failed(raw_results)
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
                    print("[Pipeline] Retrying with feedback…")
            else:
                if v:
                    print(f"\n[Pipeline] Query failed after {self.max_retries} retries — {failure}")

        unfolded = unfold_results(self.graph, raw_results)
        if v:
            print(f"\n{sep}")
            print("[Step 2] Unfolded results (URIs resolved to linked properties):")
            for r in unfolded[:5]:
                print("  ", r)
            if len(unfolded) > 5:
                print(f"  … and {len(unfolded) - 5} more.")

        # ── Step 3: Natural Language Answer ─────────────────────────────────
        if v:
            print(f"\n{sep}")
            print("[Step 3] Generating natural language answer…")
        answer = generate(query, sparql, unfolded)
        if v:
            print("[Step 3] Answer:")
            print(answer)

        return {
            "query":   query,
            "intent":  intent,
            "sparql":  sparql,
            "results": unfolded,
            "answer":  answer,
        }
