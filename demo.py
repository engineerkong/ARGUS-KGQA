"""
Demo — ARGUS KGQA Pipeline (4-step NL→KG→SPARQL→Answer).

Prerequisites:
    1. Fetch data first:
       python readings.py --max-records 500

    2. Set LLM endpoint:
       export OPENAI_API_KEY=<your_fraunhofer_key>
       export OLLAMA_BASE_URL=https://ollama.fit.fraunhofer.de/api
       export OLLAMA_MODEL=gpt-oss:120b

Run:
    python demo.py
"""

from pipeline import Pipeline

QUERIES = [
    # Per-site overview
    "How many readings are available per site?",
    "Which sensors are available at the baltanas site?",
    # Specific quantities
    "What are the temperature values recorded at each site?",
    "Which displacement measurements are available?",
    # Temporal queries
    "What are the latest 10 readings?",
    "What is the most recent reading timestamp for each site?",
    # Sensor / node inventory
    "How many sensors are deployed per site?",
    "Which physical quantities are measured at the delos site?",
]


def main():
    pipeline = Pipeline(verbose=True)

    for query in QUERIES:
        print("\n" + "=" * 70)
        print(f"QUERY: {query}")
        print("=" * 70)

        pipeline.run(query)
        print()


if __name__ == "__main__":
    main()
