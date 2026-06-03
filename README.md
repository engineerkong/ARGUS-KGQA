# ARGUS KGQA — Knowledge Graph Question Answering

Natural language question answering over cultural heritage data using the
ARGUS Panoptes ontology (`panoptes3.owl`), an in-memory RDF triple store,
SPARQL retrieval, and LLM-generated answers.

Default endpoint: `https://ollama.fit.fraunhofer.de/api` with model `gpt-oss:120b`.

## Pipeline (4 steps)

```
NL Query
   │
   ▼
[Step 1] Semantic Parser  (LLM)
         semantic_parser.py
         → structured intent JSON
         (target_class, filters, joins)
   │
   ▼
[Step 2] KG Instance Store
         kg_store.py
         panoptes3.owl + dummy cultural-heritage triples
         → rdflib in-memory Graph
   │
   ▼
[Step 3] SPARQL Retrieval
         sparql_retriever.py
         intent → SPARQL query → results list
   │
   ▼
[Step 4] NL Answer Generator  (LLM)
         answer_generator.py
         query + SPARQL + results → natural language answer
```

## File structure

| File | Role |
|------|------|
| `panoptes3.owl` | ARGUS Panoptes ontology (CIDOC-CRM, SOSA, GeoSPARQL, …) |
| `kg_store.py` | Loads ontology + adds dummy cultural-heritage instance data |
| `semantic_parser.py` | Step 1 — LLM parses NL query into a structured intent |
| `sparql_retriever.py` | Step 3 — builds and executes a SPARQL query from the intent |
| `answer_generator.py` | Step 4 — LLM generates a grounded NL answer from results |
| `pipeline.py` | Orchestrates all four steps |
| `demo.py` | Demo entry point with sample queries |

## Setup

```bash
pip install openai rdflib

export OPENAI_API_KEY="your_fraunhofer_api_key"

# Optional overrides (defaults shown):
export OLLAMA_BASE_URL="https://ollama.fit.fraunhofer.de/api"
export OLLAMA_MODEL="gpt-oss:120b"

python demo.py
```

## Sample queries

```python
from pipeline import Pipeline

p = Pipeline()
result = p.run("Which assets are at risk from earthquakes?")
print(result["answer"])
```

The `result` dict contains all intermediate outputs:
- `result["intent"]`  — parsed intent from Step 1
- `result["sparql"]`  — generated SPARQL query from Step 3
- `result["results"]` — raw rows returned by the SPARQL query
- `result["answer"]`  — final natural language answer from Step 4

## Dummy KG data

`kg_store.py` populates the graph with example cultural heritage sites:

| Asset | Country | Style | Condition |
|-------|---------|-------|-----------|
| Parthenon | Greece | Classical | fair |
| Hagia Sophia | Turkey | Byzantine | good |
| Colosseum | Italy | Roman | fair |
| Dubrovnik Old Town | Croatia | Medieval | good |
| Pompeii | Italy | Roman | damaged |
| Alhambra | Spain | Islamic | good |

Each asset has associated Events, Threats, RiskAssessments, and Measurements.
