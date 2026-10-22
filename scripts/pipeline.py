"""
ARGUS KGQA pipeline: parse → SPARQL → answer, over a KG loaded once at init.

A Step 2 error or empty result is fed back to Step 1 for up to k re-parses.
Conversation history is opt-in (see Pipeline.keep_history). The system runs in
one configuration, THOROUGH: n parse candidates voted, retry budget k = 2,
history h = 2, and an LLM answer checked against the computed evidence
(n+1 to n+4 LLM calls). An answer that still fails the check after its one
regeneration, or an anomaly answer that does not lead with the verdict the AD-RT
check computed, is replaced by the template answer. A question the parser marks
unanswerable, or whose time window lies wholly outside the data, is declined
without running a query.

Two ablations (get_config, or --no-grounding / --no-error-correction):
  w/o grounding (grounding=False): the deterministic analysis layer still fetches
      each anomaly rule's raw readings but computes nothing, and the answer gets
      no pre-computed temporal/spatial/numeric facts; the LLM computes and judges
      from the rows and raw readings. SPARQL aggregates are unchanged; the raw
      readings count toward the row cap; the answer check, defined against the
      analysis output, is skipped (n+1 to n+3 LLM calls).
  w/o error correction (error_correction=False): one parse candidate, retry budget 0,
      and an LLM answer without the answer check (an anomaly answer not leading
      with the computed verdict still falls back to the template). Analysis and
      history are unchanged.
"""

from __future__ import annotations
import importlib
import json
import os
import time
from dataclasses import dataclass, replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


_sp = importlib.import_module("1_semantic_parser")
parse = _sp.parse
parse_voted = _sp.parse_voted

_sr = importlib.import_module("2_sparql_retriever")
build_sparql = _sr.build_sparql
validate_intent = _sr.validate_intent
execute      = _sr.execute
unfold_results = _sr.unfold_results

_ta = importlib.import_module("analysis_temp")
_domain = importlib.import_module("domain")

_ag = importlib.import_module("3_answer_generator")
generate = _ag.generate
prompt_row_stats = _ag.prompt_row_stats
template_answer = _ag.template_answer
check_answer = _ag.check_answer
ad_rt_verdict = _ag.ad_rt_verdict
leads_with = _ag.leads_with

_ek = importlib.import_module("analysis_ek")
evaluate_ad_rt = _ek.evaluate
fetch_ad_rt_raw = _ek.fetch_raw
rule_vocabulary = _ek.rule_vocabulary

_be = importlib.import_module("backend")
make_backend = _be.make_backend

# Result sets larger than this make the Step 3 call noticeably slow; nothing is
# dropped, the user is just told to expect the wait.
SLOW_PROMPT_ROWS = 500

# Result sets larger than this are treated as a failure (fed back to Step 1 to
# add an aggregation or a limit) rather than sent whole to the LLM. Unlike
# SLOW_PROMPT_ROWS, this one is a hard cutoff — as the underlying data grows
# (e.g. the live Postgres/Ontop backend), a "list all X" question with no
# aggregation and no LIMIT would otherwise scale its prompt with the whole
# dataset instead of with the answer.
MAX_RESULT_ROWS = int(os.environ.get("ARGUS_MAX_RESULT_ROWS", "1000"))

_DEFAULT_TTL_PATH = Path(__file__).resolve().parent.parent / "data" / "argus_readings.ttl"
DEFAULT_TTL = Path(os.environ.get("ARGUS_TTL_PATH", str(_DEFAULT_TTL_PATH)))


@dataclass(frozen=True)
class Config:
    name: str
    parse_candidates: int   # n; >1 votes over n parses (first turn only, retries parse once)
    max_retries: int        # k
    max_history: int        # h
    answer: str             # "template" | "llm" | "llm+check"
    grounding: bool = True  # False = w/o grounding ablation


CONFIGS = {
    # [disabled-config] begin — only THOROUGH is used; FAST and BALANCED kept for reference
    # "fast":     Config("fast",     parse_candidates=1, max_retries=0, max_history=1, answer="template"),
    # "balanced": Config("balanced", parse_candidates=1, max_retries=2, max_history=2, answer="llm"),
    # [disabled-config] end
    "thorough": Config("thorough", parse_candidates=3, max_retries=2, max_history=2, answer="llm+check"),
}


def get_config(name: str = "thorough", n: int | None = None, grounding: bool = True,
               error_correction: bool = True) -> Config:
    """THOROUGH; n overrides its number of parse candidates. grounding=False gives the
    w/o grounding ablation, error_correction=False the w/o error correction ablation: one
    parse candidate, no retries, and an LLM answer without the answer check (an
    anomaly answer still has to lead with the computed verdict)."""
    cfg = CONFIGS[name.lower()]
    if n is not None and cfg.parse_candidates > 1:
        cfg = replace(cfg, parse_candidates=n)
    if not error_correction:
        cfg = replace(cfg, name=cfg.name + "-noerrorcorrection", parse_candidates=1, max_retries=0,
                      answer="llm" if cfg.answer == "llm+check" else cfg.answer)
    if not grounding:
        cfg = replace(cfg, name=cfg.name + "-nogrounding", grounding=False)
    return cfg


MAX_SAMPLE_VALUES = 8
LATEST_TTL = float(os.environ.get("ARGUS_LATEST_TTL", "3600"))


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


def _drop_empty_aggregate(results: list[dict]) -> list[dict]:
    """An aggregate over nothing still returns a row (COUNT 0, AVG/SUM 0, MIN/MAX
    unbound). Treat "matched no values" as no results, so it is retried and,
    failing that, answered as "no data" rather than as a measured 0."""
    if (len(results) == 1 and "error" not in results[0]
            and str(results[0].get("n_values", results[0].get("count", ""))) == "0"):
        return []
    return results


def _is_failed(results: list[dict]) -> str | None:
    """Return a feedback string if results indicate failure, else None."""
    if not results:
        return "The SPARQL query returned 0 results. The query may be too restrictive or using wrong class/property names."
    if len(results) == 1 and "error" in results[0]:
        return f"SPARQL execution error: {results[0]['error']}"
    return None


def _is_oversized(results: list[dict]) -> bool:
    # Not fed back to Step 1 as a retry, even with neutral wording: tried that
    # and the model reached for a LIMIT anyway (its only obvious lever for
    # "too many rows"), and — because the retriever applies LIMIT at the
    # target-class subquery level, before joins/filters — it sampled 10
    # sensors *globally* and only 2 happened to match the requested site. The
    # answer confidently reported "2 sensors at baltanas" against a true count
    # of 28: worse than not answering. An oversized result set ends the turn
    # immediately instead.
    return len(results) > MAX_RESULT_ROWS


# Time windows (relative to the latest reading, against the data's range) are
# the temporal layer's (analysis_temp.py).
_apply_relative_time = _ta.apply_relative_time
_data_note = _ta.data_note
_outside_data = _ta.outside_data
_iso, _fmt = _ta.iso, _ta.fmt
_anchor_intent, _apply_anchor = _ta.anchor_intent, _ta.apply_anchor


def _decline(intent: dict | None, earliest: datetime | None, latest: datetime | None) -> str | None:
    """A question answered without a query: the parser found it asks for
    something the KG does not model, or its time window lies outside the data."""
    # An anomaly question is never declined here: whether a rule applies and can be
    # evaluated is the AD-RT step's call ("Cannot be determined" with its reason).
    reason = (intent or {}).get("unanswerable") if not (intent or {}).get("anomaly_check") else None
    if reason:
        detail = "" if reason is True else f": {str(reason).strip().rstrip('.')}"
        return f"Cannot be answered from the knowledge graph{detail}."
    return _outside_data(intent, earliest, latest)


def _with_note(answer: str, note: str) -> str:
    return f"{answer}\n\n{note}" if note else answer


def _oversized_answer(n_rows: int) -> str:
    return (
        f"This question matches {n_rows} rows, too many to answer directly "
        f"(limit: {MAX_RESULT_ROWS}). Try asking for a statistic (count/average/min/max) "
        f"or narrow it — e.g. a specific site, property, or a top-N."
    )


class Pipeline:
    def __init__(
        self,
        verbose: bool = True,
        ttl_path: str | Path | None = None,
        config: str | Config = "thorough",
        keep_history: bool = False,
        sparql_endpoint: str | None = None,
    ):
        self.verbose = verbose
        self.config = get_config(config) if isinstance(config, str) else config
        self.max_retries = self.config.max_retries
        # Conversation memory is opt-in: interactive sessions need it to resolve
        # follow-ups, batch runs must stay stateless so each query is reproducible.
        self.keep_history = keep_history
        self.max_history = self.config.max_history
        self.history: list[dict[str, Any]] = []
        ttl = Path(ttl_path) if ttl_path else DEFAULT_TTL

        # ── Step 0: Connect the query backend (local TTL or remote SPARQL) ──
        endpoint = sparql_endpoint or os.environ.get("ARGUS_SPARQL_ENDPOINT")
        if not endpoint and not ttl.exists() and not os.environ.get("HERIKGQA_OXIGRAPH_STORE"):
            print(f"[Step 0] WARNING: TTL file not found: {ttl}")
            print("[Step 0] Run `python scripts/0a_offline_readings.py --max-records 500` to fetch data first.")
        self.backend = make_backend(ttl_path=ttl, endpoint=endpoint)
        latest = self.latest_reading()  # fetched up front, so no question pays for it
        self.vocabulary = self._vocabulary()
        if self.verbose:
            print(f"[Step 0] Backend ready — {self.backend.describe()}.")
            print(f"[Step 0] Configuration: {self.config}")
            print(f"[Step 0] Latest reading (reference time for relative questions): {latest}")

    _LATEST_SPARQL = """PREFIX sosa: <http://www.w3.org/ns/sosa/>
SELECT (MAX(?t) AS ?latest) (MIN(?t) AS ?earliest) WHERE { ?o a sosa:Observation ; sosa:resultTime ?t . }"""

    def latest_reading(self) -> datetime | None:
        """Time of the newest observation (measured value) in the KG — the "now"
        relative times refer to; a reading with no observations does not count.
        Cached for ARGUS_LATEST_TTL seconds (default 3600, the live ingest
        interval: the newest reading only changes once per ingest cycle)."""
        return self._time_range()[1]

    def earliest_reading(self) -> datetime | None:
        """Time of the oldest observation in the KG (cached with the latest)."""
        return self._time_range()[0]

    def _time_range(self) -> tuple[datetime | None, datetime | None]:
        cached = getattr(self, "_latest_cache", None)
        if cached and time.monotonic() - cached[0] < LATEST_TTL:
            return cached[1]
        rows = self.backend.query(self._LATEST_SPARQL)
        bounds = []
        for key in ("earliest", "latest"):
            t = None
            if rows and "error" not in rows[0] and rows[0].get(key):
                t = datetime.fromisoformat(rows[0][key].replace("Z", "+00:00"))
                if t.tzinfo is None:
                    t = t.replace(tzinfo=timezone.utc)
            bounds.append(t)
        self._latest_cache = (time.monotonic(), tuple(bounds))
        return tuple(bounds)

    _VOCAB_SPARQL = """PREFIX argus: <http://www.argus-project.eu/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT DISTINCT ?cls ?label WHERE {
  { ?x a argus:ObservedProperty ; rdfs:label ?label . BIND("ObservedProperty" AS ?cls) }
  UNION { ?x a argus:Site ; rdfs:label ?label . BIND("Site" AS ?cls) }
  UNION { ?x a argus:Node ; rdfs:label ?label . BIND("Node" AS ?cls) }
}"""

    def _vocabulary(self) -> str | None:
        """The KG's own quantity and site labels for the parser, so a filter
        uses "soil_temperature", not "soil temperature" (which matches nothing)
        or "voltage" with contains (which also matches voltage_polynomial_4).
        Another domain (scripts/domain.py) supplies its own."""
        if not _domain.IS_ARGUS:
            return _domain.load("prompt").vocabulary(self.backend)
        rows = [r for r in self.backend.query(self._VOCAB_SPARQL) if "error" not in r]
        if not rows:
            return None
        by_cls: dict[str, list[str]] = {}
        for r in rows:
            by_cls.setdefault(r["cls"], []).append(r["label"])
        lines = ["Labels in this knowledge graph — filter on them verbatim with op equals (or in), choosing the "
                 "label that matches the user's wording (e.g. \"soil temperature\" → soil_temperature, "
                 "\"voltage\" → voltage, not voltage_1). A quantity named in the question is ONE label: use equals, "
                 "never contains (contains \"voltage\" also matches voltage_1 and voltage_polynomial_4). Use contains "
                 "only when the user explicitly asks for a family (\"all voltage channels\"). A name that appears "
                 "under Node.label is a sensor node, not a quantity."]
        lines += [f"{cls}.label: {', '.join(sorted(set(v)))}" for cls, v in sorted(by_cls.items())]
        # The expert rules per site come from the AD-RT layer that evaluates them.
        rules = rule_vocabulary(self.backend)
        if rules:
            lines.append(rules)
        return "\n".join(lines)

    def _question_vocabulary(self, query: str) -> str | None:
        """The vocabulary for one question: for a domain too large to list its entities
        (scripts/domain.py), the KG labels that the question may mean are added."""
        if _domain.IS_ARGUS:
            return self.vocabulary
        earlier = [t["query"] for t in self.history] if self.keep_history else []
        candidates = _domain.load("linker").candidates(query, earlier)
        return "\n\n".join(x for x in (self.vocabulary, candidates) if x) or None

    def _resolve_anchor(self, intent: dict) -> tuple[dict, str | None]:
        """Anchored time (analysis_temp): find the anchor event's time with its own
        query, then turn the "anchor" filters into bounds. No anchor: unchanged."""
        sub = _anchor_intent(intent)
        if sub is None:
            return intent, None
        problem = validate_intent(sub)
        if problem:
            return intent, f"Anchor: {problem}"
        rows = [r for r in execute(self.backend, build_sparql(sub)) if "error" not in r]
        t = next((v for r in rows for k, v in r.items() if k.endswith("resulttime") and v), None)
        return _apply_anchor(intent, t)

    def run(self, query: str) -> dict[str, Any]:
        v = self.verbose
        sep = "─" * 60
        latest = self.latest_reading()
        ref = _fmt(latest)[:-4] if latest else None
        window = None
        vocabulary = self._question_vocabulary(query)

        feedback = None
        intent = None
        sparql = None
        raw_results = []
        # Separated so a slow turn can be attributed to the LLM endpoint (steps 1
        # and 3) rather than to local query work (step 2).
        t_parse = t_query = t_answer = 0.0
        parse_calls = answer_calls = 0
        vote = None
        check_feedback = None
        decline = None
        template_fallback = False
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
            n = self.config.parse_candidates
            if attempt == 0 and n > 1:
                intent, vote = parse_voted(query, n, history=history, reference_time=ref,
                                           vocabulary=vocabulary)
                parse_calls += n
                if v:
                    print(f"[Step 1] Voted over {n} candidates: {vote['distinct']} distinct intent(s), "
                          f"winner has {vote['winner_votes']} vote(s).")
            else:
                intent = parse(query, feedback=feedback, history=history, reference_time=ref,
                                vocabulary=vocabulary)
                parse_calls += 1
            t_parse += time.perf_counter() - _t
            # AD questions: this fetches the applicable Policy rule(s), labelled
            # 2a (Step 2b below does the readings work). Normal questions: this
            # IS the readings retrieval, so it's labelled 2b directly.
            is_ad = bool(intent.get("anomaly_check"))
            step2_label = "Step 2a" if is_ad else "Step 2b"
            step2_topic = "Policy" if is_ad else intent.get("target_class", "Readings")
            if v:
                print("[Step 1] Intent:", json.dumps(intent, indent=2))
                if is_ad:
                    print("[Pipeline] Anomaly-check question — Step 2b will run extra AD-RT "
                          "rule queries after retrieval, so this may take a bit longer.")

            # ── Step 2a/2b: SPARQL Retrieval + Result Unfolding ──────────────
            _t = time.perf_counter()
            # An intent that cannot compile (e.g. an unsupported aggregation type)
            # is reported as an execution error, so it goes through the same retry.
            if intent.get("parse_error"):
                window, problem = None, intent["parse_error"]
            else:
                intent, anchor_problem = self._resolve_anchor(intent)
                intent, window, problem = _apply_relative_time(intent, latest)
                problem = anchor_problem or problem or validate_intent(intent)
            decline = _decline(intent, self.earliest_reading(), latest)
            if decline:
                sparql = f"# not run: {decline}"
                break
            sparql = f"# not compiled: {problem}" if problem else build_sparql(intent)
            if v:
                print(f"\n{sep}")
                print(f"[{step2_label}] SPARQL query on {step2_topic}:")
                print(sparql)

            raw_results = [{"error": problem}] if problem else _drop_empty_aggregate(execute(self.backend, sparql))
            t_query += time.perf_counter() - _t
            if v:
                print(f"[{step2_label}] {len(raw_results)} raw result(s) returned.")

            if _is_oversized(raw_results):
                break

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

        if decline:
            answer = _with_note(decline, _data_note(intent, latest, window))
            if v:
                print(f"\n{sep}\n[Pipeline] Declined without a query — {decline}")
            if self.keep_history:
                self.history.append({"query": query, "intent": intent,
                                     "result_summary": _summarize_results([])})
                del self.history[:-self.max_history]
            return {
                "query": query, "intent": intent, "sparql": sparql, "results": [], "answer": answer,
                "config": self.config.name, "declined_oversized": False, "declined": True,
                "llm_calls": parse_calls, "latency_s": round(time.perf_counter() - t_total, 2),
            }

        # Oversized ends the turn on the spot (see _is_oversized) — no retry,
        # no Step 2b or Step 3, just an explanation.
        if _is_oversized(raw_results):
            answer = _with_note(_oversized_answer(len(raw_results)), _data_note(intent, latest, window))
            if v:
                print(f"\n{sep}")
                print(f"[Pipeline] Giving up — {len(raw_results)} rows exceeds MAX_RESULT_ROWS "
                      f"({MAX_RESULT_ROWS}); not sending to the LLM.")
                print("[Step 3] Answer:")
                print(answer)
            if self.keep_history:
                self.history.append({
                    "query": query,
                    "intent": intent,
                    "result_summary": _summarize_results(raw_results),
                })
                del self.history[:-self.max_history]
            return {
                "query": query, "intent": intent, "sparql": sparql,
                "results": [], "answer": answer, "config": self.config.name, "declined_oversized": True,
                "llm_calls": parse_calls, "latency_s": round(time.perf_counter() - t_total, 2),
            }

        _t = time.perf_counter()
        unfolded = unfold_results(self.backend, raw_results)
        t_query += time.perf_counter() - _t
        if v:
            print(f"\n{sep}")
            print(f"[{step2_label}] Unfolded results (URIs resolved to linked properties):")
            for r in unfolded[:5]:
                print("  ", r)
            if len(unfolded) > 5:
                print(f"  … and {len(unfolded) - 5} more.")

        # ── Step 2b: Readings — AD-RT rule check (AD questions only) ────────
        # Runs each Policy rule's own windowed/per-sensor Observation queries
        # (see analysis_ek.RULE_SPECS) — a single generic query can't express
        # that, so it's a separate retrieval from Step 2a.
        ad_rt_summary = ""
        ad_rt_policies: list[dict[str, Any]] = []
        ad_rt_readings: list[str] = []
        ad_rt_raw_rows = 0
        if is_ad:
            _t = time.perf_counter()
            if self.config.grounding:
                ad_rt_result = evaluate_ad_rt(self.backend, intent)
            else:
                ad_rt_result = fetch_ad_rt_raw(self.backend, intent)
                ad_rt_raw_rows = ad_rt_result["n_rows"]
            ad_rt_summary = ad_rt_result["summary_text"]
            ad_rt_policies = ad_rt_result.get("policies", [])
            ad_rt_readings = ad_rt_result.get("readings", [])
            t_query += time.perf_counter() - _t
            if v and ad_rt_summary:
                print(f"\n{sep}")
                if self.config.grounding:
                    print("[Step 2b] SPARQL query on Readings (per matched rule, windowed/sensor-grouped):")
                    print(ad_rt_summary)
                else:
                    print(f"[Step 2b] Raw readings per matched rule (ablation, nothing computed): "
                          f"{ad_rt_raw_rows} row(s)")
                    print("\n".join(ad_rt_summary.splitlines()[:20]))

        # Ablation: the raw readings go to the LLM, so they count toward the same
        # row cap as Step 2's rows, handled the same way — declined, not truncated.
        if ad_rt_raw_rows and len(unfolded) + ad_rt_raw_rows > MAX_RESULT_ROWS:
            n_rows = len(unfolded) + ad_rt_raw_rows
            answer = _with_note(_oversized_answer(n_rows), _data_note(intent, latest, window))
            if v:
                print(f"\n[Pipeline] Giving up — {n_rows} rows (incl. {ad_rt_raw_rows} raw AD-RT readings) "
                      f"exceeds MAX_RESULT_ROWS ({MAX_RESULT_ROWS}); not sending to the LLM.")
            if self.keep_history:
                self.history.append({"query": query, "intent": intent,
                                     "result_summary": _summarize_results(unfolded)})
                del self.history[:-self.max_history]
            return {
                "query": query, "intent": intent, "sparql": sparql, "results": unfolded,
                "answer": answer, "is_ad": is_ad, "policies": ad_rt_policies, "readings": ad_rt_readings,
                "config": self.config.name, "llm_calls": parse_calls,
                "ad_rt_raw_rows": ad_rt_raw_rows, "declined_oversized": True,
                "latency_s": round(time.perf_counter() - t_total, 2),
            }

        # ── Step 3: Natural Language Answer ─────────────────────────────────
        if v:
            llm_rows, llm_chars = prompt_row_stats(unfolded)
            print(f"\n{sep}")
            print(f"[Step 3] Sending {llm_rows} row(s) / ~{llm_chars:,} chars to the LLM.")
            if llm_rows > SLOW_PROMPT_ROWS:
                print(f"[Step 3] Large result set — this answer may take a while.")
            print("[Step 3] Generating natural language answer…")
        _t = time.perf_counter()
        anomaly = bool(intent.get("anomaly_check"))
        # A follow-up's answer needs what it refers to (the current turn is added to
        # self.history only after this).
        followup_context = ({"earlier_questions": [t["query"] for t in self.history],
                             "interpretation": intent.get("explanation")}
                            if self.keep_history and self.history else {})
        if self.config.answer == "template":
            answer = template_answer(query, unfolded, ad_rt_summary=ad_rt_summary, anomaly_check=anomaly,
                                     with_grounding=self.config.grounding, reference_time=latest)
        else:
            answer = generate(query, sparql, unfolded, ad_rt_summary=ad_rt_summary,
                              anomaly_check=anomaly, verbose=v, with_grounding=self.config.grounding,
                              reference_time=latest, **followup_context)
            answer_calls += 1
            # THOROUGH: deterministic check against the evidence; one regeneration on failure.
            # Both of its criteria are defined against analysis output (the computed
            # verdict and analysis numbers), so the ablation skips it.
            if self.config.answer == "llm+check" and self.config.grounding:
                check_feedback = check_answer(answer, query, unfolded, ad_rt_summary=ad_rt_summary,
                                              anomaly_check=anomaly, reference_time=latest)
                if check_feedback:
                    if v:
                        print(f"[Step 3] Answer check failed — regenerating:\n{check_feedback}")
                    answer = generate(query, sparql, unfolded, ad_rt_summary=ad_rt_summary,
                                      anomaly_check=anomaly, verbose=False, feedback=check_feedback,
                                      reference_time=latest, **followup_context)
                    answer_calls += 1
                    # Still wrong after the one regeneration: the template answer,
                    # whose every number is the computed one.
                    if check_answer(answer, query, unfolded, ad_rt_summary=ad_rt_summary,
                                    anomaly_check=anomaly, reference_time=latest):
                        template_fallback = True
            # The computed verdict is not the LLM's to overrule (without the answer
            # check nothing else catches it): an answer leading with another verdict
            # is replaced.
            elif anomaly and self.config.grounding and not leads_with(answer, ad_rt_verdict(ad_rt_summary)):
                template_fallback = True
            if template_fallback:
                if v:
                    print("[Step 3] LLM answer contradicts the computed evidence — using the template answer.")
                answer = template_answer(query, unfolded, ad_rt_summary=ad_rt_summary, anomaly_check=anomaly,
                                         with_grounding=True, reference_time=latest)
        t_answer = time.perf_counter() - _t
        # Added after the answer check, so it never counts as an unsupported number.
        answer = _with_note(answer, _data_note(intent, latest, window))
        if v:
            print("[Step 3] Answer:")
            print(answer)
            total = time.perf_counter() - t_total
            llm = t_parse + t_answer
            print(f"\n[Timing] total {total:.1f}s = "
                  f"LLM {llm:.1f}s ({llm/total*100:.0f}%) "
                  f"[step1 {t_parse:.1f}s ×{parse_calls} call(s), step3 {t_answer:.1f}s ×{answer_calls} call(s)] "
                  f"+ local query {t_query:.2f}s")

        if self.keep_history:
            self.history.append({
                "query": query,
                "intent": intent,
                "result_summary": _summarize_results(unfolded),
            })
            del self.history[:-self.max_history]

        return {
            "query":    query,
            "intent":   intent,
            "sparql":   sparql,
            "results":  unfolded,
            "answer":   answer,
            "is_ad":    is_ad,
            "policies": ad_rt_policies,
            "readings": ad_rt_readings,
            "config":   self.config.name,
            "llm_calls": parse_calls + answer_calls,
            "vote":     vote,
            "check_failed": check_feedback,
            "template_fallback": template_fallback,
            "ad_rt_raw_rows": ad_rt_raw_rows,
            "declined_oversized": False,
            "latency_s": round(time.perf_counter() - t_total, 2),
        }

    def reset_history(self) -> None:
        self.history.clear()
