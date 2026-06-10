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
    # General asset queries
    "Show me all cultural heritage sites in Italy and their current condition.",
    "Find Byzantine-style heritage sites and list any threats associated with them.",
    # Temporal queries
    "Show all seismic measurements recorded after 2023-01-01, including their timestamps and sensor locations.",
    "Which sensor readings were taken at the Colosseum in 2022? Include dates and values.",
    # Spatial / location queries
    "List all sensors deployed in Greece with their coordinates and what they measured.",
    "Which measurements were taken at sites in Italy? Show sensor positions and observation times.",
    # Combined temporal + spatial
    "Show me all on-site measurements taken after 2022-01-01 at sites in Turkey or Croatia, with timestamps and sensor coordinates.",
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
