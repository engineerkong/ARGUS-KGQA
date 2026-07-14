"""
Demo — ARGUS KGQA Pipeline (Steps 0–3: KG → Parse → SPARQL → Answer).

Prerequisites:
    1. Fetch data first:
       python scripts/0_readings.py --max-records 500

    2. Set LLM endpoint:
       export OPENAI_API_KEY=<your_fraunhofer_key>
       export OLLAMA_BASE_URL=https://ollama.fit.fraunhofer.de/api
       export OLLAMA_MODEL=gpt-oss:120b

Run:
    python scripts/demo.py              # batch mode: run preset queries
    python scripts/demo.py --online     # interactive mode: type queries in terminal
"""

import argparse
from pipeline import Pipeline

QUERIES = [
    "How many readings are available per site?",
    "Which sensors are available at the baltanas site?",
    "What are the temperature values recorded at each site?",
    "Which displacement measurements are available?",
    "What are the latest 10 readings?",
    "What is the most recent reading timestamp for each site?",
    "How many sensors are deployed per site?",
    "Which physical quantities are measured at the delos site?",
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
    print("Type a question and press Enter. Type 'quit' or Ctrl+C to exit.\n")

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

    pipeline = Pipeline(verbose=not args.quiet)

    if args.online:
        run_online(pipeline)
    else:
        run_batch(pipeline)


if __name__ == "__main__":
    main()
