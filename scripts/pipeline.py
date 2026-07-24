"""
ARGUS KGQA pipeline: parse → SPARQL → answer, over a KG loaded once at init.

A Step 2 error or empty result is fed back to Step 1 for up to max_retries
re-parses. Conversation history is opt-in (see Pipeline.keep_history).
"""

from __future__ import annotations
import importlib
import json
import os
import time
from pathlib import Path
from typing import Any


_sp = importlib.import_module("1_semantic_parser")
parse = _sp.parse

_sr = importlib.import_module("2_sparql_retriever")
build_sparql = _sr.build_sparql
execute      = _sr.execute
unfold_results = _sr.unfold_results

_ag = importlib.import_module("3_answer_generator")
generate = _ag.generate
prompt_row_stats = _ag.prompt_row_stats

_be = importlib.import_module("backend")
make_backend = _be.make_backend

# Result sets larger than this make the Step 3 call noticeably slow; nothing is
# dropped, the user is just told to expect the wait.
SLOW_PROMPT_ROWS = 500

_DEFAULT_TTL_PATH = Path(__file__).resolve().parent.parent / "data" / "argus_readings.ttl"
DEFAULT_TTL = Path(os.environ.get("ARGUS_TTL_PATH", str(_DEFAULT_TTL_PATH)))
MAX_RETRIES = 2
MAX_HISTORY = 2


MAX_SAMPLE_VALUES = 8


def _summarize_results(results: list[dict[str, Any]]) -> dict[str, Any]:
    # Compact shape of a result set for follow-up context: how big it was and
    # which columns it had. Deliberately not the rows themselves — a follow-up
    # almost always asks about an attribute that was never projected, so the
    # rows cannot answer it and would only waste tokens.
    if not results or (len(results) == 1 and "error" in results[0]):
        return {"row_count": 0, "columns": [], "sample_values": [], "sample_of": None}

    columns = sorted({k for row in results for k in row})
    label_col = next((c for c in columns if c.endswith("_label")), columns[0] if columns else None)

    values: list[str] = []
    for row in results:
        v = row.get(label_col)
        if v is not None and str(v) not in values:
            values.append(str(v))
        if len(values) >= MAX_SAMPLE_VALUES:
            break

    return {"row_count": len(results), "columns": columns,
            "sample_values": values, "sample_of": label_col}


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
        keep_history: bool = False,
        max_history: int = MAX_HISTORY,
        sparql_endpoint: str | None = None,
    ):
        self.verbose = verbose
        self.max_retries = max_retries
        # Conversation memory is opt-in: interactive sessions need it to resolve
        # follow-ups, batch runs must stay stateless so each query is reproducible.
        self.keep_history = keep_history
        self.max_history = max_history
        self.history: list[dict[str, Any]] = []
        ttl = Path(ttl_path) if ttl_path else DEFAULT_TTL

        # ── Step 0: Connect the query backend (local TTL or remote SPARQL) ──
        endpoint = sparql_endpoint or os.environ.get("ARGUS_SPARQL_ENDPOINT")
        if not endpoint and not ttl.exists():
            print(f"[Step 0] WARNING: TTL file not found: {ttl}")
            print("[Step 0] Run `python scripts/0a_offline_readings.py --max-records 500` to fetch data first.")
        self.backend = make_backend(ttl_path=ttl, endpoint=endpoint)
        if self.verbose:
            print(f"[Step 0] Backend ready — {self.backend.describe()}.")

    def run(self, query: str) -> dict[str, Any]:
        v = self.verbose
        sep = "─" * 60

        feedback = None
        intent = None
        sparql = None
        raw_results = []
        # Separated so a slow turn can be attributed to the LLM endpoint (steps 1
        # and 3) rather than to local query work (step 2).
        t_parse = t_query = t_answer = 0.0
        parse_calls = 0
        t_total = time.perf_counter()

        for attempt in range(1 + self.max_retries):
            # ── Step 1: Semantic Parsing ─────────────────────────────────────
            history = self.history if self.keep_history else None
            if v:
                print(f"\n{sep}")
                if attempt == 0:
                    print(f"[Step 1] Semantic parsing: {query!r}")
                    if history:
                        prior = ", ".join(repr(t["query"]) for t in history)
                        print(f"[Step 1] Context from {len(history)} prior turn(s): {prior}")
                else:
                    print(f"[Step 1] Retry {attempt}/{self.max_retries} — re-parsing with feedback")
            _t = time.perf_counter()
            intent = parse(query, feedback=feedback, history=history)
            t_parse += time.perf_counter() - _t
            parse_calls += 1
            if v:
                print("[Step 1] Intent:", json.dumps(intent, indent=2))

            # ── Step 2: SPARQL Retrieval + Result Unfolding ──────────────────
            _t = time.perf_counter()
            sparql = build_sparql(intent)
            if v:
                print(f"\n{sep}")
                print("[Step 2] SPARQL query:")
                print(sparql)

            raw_results = execute(self.backend, sparql)
            t_query += time.perf_counter() - _t
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

        _t = time.perf_counter()
        unfolded = unfold_results(self.backend, raw_results)
        t_query += time.perf_counter() - _t
        if v:
            print(f"\n{sep}")
            print("[Step 2] Unfolded results (URIs resolved to linked properties):")
            for r in unfolded[:5]:
                print("  ", r)
            if len(unfolded) > 5:
                print(f"  … and {len(unfolded) - 5} more.")

        # ── Step 3: Natural Language Answer ─────────────────────────────────
        if v:
            llm_rows, llm_chars = prompt_row_stats(unfolded)
            print(f"\n{sep}")
            print(f"[Step 3] Sending {llm_rows} row(s) / ~{llm_chars:,} chars to the LLM.")
            if llm_rows > SLOW_PROMPT_ROWS:
                print(f"[Step 3] Large result set — this answer may take a while.")
            print("[Step 3] Generating natural language answer…")
        _t = time.perf_counter()
        answer = generate(query, sparql, unfolded)
        t_answer = time.perf_counter() - _t
        if v:
            print("[Step 3] Answer:")
            print(answer)
            total = time.perf_counter() - t_total
            llm = t_parse + t_answer
            print(f"\n[Timing] total {total:.1f}s = "
                  f"LLM {llm:.1f}s ({llm/total*100:.0f}%) "
                  f"[step1 {t_parse:.1f}s ×{parse_calls} call(s), step3 {t_answer:.1f}s] "
                  f"+ local query {t_query:.2f}s")

        if self.keep_history:
            self.history.append({
                "query": query,
                "intent": intent,
                "result_summary": _summarize_results(unfolded),
            })
            del self.history[:-self.max_history]

        return {
            "query":   query,
            "intent":  intent,
            "sparql":  sparql,
            "results": unfolded,
            "answer":  answer,
        }

    def reset_history(self) -> None:
        self.history.clear()
