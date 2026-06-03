"""
Demo — ARGUS KGQA Pipeline (4-step NL→KG→SPARQL→Answer).

Setup:
    export OPENAI_API_KEY=<your_fraunhofer_key>
    export OLLAMA_BASE_URL=https://ollama.fit.fraunhofer.de/api   # default
    export OLLAMA_MODEL=gpt-oss:120b                               # default

Run:
    python demo.py
"""

from pipeline import Pipeline

QUERIES = [
    "Show me all cultural heritage sites in Italy and their current condition.",
    "Which assets are at risk from earthquakes and what is their risk magnitude?",
    "Find Byzantine-style heritage sites and list any threats associated with them.",
    "What measurements have been taken for the Parthenon?",
]


def main():
    pipeline = Pipeline(verbose=True)

    for query in QUERIES:
        print("\n" + "=" * 70)
        print(f"QUERY: {query}")
        print("=" * 70)

        result = pipeline.run(query)

        print("\n── FINAL ANSWER ──")
        print(result["answer"])
        print()


if __name__ == "__main__":
    main()
