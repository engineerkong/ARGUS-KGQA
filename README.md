# ARGUS KGQA — Knowledge Graph Question Answering

Natural language question answering over cultural heritage data using the
ARGUS Panoptes ontology (`panoptes3.owl`), an in-memory RDF triple store,
SPARQL retrieval, and LLM-generated answers.

Default LLM endpoint: `https://ollama.fit.fraunhofer.de/api` with model `gpt-oss:120b`.

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
         panoptes3.owl + cultural-heritage triples
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
         query + SPARQL + results + geo analysis → natural language answer
```

## File structure

| File | Role |
|------|------|
| `panoptes3.owl` | ARGUS Panoptes ontology (CIDOC-CRM, SOSA, GeoSPARQL, …) |
| `CIDOC_CRM_v7.1.3.rdf` | CIDOC-CRM v7.1.3 base ontology |
| `kg_store.py` | Loads ontology + populates in-memory RDF graph with instance data |
| `semantic_parser.py` | Step 1 — LLM parses NL query into a structured intent |
| `sparql_retriever.py` | Step 3 — builds and executes a SPARQL query from the intent |
| `answer_generator.py` | Step 4 — LLM generates a grounded NL answer from results |
| `geo_analysis.py` | Spatial/temporal helpers (haversine distances, proximity clustering, recency ranking) |
| `pipeline.py` | Orchestrates all four steps |
| `demo.py` | Demo entry point with sample queries |
| `readings.py` | Client for the live ARGUS readings API |

## Setup

```bash
pip install openai rdflib requests

export OPENAI_API_KEY="your_fraunhofer_api_key"

# Optional overrides (defaults shown):
export OLLAMA_BASE_URL="https://ollama.fit.fraunhofer.de/api"
export OLLAMA_MODEL="gpt-oss:120b"

python demo.py
```

## Running a query

```python
from pipeline import Pipeline

p = Pipeline()
result = p.run("Which assets are at risk from earthquakes?")
print(result["answer"])
```

The `result` dict contains all intermediate outputs:

| Key | Content |
|-----|---------|
| `result["intent"]` | Parsed intent JSON from Step 1 |
| `result["sparql"]` | Generated SPARQL query from Step 3 |
| `result["results"]` | Raw rows returned by the SPARQL query |
| `result["answer"]` | Final natural language answer from Step 4 |

## Sample queries (demo.py)

- *"Show me all cultural heritage sites in Italy and their current condition."*
- *"Find Byzantine-style heritage sites and list any threats associated with them."*
- *"Show all seismic measurements recorded after 2023-01-01, including their timestamps and sensor locations."*
- *"Which sensor readings were taken at the Colosseum in 2022? Include dates and values."*
- *"List all sensors deployed in Greece with their coordinates and what they measured."*
- *"Which measurements were taken at sites in Italy? Show sensor positions and observation times."*
- *"Show me all on-site measurements taken after 2022-01-01 at sites in Turkey or Croatia, with timestamps and sensor coordinates."*

## KG instance data (kg_store.py)

The graph is populated with example cultural heritage sites and associated data:

| Asset | Country | Style | Condition |
|-------|---------|-------|-----------|
| Parthenon | Greece | Classical | fair |
| Hagia Sophia | Turkey | Byzantine | good |
| Colosseum | Italy | Roman | fair |
| Dubrovnik Old Town | Croatia | Medieval | good |
| Pompeii | Italy | Roman | damaged |
| Alhambra | Spain | Islamic | good |

Each asset has associated Events, Threats, RiskAssessments, Measurements, and CulturalDocumentation nodes.

## Live readings API (readings.py)

Fetches live sensor readings from `http://api.argusservices.athenarc.gr/api/readings`.

API has 401,808 records across 26,788 pages (June 10.)

```python
from readings import fetch_page, fetch_readings, fetch_all

# Single page (includes meta/pagination info)
page = fetch_page(1)

# Lazy iterator — yields individual records across pages
for record in fetch_readings(max_pages=5):
    print(record["ts"], record["site"], record["payload"])

# All records as a list (401k+ records total — use max_pages to limit)
records = fetch_all(max_pages=2)
```

Each record contains: `ts`, `site`, `sensor_id`, `node_id`, `node_name`, `node_label`,
`sensor_name`, `sensor_model`, `payload` (measurement values), `eng_unit_name`, and more.

Run standalone to fetch and print the first page:

```bash
python readings.py
```

## Geo analysis (geo_analysis.py)

`geo_analysis.analyze()` enriches SPARQL results with:

- **Distances** to a pilot site (haversine, km)
- **Proximity clusters** — groups of results within a configurable threshold (default 300 km)
- **Recency ranking** — results ordered by observation timestamp
- **`summary_text`** — a pre-formatted block passed directly to the LLM in Step 4

The default pilot site is the Parthenon (37.9715°N, 23.7267°E), configurable via `Pipeline(pilot_lat=…, pilot_lon=…)`.
