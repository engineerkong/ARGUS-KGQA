"""
Batch runner for experiments: one result JSON per question.

    python scripts/run_eval.py --questions trial20.json --out results/balanced
    python scripts/run_eval.py --questions q.json --out results/thorough --config thorough --n 3
    python scripts/run_eval.py --questions q.json --out results/balanced-noanalysis --no-analysis

Question file: [{"id", "question", "history"?: [{"question", ...}], ...}].
For a follow-up, the earlier questions in "history" are first run through the
same Pipeline with conversation memory on, so the follow-up resolves against
the system's own earlier turns; only the final question is timed and saved.
Finished ids are skipped on re-runs.
"""

import argparse
import json
from pathlib import Path

from pipeline import CONFIGS, Pipeline, get_config


def main():
    ap = argparse.ArgumentParser(description="ARGUS KGQA batch evaluation")
    ap.add_argument("--questions", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--config", choices=list(CONFIGS), default="balanced")
    ap.add_argument("--n", type=int, default=3)
    ap.add_argument("--no-analysis", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    cfg = get_config(args.config, n=args.n, analysis=not args.no_analysis)
    pipeline = Pipeline(verbose=args.verbose, config=cfg, keep_history=True)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    for d in json.loads(Path(args.questions).read_text()):
        path = out / f"{d['id']}.json"
        if path.exists():
            continue
        pipeline.reset_history()
        try:
            for h in d.get("history") or []:
                pipeline.run(h["question"])
            r = pipeline.run(d["question"])
        except Exception as e:  # e.g. an LLM endpoint timeout: leave it for the next run
            print(f"{d['id']} FAILED: {type(e).__name__}: {e}", flush=True)
            continue
        res = {
            **d,
            "prediction": r["answer"],
            "config": r.get("config"),
            "intent": r.get("intent"),
            "sparql": r.get("sparql"),
            "n_result_rows": len(r.get("results") or []),
            "llm_calls": r.get("llm_calls"),
            "latency_s": r.get("latency_s"),
            "declined_oversized": r.get("declined_oversized"),
            "ad_rt_raw_rows": r.get("ad_rt_raw_rows"),
            "vote": r.get("vote"),
            "check_failed": r.get("check_failed"),
            "template_fallback": r.get("template_fallback"),
            "declined": r.get("declined"),
        }
        path.write_text(json.dumps(res, indent=1, ensure_ascii=False, default=str))
        print(f"{d['id']} ({res['latency_s']}s, {res['llm_calls']} LLM calls): {res['prediction'][:200]}", flush=True)


if __name__ == "__main__":
    main()
