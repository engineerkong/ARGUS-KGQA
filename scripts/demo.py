"""
Demo runner for the ARGUS KGQA pipeline.

Needs data (0_readings.py) and an LLM endpoint (OPENAI_API_KEY,
OLLAMA_BASE_URL, OLLAMA_MODEL).

    python scripts/demo.py           # preset queries, no conversation history
    python scripts/demo.py --online  # interactive, follow-up questions supported
"""

import argparse
from pipeline import Pipeline

QUERIES = [
    # ── General retrieval ────────────────────────────────────────────────
    "How many readings are available per site?",
    "Which sensors are available at the baltanas site?",
    "Which displacement measurements are available?",
    "How many sensors are deployed per site?",
    "Which physical quantities are measured at the delos site?",

    # ── Spatial — node coordinates, centroid/bbox, haversine distances ───
    "Where are the sensor nodes at the baltanas site?",
    "Which node at baltanas has the highest altitude, and which the lowest?",
    "How far apart are the two most distant nodes at baltanas?",
    "Which two nodes at baltanas are closest together?",

    # ── Temporal — full-timestamp recency, oldest/newest/span ────────────
    "What are the latest 10 readings?",
    "What is the most recent reading timestamp for each site?",
    "What time period do the readings at baltanas cover?",

    # ── Numeric — per-quantity ranges, never a single global min/max ─────
    "What are the temperature values recorded at each site?",
    "What physical quantities are measured at baltanas and what are their value ranges?",
    "How does the voltage range at delos compare to baltanas?",
]


def run_batch(pipeline: Pipeline):
    for query in QUERIES:
        print("\n" + "=" * 70)
        print(f"QUERY: {query}")
        print("=" * 70)
        pipeline.run(query)
        print()


def run_online(pipeline: Pipeline):
    print("ARGUS KGQA — Interactive Mode")
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
    parser = argparse.ArgumentParser(description="ARGUS KGQA demo")
    parser.add_argument("--online", action="store_true",
                        help="Interactive mode: type queries in terminal")
    parser.add_argument("--quiet", action="store_true",
                        help="Hide intermediate pipeline steps")
    args = parser.parse_args()

    # History only in interactive mode — batch queries stay independent so the
    # preset run is reproducible and one query cannot contaminate the next.
    pipeline = Pipeline(verbose=not args.quiet, keep_history=args.online)

    if args.online:
        run_online(pipeline)
    else:
        run_batch(pipeline)


if __name__ == "__main__":
    main()
