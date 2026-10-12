"""
Step 3 — turn results into an answer. The LLM receives the query, the SPARQL,
the full result rows and the pre-computed spatial/temporal analysis, and is
asked to reason over them rather than reformat them.
"""

from __future__ import annotations
import json
import os
import re
from openai import OpenAI

from analysis_geo import analyze
import analysis_geo as _spatial
import analysis_ek as _anomaly
import analysis_temp as _temporal
import importlib
_query = importlib.import_module("2_sparql_retriever")

BASE_URL = os.environ.get("OLLAMA_BASE_URL", "https://chat.kiconnect.nrw/api/v1")
API_KEY  = os.environ.get("OPENAI_API_KEY", "no-key")
MODEL    = os.environ.get("OLLAMA_MODEL", "openai-gpt-oss-120b")

# The SDK default is a 600s timeout with silent retries, so a stalled endpoint
# hangs the pipeline for many minutes with no output.
LLM_TIMEOUT     = float(os.environ.get("ARGUS_LLM_TIMEOUT", "120"))
LLM_MAX_RETRIES = int(os.environ.get("ARGUS_LLM_MAX_RETRIES", "2"))

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        http_client = None
        # Temporary escape hatch for an expired cert on the remote endpoint —
        # unset/false keeps normal verification. Never enable this by default.
        insecure = os.environ.get("ARGUS_OPENAI_COMPATIBLE_INSECURE_SSL", "").strip().lower() in {"1", "true", "yes", "on"}
        if insecure:
            import httpx
            http_client = httpx.Client(verify=False)
        _client = OpenAI(
            base_url=BASE_URL, api_key=API_KEY,
            timeout=LLM_TIMEOUT, max_retries=LLM_MAX_RETRIES,
            http_client=http_client,
        )
    return _client

# The layer-specific rules come from the layers that produce what the answer
# reports: query statistics (2_sparql_retriever), time (analysis_temp),
# spatial facts (analysis_geo), AD-RT verdicts (analysis_ek).
SYSTEM = f"""You are a concise sensor data analyst for the ARGUS cultural heritage monitoring system.

You are given a user question, SPARQL results, and a numeric summary.

Rules:
- Answer the question directly in 1-3 short sentences.
- Include key numbers from the results (counts, values, site names).
- If results are tabular, present them as a compact list or table.
- If results are empty or contain an error, say so in one sentence and suggest a rephrased query.
- If the question asks about something the results do not contain (something the knowledge graph does not model, e.g. ownership or costs), say it cannot be answered from the knowledge graph — do not answer a different question with the rows you have.
- Do NOT output URIs or internal identifiers — use human-readable names and labels only.
- Do NOT explain the SPARQL query, the ontology, or how the system works.
- Do NOT add follow-up suggestions or next steps.

{_spatial.ANSWER_GUIDE}

{_query.ANSWER_GUIDE}

{_temporal.ANSWER_GUIDE}

{_anomaly.ANSWER_GUIDE}
"""


# Ablation (w/o analysis): same prompt, except that nothing is pre-computed
# any more — no spatial/temporal/numeric summary and no AD-RT verdict, only the
# rule definitions and raw readings. SPARQL aggregates are still computed in
# the query, so the instruction to report them stays.
SYSTEM_NO_ANALYSIS = SYSTEM.replace(
    "You are given a user question, SPARQL results, and a numeric summary.",
    "You are given a user question and SPARQL results. No numeric summary or analysis is provided.",
).replace(
    """- Otherwise the rows are a de-duplicated listing, so do NOT compute an average, total or record count from them; give the values, ranges or examples the rows support and leave it there.""",
    """- Otherwise the rows are a de-duplicated listing, so do NOT compute an average, total or record count from them.
- Anything else the question needs — newest/oldest timestamps and time spans, distances between nodes from their coordinates, centroids, value ranges — compute it yourself from the rows.""",
).replace(
    """- If a message includes a section starting "AD-RT rule check", that verdict (EXCEEDS/within a threshold) was computed in Python, not by you — report it as-is, do NOT recompute or second-guess it by comparing raw numbers yourself.""",
    """- If a message includes a section starting "AD-RT rules and raw readings", it lists each applicable rule (definition and threshold) and the raw readings retrieved for it. No verdict has been computed: evaluate each rule yourself from those readings and decide whether it fires.""",
)
assert SYSTEM_NO_ANALYSIS.count("compute it yourself") == 1 and "No verdict has been computed" in SYSTEM_NO_ANALYSIS


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


def generate(query: str, sparql: str, results: list, ad_rt_summary: str | None = None,
             anomaly_check: bool = False, verbose: bool = False, feedback: str | None = None,
             with_analysis: bool = True, reference_time=None,
             earlier_questions: list[str] | None = None, interpretation: str | None = None) -> str:
    """with_analysis=False is the w/o-analysis ablation: no pre-computed
    summary, and ad_rt_summary holds rule definitions + raw readings
    (analysis_ek.fetch_raw) instead of verdicts (analysis_ek.evaluate).
    For a follow-up, earlier_questions and the parser's interpretation say what
    the question refers to: without them "and on the following day?" was read
    against the already-shifted date in the query and shifted a second time."""
    client = _get_client()

    deduped = _dedupe(results)
    results_text = json.dumps(deduped, indent=2, ensure_ascii=False)

    context = ""
    if earlier_questions:
        context = ("This is a follow-up question. Earlier questions in this conversation:\n"
                   + "\n".join(f"- {q}" for q in earlier_questions)
                   + (f"\nHow the follow-up was resolved into the query below: {interpretation}" if interpretation else "")
                   + "\nThe query's filters (dates, site, quantity) already apply what the follow-up refers to "
                     "(e.g. \"the following day\" is already the date in the query): answer for the data retrieved, "
                     "without shifting it again.\n\n")
    user_msg = (
        context +
        f"User question:\n{query}\n\n"
        f"SPARQL query executed:\n```sparql\n{sparql}\n```\n\n"
        f"Results — all {len(deduped)} distinct rows ({len(results)} total):\n{results_text}"
    )
    if with_analysis:
        analysis = analyze(results, now=reference_time, query=query)
        user_msg += f"\n\nPre-computed spatial & temporal analysis:\n{analysis['summary_text']}"
        if verbose:
            print(f"[Step 3] Pre-computed spatial & temporal analysis:\n{analysis['summary_text']}")

    # AD-RT expert-rule threshold check — precomputed by the caller (Step 2b,
    # see pipeline.py) and just passed through here; Step 3 only assembles the
    # prompt and asks the model to report it, never queries or computes it.
    if ad_rt_summary:
        user_msg += f"\n\n{ad_rt_summary}"
        if anomaly_check:
            user_msg += "\n\n(This is a yes/no anomaly check — lead your answer with Yes/No/Cannot be determined.)"

    # THOROUGH: a previous answer failed check_answer(); say what was wrong.
    if feedback:
        user_msg += f"\n\n--- YOUR PREVIOUS ANSWER FAILED A CHECK ---\n{feedback}\nWrite a corrected answer."

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM if with_analysis else SYSTEM_NO_ANALYSIS},
            {"role": "user",   "content": user_msg},
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()


# ── Verdict, template answer (FAST) and answer check (THOROUGH) ─────────────

_FIRED = re.compile(r"→ (EXCEEDS|BELOW|FIRES)")
_WITHIN = re.compile(r"→ within")


def leads_with(answer: str, verdict: str) -> bool:
    """Whether the answer opens with the verdict, ignoring markdown emphasis."""
    return re.sub(r"^[\s*_#>\"']+", "", answer or "").lower().startswith(verdict.lower())


def ad_rt_verdict(ad_rt_summary: str | None) -> str:
    """The Yes/No/Cannot-be-determined verdict implied by analysis_ek's summary:
    Yes if any evaluated rule fired, No if rules were evaluated and none fired."""
    if ad_rt_summary and _FIRED.search(ad_rt_summary):
        return "Yes"
    if ad_rt_summary and _WITHIN.search(ad_rt_summary):
        return "No"
    return "Cannot be determined"


_TEMPLATE_ROWS = 10


def template_answer(query: str, results: list, ad_rt_summary: str | None = None,
                    anomaly_check: bool = False, with_analysis: bool = True, reference_time=None) -> str:
    """Deterministic answer with no LLM call: the AD-RT verdict, or the result
    rows plus the pre-computed analysis, rendered as text. Without the analysis
    layer nothing computes a verdict, so an anomaly question cannot be decided
    and only the applicable rules are listed."""
    if anomaly_check and not with_analysis:
        rules = [l.strip()[2:] for l in (ad_rt_summary or "").splitlines() if l.startswith("  - ")]
        n_readings = sum(1 for l in (ad_rt_summary or "").splitlines() if l.startswith("    ") and "|" in l)
        detail = (f" Applicable rules: {' '.join(rules)} ({n_readings} raw readings retrieved, "
                  f"no verdict computed.)") if rules else (" " + ad_rt_summary if ad_rt_summary else "")
        return f"Cannot be determined.{detail}"
    if anomaly_check:
        rules = [l.strip() for l in (ad_rt_summary or "").splitlines()[1:] if l.strip()]
        detail = (" " + " ".join(rules)) if rules else (" " + ad_rt_summary if ad_rt_summary else "")
        return f"{ad_rt_verdict(ad_rt_summary)}.{detail}"

    if len(results) == 1 and "error" in results[0]:
        return "The question could not be answered: the query could not be built or executed."
    if not results:
        return "No matching data was found in the knowledge graph for this question."

    # The analysis picked the fact that answers this question: that is the answer.
    focus = analyze(results, now=reference_time, query=query)["focus"] if with_analysis else []
    if focus:
        return "\n".join(f.strip() for f in focus)

    rows = _dedupe(results)
    if len(rows) == 1 and len(rows[0]) == 1:
        (k, v), = rows[0].items()
        return f"{k.replace('_', ' ')}: {v}."

    lines = [f"{len(rows)} result(s):"]
    for row in rows[:_TEMPLATE_ROWS]:
        lines.append("- " + ", ".join(f"{k.replace('_', ' ')}: {v}" for k, v in row.items()))
    if len(rows) > _TEMPLATE_ROWS:
        lines.append(f"- … and {len(rows) - _TEMPLATE_ROWS} more.")
    facts = ([l for l in analyze(results, now=reference_time, query=query)["summary_text"].splitlines()[1:] if l.strip()]
             if with_analysis else [])
    if facts:
        lines.append("Analysis:")
        lines += facts[:15]
    return "\n".join(lines)


# Unsigned on purpose: "2026-10-08" must yield 10 and 8, the same numbers as
# "8 October 2026". "18,507" is a thousands separator, not a decimal comma.
_NUMBER = re.compile(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?")


def _numbers(text: str) -> list[str]:
    return [m.replace(",", "") for m in _NUMBER.findall(text or "")]


def _supported(num: str, evidence: list[float]) -> bool:
    # The answer may round: 18.4381 supports "18.44", "18.4" and "18".
    x = float(num)
    decimals = len(num.split(".")[1]) if "." in num else 0
    tol = 0.5 * 10 ** -decimals + 1e-9
    return any(abs(x - e) <= tol or (e and abs(x - e) / abs(e) <= 0.005) for e in evidence)


_DASHES = re.compile(r"[\u2010-\u2015\u2212]")
_TIMESTAMP = re.compile(r"(\d{4}-\d{2}-\d{2})(?:T|\s+at\s+|\s+)(\d{2}:\d{2})")


def _timestamps(text: str) -> set[str]:
    text = _DASHES.sub("-", re.sub(r"[\u00a0\u202f\u2009]", " ", text or ""))
    return {f"{d} {t}" for d, t in _TIMESTAMP.findall(text)}


def check_answer(answer: str, query: str, results: list, ad_rt_summary: str | None = None,
                 anomaly_check: bool = False, reference_time=None) -> str | None:
    """Deterministic check of an LLM answer against the evidence it was given.
    Returns None when it passes, else feedback for one regeneration:
      - every number in the answer must appear (up to rounding) in the result
        rows, the pre-computed analysis, the AD-RT summary or the question;
      - every timestamp (date and time) must appear in that evidence too;
      - an anomaly answer must lead with the verdict the AD-RT check computed."""
    problems = []

    if anomaly_check:
        expected = ad_rt_verdict(ad_rt_summary)
        if not leads_with(answer, expected):
            problems.append(f"The AD-RT rule check computed the verdict '{expected}', "
                            f"but the answer does not start with it.")

    evidence_text = "\n".join([
        json.dumps(results, ensure_ascii=False), analyze(results, now=reference_time, query=query)["summary_text"],
        ad_rt_summary or "", query,
    ])
    wrong_times = sorted(_timestamps(answer) - _timestamps(evidence_text))
    if wrong_times:
        problems.append("These timestamps in the answer are not in the results: " + ", ".join(wrong_times)
                        + ". Copy timestamps from the results.")
    evidence = [float(n) for n in _numbers(evidence_text)]
    unsupported = [n for n in dict.fromkeys(_numbers(answer)) if not _supported(n, evidence)]
    if unsupported:
        problems.append("These numbers in the answer are not in the results or the analysis: "
                        + ", ".join(unsupported) + ". Report only values that are in them.")

    return "\n".join(problems) or None
