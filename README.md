# ARGUS KGQA — Knowledge Graph Question Answering

Natural language question answering over real ARGUS sensor readings using
SOSA/ARGUS RDF vocabularies, SPARQL retrieval, and LLM-generated answers.

Default LLM endpoint: `https://ollama.fit.fraunhofer.de/api` with model `gpt-oss:120b`.

## Ontology architecture

The system is grounded in a formal OWL ontology stack. All schema knowledge
(class maps, property maps, graph connectivity, LLM prompt context) is
dynamically extracted from the OWL files — no hardcoded schema definitions
exist in the Python code.

```
W3C Standards                  ARGUS Project
─────────────                  ─────────────
SOSA/SSN ◄──────────┐
PROV-O               ├── panoptes3.owl (core project ontology)
CIDOC-CRM             │     Asset, Decision, Threat, Policy, ...
GeoSPARQL             │
OWL-Time              │
DUL ◄────────────────┘
                       │
                       ▼
                  panoptes3_extension.owl (sensor data extension)
                       argus:Site        → subClassOf sosa:FeatureOfInterest
                       argus:Node        → subClassOf sosa:Platform
                       argus:ObservedProperty → subClassOf sosa:ObservableProperty
                       argus:EngineeringUnit
                       + SOSA property declarations (madeBySensor, resultTime, ...)
                       │
                       ▼
                  data/argus_readings.ttl (instance data)
                       ex:site/baltanas   a argus:Site
                       ex:sensor/6dbe...  a sosa:Sensor
                       ex:reading/003...  a sosa:ObservationCollection
```

| Namespace | URI | Role |
|-----------|-----|------|
| `sosa:` | `http://www.w3.org/ns/sosa/` | W3C standard vocabulary for observations and sensors |
| `panoptes:` | `http://www.argus-project.eu/panoptes#` | Core ARGUS project ontology (cultural heritage, risk, decisions) |
| `argus:` | `http://www.argus-project.eu/ontology/` | Sensor data extension — classes and properties for IoT readings |
| `ex:` | `http://www.argus-project.eu/resource/` | Instance namespace — URIs for concrete data entities |

### What `ontology_schema.py` extracts from the OWL files

| Extraction | Used by | Purpose |
|------------|---------|---------|
| `CLASS_MAP` (short name → prefixed) | `sparql_retriever.py` | Map `"Site"` → `"argus:Site"` in SPARQL generation |
| `PROP_MAP` (short name → prefixed) | `sparql_retriever.py` | Map `"hasSite"` → `"argus:hasSite"` |
| `OBJECT_PROPS` | `sparql_retriever.py` | Distinguish object vs datatype properties |
| `PROP_DOMAIN` | `sparql_retriever.py` | Route joins through correct anchor class |
| Schema text | `semantic_parser.py` | LLM prompt: classes, properties, domain/range |
| Graph connectivity | `semantic_parser.py` | LLM prompt: direct edges, property ownership, indirect paths |
| Class list | `semantic_parser.py` | LLM prompt: valid `target_class` values |
| `SOSA`, `ARGUS`, `EX` | `readings.py` | Shared RDF namespace definitions |

## Pipeline

```
NL Query
   │
   ▼
[Step 1] Semantic Parser  (LLM)
         semantic_parser.py
         ontology schema + graph connectivity (auto-extracted from OWL)
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
         intent → SPARQL query → raw results
   │
   ├── results OK → continue
   └── empty / error → feedback to Step 1 (up to 2 retries)
   │
   ▼
[Step 3.5] Result Unfolding
           sparql_retriever.unfold_results()
           Resolves URI references by following all linked properties
           in the graph, replacing opaque URIs with human-readable
           labels and values. Nested URIs are resolved one level deep.
   │
   ▼
[Step 4] NL Answer Generator  (LLM)
         answer_generator.py
         query + unfolded results + analysis → concise answer
```

### Step 3.5 unfolding example

Raw SPARQL result (contains opaque URIs and IDs):
```json
{"observation": "http://...resource/observation/011573dbc...", "hassimpleresult": "20"}
```

After unfolding (URIs resolved, IDs dropped, only human-readable values remain):
```json
{
  "observation_hasSimpleResult": "20",
  "observation_observedProperty": "temperature",
  "observation_resultTime": "2026-05-13T01:30:00+00:00",
  "hassimpleresult": "20"
}
```

The unfolding step:
- Follows all linked properties of each URI in the graph
- Resolves nested URIs one level deep (e.g. `hasSite` URI → its `rdfs:label`)
- Drops values that are UUIDs, hex IDs, or ID-heavy paths (detected by pattern)
- Drops values longer than 200 characters (e.g. `rawJson`)

## Quick start

```bash
pip install openai rdflib requests

export OPENAI_API_KEY="your_fraunhofer_api_key"

# 1. Fetch sensor data from the ARGUS API
python readings.py --max-records 500    # small test run
python readings.py                       # full dataset (~420k records)
python readings.py --resume              # incremental update

# 2. Run the pipeline
python demo.py              # batch mode: run preset queries
python demo.py --online     # interactive mode: type queries in terminal
python demo.py --online --quiet  # interactive without debug output
```

## File structure

| File | Role |
|------|------|
| `readings.py` | ARGUS API client + RDF knowledge graph builder. Fetches sensor readings, converts to SOSA/ARGUS triples, saves to `data/argus_readings.ttl` |
| `ontology_schema.py` | Single source of truth — parses OWL files and exports all schema knowledge: namespaces, class/property maps, graph connectivity, LLM prompt text |
| `semantic_parser.py` | Step 1 — LLM parses NL query into a structured intent JSON |
| `sparql_retriever.py` | Step 3 + 3.5 — builds SPARQL from intent, executes against the graph, unfolds URI results |
| `answer_generator.py` | Step 4 — LLM generates a concise answer from unfolded results |
| `geo_analysis.py` | Temporal and numeric analysis helpers for enriching LLM context |
| `pipeline.py` | Orchestrates all steps with retry loop and result unfolding |
| `demo.py` | Demo entry point — batch mode (preset queries) or `--online` interactive mode |
| `panoptes3.owl` | Core ARGUS Panoptes ontology — integrates SOSA/SSN, PROV, CIDOC-CRM, GeoSPARQL, OWL-Time, DUL |
| `panoptes3_extension.owl` | Sensor data extension — defines `argus:` classes/properties and declares SOSA properties with domain/range, bridging standard and project vocabularies |
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
| `result["results"]` | Unfolded rows (URIs resolved to labels/values) |
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
