# ARGUS KGQA — Knowledge Graph Question Answering

Natural language question answering over real ARGUS sensor readings using
SOSA/ARGUS RDF vocabularies, SPARQL retrieval, and LLM-generated answers.

Default LLM endpoint: `https://ollama.fit.fraunhofer.de/api` with model `gpt-oss:120b`.

## Pipeline (4 steps with retry loop)

```
NL Query
   │
   ▼
[Step 1] Semantic Parser  (LLM)
         semantic_parser.py
         → structured intent JSON
         (target_class, filters, joins, aggregation)
   │
   ▼
[Step 2] KG Store
         data/argus_readings.ttl
         → rdflib in-memory Graph (SOSA/ARGUS triples)
   │
   ▼
[Step 3] SPARQL Retrieval
         sparql_retriever.py
         intent → SPARQL query → results
   │
   ├── results OK → continue
   └── empty / error → feedback to Step 1 (up to 2 retries)
   │
   ▼
[Step 4] NL Answer Generator  (LLM)
         answer_generator.py
         query + results + analysis → concise answer
```

## Quick start

```bash
pip install openai rdflib requests

export OPENAI_API_KEY="your_fraunhofer_api_key"

# 1. Fetch sensor data from the ARGUS API
python readings.py --max-records 500    # small test run
python readings.py                       # full dataset (~420k records)
python readings.py --resume              # incremental update

# 2. Run the pipeline
python demo.py
```

## File structure

| File | Role |
|------|------|
| `readings.py` | ARGUS API client + RDF knowledge graph builder. Fetches sensor readings, converts to SOSA/ARGUS triples, saves to `data/argus_readings.ttl` |
| `semantic_parser.py` | Step 1 — LLM parses NL query into a structured intent JSON |
| `sparql_retriever.py` | Step 3 — builds SPARQL from intent and executes against the graph |
| `answer_generator.py` | Step 4 — LLM generates a concise answer from query results |
| `geo_analysis.py` | Temporal and numeric analysis helpers for enriching LLM context |
| `pipeline.py` | Orchestrates all steps with a retry loop on failure |
| `demo.py` | Demo entry point with sample sensor data queries |
| `panoptes3.owl` | ARGUS Panoptes ontology (CIDOC-CRM, SOSA, GeoSPARQL) — reference only |
| `CIDOC_CRM_v7.1.3.rdf` | CIDOC-CRM v7.1.3 base ontology — reference only |

### Generated data (in `data/`, gitignored)

| File | Content |
|------|---------|
| `argus_readings.ttl` | RDF triples of sensor readings (Turtle format) |
| `argus_readings_state.json` | Download progress and deduplication state |
| `argus_readings.backup.ttl` | Backup of previous TTL before update |

## Data model (SOSA/ARGUS)

```
sosa:ObservationCollection          ← one API reading record
  ├── sosa:resultTime               (xsd:dateTime)
  ├── argus:hasSite → argus:Site    (rdfs:label: "baltanas", "delos", …)
  ├── sosa:madeBySensor → sosa:Sensor
  ├── argus:hasNode → argus:Node
  ├── argus:hasEngineeringUnit → argus:EngineeringUnit
  └── argus:hasObservation → sosa:Observation   (one per measured quantity)
        ├── sosa:observedProperty → argus:ObservedProperty  (rdfs:label: "temperature", …)
        ├── sosa:hasSimpleResult  (xsd:decimal)
        └── sosa:resultTime       (xsd:dateTime)
```

Known sites: baltanas, lucretili, delos, ranverso, schenkenberg, eurecat.

Known quantities include: temperature, voltage, displacement, rainfall, humidity,
soil_temperature, soil_water_potential, thermistor, potentiometer_displacement, pulse_counter.

## Running a query

```python
from pipeline import Pipeline

p = Pipeline()
result = p.run("How many readings are available per site?")
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

- *"How many readings are available per site?"*
- *"Which sensors are available at the baltanas site?"*
- *"What are the temperature values recorded at each site?"*
- *"Which displacement measurements are available?"*
- *"What are the latest 10 readings?"*
- *"What is the most recent reading timestamp for each site?"*
- *"How many sensors are deployed per site?"*
- *"Which physical quantities are measured at the delos site?"*

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_BASE_URL` | `https://ollama.fit.fraunhofer.de/api` | LLM API endpoint |
| `OPENAI_API_KEY` | `no-key` | API key for the LLM endpoint |
| `OLLAMA_MODEL` | `gpt-oss:120b` | Model name |

## readings.py usage

```bash
# Full download (all ~420k API records, takes a while)
python readings.py

# Limit to N records (for testing)
python readings.py --max-records 500

# Resume from where you left off (incremental update)
python readings.py --resume

# Resume with more overlap to avoid missing records
python readings.py --resume --overlap-pages 3

# Start from a specific page
python readings.py --start-page 100
```
