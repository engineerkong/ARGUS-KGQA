"""
Demo runner for AD-RT anomaly-check questions specifically — exercises the
Step 2a (Policy) / Step 2b (Readings, per-rule windowed/sensor-grouped) split
in pipeline.py. Same setup requirements as demo.py (data + LLM endpoint).

    python scripts/demo_ad.py           # preset AD-RT queries, no history
    python scripts/demo_ad.py --online  # interactive, follow-up questions supported
"""

import argparse
from pipeline import Pipeline

QUERIES = [
    # ── Real data on both sides — full Step 2a/2b split visible, non-trivial
    #    verdicts (R9a EXCEEDS, R9b within) ─────────────────────────────────
    "Has the temperature range at lucretili exceeded its threshold?",
    "Has the temperature at lucretili changed too rapidly in the last hour?",

    # ── Real data, but the readings are quiet (within threshold) ──────────
    "Is the rainfall at lucretili currently anomalous?",
    "Has the 7-day rainfall at ranverso exceeded its threshold?",

    # ── Step 2a finds the rule/threshold; Step 2b honestly reports no
    #    matching sensor data (documented coverage gap, not a bug) ─────────
    "Is the wind speed at delos anomalous?",
    "Has soil moisture at baltanas exceeded threshold?",
    "Is there a crack step anomaly at lucretili?",

    # ── Step 2a finds a rule that is deliberately left unevaluated
    #    (double-smoothed crossing-count, too risky to approximate) ───────
    "Is the humidity at delos currently anomalous?",
]


def run_batch(pipeline: Pipeline):
    for query in QUERIES:
        print("\n" + "=" * 70)
        print(f"QUERY: {query}")
        print("=" * 70)
        pipeline.run(query)
        print()


def run_online(pipeline: Pipeline):
    print("ARGUS KGQA — AD-RT Demo (Interactive Mode)")
    print("Follow-up questions are supported (e.g. 'what about delos?').")
    print("Type 'reset' to forget the conversation, 'quit' or Ctrl+C to exit.\n")

    while True:
        try:
            query = input("Question: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break

        if not query:
            continue
        if query.lower() in ("quit", "exit", "q"):
            print("Bye.")
            break
        if query.lower() in ("reset", "clear"):
            pipeline.reset_history()
            print("Conversation history cleared.\n")
            continue

        print()
        result = pipeline.run(query)
        print("\n" + "─" * 60)
        print(f"Answer: {result['answer']}")
        print("─" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(description="ARGUS KGQA AD-RT demo")
    parser.add_argument("--online", action="store_true",
                        help="Interactive mode: type queries in terminal")
    parser.add_argument("--quiet", action="store_true",
                        help="Hide intermediate pipeline steps")
    args = parser.parse_args()

    pipeline = Pipeline(verbose=not args.quiet, keep_history=args.online)

    if args.online:
        run_online(pipeline)
    else:
        run_batch(pipeline)


if __name__ == "__main__":
    main()
