# ARGUS KGQA — Knowledge Graph Question Answering

Natural-language question answering over real ARGUS sensor readings, grounded in
the SOSA/ARGUS RDF vocabularies. A question is parsed into a structured intent,
compiled to SPARQL, executed against a knowledge graph, and turned into a concise
answer — with the statistics computed *in the query*, not guessed by the LLM.

Default LLM endpoint: `https://ollama.fit.fraunhofer.de/api`, model `gpt-oss:120b`.

## Requirements

- **Python 3.10+** — the codebase uses `X | None` type hints throughout.
- **Python packages:** `openai`, `rdflib`, `requests` (core, both modes); `psycopg[binary]` (only for `scripts/0b_online_ingest.py`, the deploy/Postgres path).
  ```bash
  pip install openai rdflib requests "psycopg[binary]"
  ```
- **Docker + Docker Compose** — deploy mode only (`postgres`, `ontop`, `ingest` in `obda/docker-compose.yml`). Not needed for dev mode.
- An **LLM API key** (`OPENAI_API_KEY`) for the configured endpoint — see [Environment variables](#environment-variables).

## Getting started

**Deploy — live data via Postgres + Ontop.** `ingest` creates the schema and
starts loading on its first cycle, then keeps polling the ARGUS API on a loop
(default hourly); `ontop` needs those tables to exist, so bring it up after:

```bash
docker compose -f obda/docker-compose.yml up -d postgres
docker compose -f obda/docker-compose.yml up -d ingest
docker compose -f obda/docker-compose.yml up -d ontop

export ARGUS_SPARQL_ENDPOINT=http://localhost:8081/sparql
export OPENAI_API_KEY="your_fraunhofer_api_key" # sk-39f498e276294f96a8cefdf9ac16fa12 (temporary)
python scripts/demo.py --online
```

**Dev — local snapshot, zero setup.** No Docker, no Postgres:

```bash
pip install openai rdflib requests
export OPENAI_API_KEY="your_fraunhofer_api_key"

python scripts/0a_offline_readings.py --max-records 500   # small local TTL snapshot
python scripts/demo.py --online
```

```python
from pipeline import Pipeline

p = Pipeline()
result = p.run("What is the average temperature at each site?")
print(result["answer"])
# result also holds: intent, sparql, results (unfolded rows), answer
```

## Pipeline

```
[Step 0] Query backend (connected once at startup)          backend.py
         local TTL in rdflib  OR  remote SPARQL endpoint (Ontop over Postgres)
   │
   ▼ (per query)
[Step 1] Semantic parser (LLM)                              1_semantic_parser.py
         NL query + ontology schema  →  intent JSON
   │
   ▼
[Step 2] SPARQL retrieval + unfolding                       2_sparql_retriever.py
         intent → SPARQL → rows → URIs unfolded to labels
   │     ├── OK → continue
   │     └── empty / error → feedback to Step 1 (up to 2 retries)
   ▼
[Analysis] Pre-computed stats over ALL rows                 geo_analysis.py
         temporal (recency/span) · spatial (distances) · numeric (per quantity)
   │
   ▼
[Step 3] Answer generator (LLM)                             3_answer_generator.py
         query + rows + analysis → concise answer
```

Design principle throughout: **the LLM reasons over data, it does not compute
over it.** Counts, averages, ranges and distances are produced by SPARQL or by
`geo_analysis`, never derived by the model from raw rows.

## Query backends

`backend.py` hides where the triples live behind one interface — `intent`, SPARQL
generation, prompts and analysis are unchanged either way. Switching is one env
var: unset `ARGUS_SPARQL_ENDPOINT` for local, set it for remote.

| Backend | Selected by | Use |
|---------|-------------|-----|
| `RdflibBackend` | default (a `data/argus_readings.ttl` file) | dev / small data, zero setup |
| `RemoteSparqlBackend` | `ARGUS_SPARQL_ENDPOINT` set | Ontop over Postgres, live/unbounded data |

```bash
python scripts/test_backend.py  # diagnose a remote endpoint layer by layer
```

URI *unfolding* (resolving a result URI to its `rdfs:label` and literals) batches
all URIs into one `VALUES` query via `backend.prefetch()`, so a remote endpoint is
one round-trip, not one per URI.

### Ontop OBDA (`obda/`)

The observation stream is unbounded and does not belong in an in-memory RDF graph.
Ontop maps a Postgres schema back to exactly the SOSA/ARGUS RDF the pipeline
queries, so the pipeline itself is untouched:

```
Postgres (SQL time series)  ──Ontop mapping (argus.obda)──►  virtual SPARQL endpoint
  sites / nodes / sensors                                     ex:reading a sosa:ObservationCollection
  observed_properties                                         argus:hasSite / hasObservation / …
  readings / observations                                     sosa:hasSimpleResult / resultTime
```

| File | Role |
|------|------|
| `obda/schema.sql` | Postgres DDL — topology tables + the `observations` time series + `ingest_state` |
| `obda/argus.obda` | Ontop mapping: SQL rows → the classes, predicates and `ex:` URIs `build_sparql` emits |
| `obda/argus.properties` | Ontop → Postgres JDBC connection |
| `obda/docker-compose.yml` | Postgres + Ontop endpoint + live `ingest` loop |

For very large deployments, make `observations` a TimescaleDB hypertable and add
continuous aggregates — the mapping and pipeline are unaffected.

### Live ingestion (`scripts/0b_online_ingest.py`)

Pulls new readings straight from the ARGUS API into Postgres on a loop — no TTL,
no JSONL sidecar, no local state file. Postgres is the only store; pagination
bookmarks live in its `ingest_state` table, and every insert is `ON CONFLICT DO
NOTHING` on the row's primary key, so re-walking the last few pages every cycle
(for late-arriving records) is always safe.

```bash
python scripts/0b_online_ingest.py --once   # single cycle, then exit
python scripts/0b_online_ingest.py          # loop forever, default 3600s
```

For local dev without Postgres, use `scripts/0a_offline_readings.py` instead — it
writes a TTL file for the in-memory `RdflibBackend`. The two don't share a data
store on purpose: `0a` is a disposable local snapshot for zero-setup testing, `0b`
is the always-current source of truth behind Ontop.

```bash
python scripts/0a_offline_readings.py                     # full download
python scripts/0a_offline_readings.py --max-records 500   # limit for testing
python scripts/0a_offline_readings.py --resume            # incremental update
python scripts/0a_offline_readings.py --enrich-geo-only   # refresh node coordinates from CSV
```

## Handling large result sets

- **Aggregate first (a correctness rule, not an optimisation).** For any statistic
  ("average", "total", "how many", "highest"), Step 1 emits an `aggregation` so the
  figure is computed inside SPARQL — detail rows pass through `SELECT DISTINCT`
  de-duplication, so averaging them afterwards would be wrong.
- **No silent truncation.** Every distinct row is sent to the LLM; Step 3's prompt
  takes counts/ranges/averages from the analysis block (computed over *all* rows),
  and Step 2 reports row/char counts so a slow turn is expected, not mysterious.

Raw API payloads are not queried by the pipeline, so they don't bloat the graph —
they live in an append-only JSONL sidecar (local/dev path only).

## Spatial & temporal analysis (`geo_analysis.py`)

Runs over the full result set before Step 3 and appends structured facts to the
prompt. Sections appear only when the data supports them:

- **Temporal** — full-timestamp recency (not day-rounded): newest, oldest, span.
- **Spatial** — when rows carry node coordinates: centroid, bounding box, altitude
  range, and haversine **distances** (nearest / farthest pairs). Node coordinates
  come from `material/ARGUS_nodes_<site>.csv`, attached to `argus:Node` instances
  at ingest time — drop a new CSV per site, no code change.
- **Numeric** — min/max/avg **grouped by observed property**, so a temperature range
  is never mixed with voltages into one meaningless figure.

## Follow-up questions

Interactive mode (`--online`) keeps a short conversation history so follow-ups
resolve against earlier turns; batch mode stays stateless so preset runs are
reproducible.

```
Q: how many sensors are in baltanas?              → 28
Q: among these, how many are about temperature?   → 21   (inherits the baltanas
                                                           set, adds a constraint)
```

Each turn's `(question → intent)` plus a compact result summary (row count and
columns, not the rows) is fed to the next parse. A follow-up is self-contained by
default; a newly named site/quantity **replaces** the old one, never adds to it.
`reset` clears history.

## Ontology architecture

All schema knowledge (class/property maps, prompt text, valid `target_class`
values) is extracted from the OWL files — no hardcoded schema in Python.

```
W3C Standards                  ARGUS Project
─────────────                  ─────────────
SOSA/SSN, PROV-O, CIDOC-CRM ──► panoptes3.owl (core project ontology)
GeoSPARQL, OWL-Time, DUL          Asset, Decision, Threat, Policy, …
                                     │
                                     ▼
                              panoptes3_extension.owl (sensor data extension)
                                argus:Site  → subClassOf sosa:FeatureOfInterest
                                argus:Node  → subClassOf sosa:Platform
                                argus:ObservedProperty → sosa:ObservableProperty
                                     │
                                     ▼
                              instance data (TTL file, or Postgres via Ontop)
                                ex:site/baltanas   a argus:Site
                                ex:reading/003…    a sosa:ObservationCollection
```

| Namespace | URI | Role |
|-----------|-----|------|
| `sosa:` | `http://www.w3.org/ns/sosa/` | W3C vocabulary for observations and sensors |
| `argus:` | `http://www.argus-project.eu/ontology/` | Sensor-data extension classes/properties |
| `ex:` | `http://www.argus-project.eu/resource/` | Instance URIs |

`ontology_schema.py` exposes two views: the **full** vocabulary drives SPARQL name
resolution, while the **prompt** view describes only `panoptes3_extension.owl` —
the 7 classes readings actually instantiate — so the base ontology's ~18 unused
classes are never offered as a `target_class` that could only return nothing.

## Data model (SOSA/ARGUS)

```
sosa:ObservationCollection          ← one API reading record
  ├── sosa:resultTime               (xsd:dateTime)
  ├── argus:hasSite → argus:Site    (rdfs:label: "baltanas", "delos", …)
  ├── sosa:madeBySensor → sosa:Sensor
  ├── argus:hasNode → argus:Node    (argus:latitude / longitude / altitude)
  └── argus:hasObservation → sosa:Observation   (one per measured quantity)
        ├── sosa:observedProperty → argus:ObservedProperty  ("temperature", …)
        ├── sosa:hasSimpleResult  (xsd:decimal)
        └── sosa:resultTime       (xsd:dateTime)
```

## File structure

| File | Role |
|------|------|
| `scripts/0a_offline_readings.py` | Dev — ARGUS API → local TTL (also node-coordinate enrichment, rawJson sidecar) |
| `scripts/0b_online_ingest.py` | Deploy — ARGUS API → Postgres directly, live loop, no local files |
| `scripts/1_semantic_parser.py` | Step 1 — LLM: NL query → intent JSON (+ follow-up history) |
| `scripts/2_sparql_retriever.py` | Step 2 — intent → SPARQL → rows → unfolded rows |
| `scripts/3_answer_generator.py` | Step 3 — LLM: rows + analysis → answer |
| `scripts/geo_analysis.py` | Spatial / temporal / grouped-numeric analysis |
| `scripts/backend.py` | Query backend abstraction (local rdflib / remote SPARQL) |
| `scripts/pipeline.py` | Orchestrates the steps, retry loop, timing, history |
| `scripts/demo.py` | Entry point — batch or `--online` |
| `scripts/test_readings.py` | Inspect raw readings before they become triples |
| `scripts/test_backend.py` | Diagnose a remote SPARQL endpoint |
| `scripts/test_llm.py` | Measure LLM endpoint latency |
| `scripts/ontology_schema.py` | Parses the OWL files; single source of schema truth |
| `material/panoptes3.owl`, `panoptes3_extension.owl` | Core + extension ontologies |
| `material/ARGUS_nodes_<site>.csv` | Per-node coordinates (lat/long/altitude) |
| `obda/` | Ontop OBDA setup — schema, mapping, connection, compose |

Generated data (in `data/`, gitignored, dev-only): `argus_readings.ttl` (graph),
`argus_readings_raw.jsonl` (raw payload sidecar), `argus_readings_state.json`
(download/dedup state), `argus_readings.backup.ttl`.

## Sample queries (`demo.py`)

Grouped by the capability they exercise:

- **Retrieval** — *"Which sensors are available at the baltanas site?"*, *"Which
  physical quantities are measured at the delos site?"*
- **Spatial** — *"Where are the sensor nodes at the baltanas site?"*, *"Which two
  nodes at baltanas are closest together?"*, *"…highest/lowest altitude?"*
- **Temporal** — *"What are the latest 10 readings?"*, *"What time period do the
  readings at baltanas cover?"*
- **Aggregation** — *"What is the average temperature at each site?"*, *"How does the
  voltage range at delos compare to baltanas?"*

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_BASE_URL` | `https://ollama.fit.fraunhofer.de/api` | LLM API endpoint |
| `OPENAI_API_KEY` | `no-key` | API key for the LLM endpoint |
| `OLLAMA_MODEL` | `gpt-oss:120b` | Model name |
| `ARGUS_SPARQL_ENDPOINT` | *(unset → local TTL)* | Remote SPARQL endpoint (Ontop) |
| `ARGUS_TTL_PATH` | `data/argus_readings.ttl` | Local graph file |
| `ARGUS_PG_DSN` | `postgresql://argus:argus@localhost:5432/argus` | Postgres DSN for `0b_online_ingest.py` |
| `ARGUS_INGEST_INTERVAL` | `3600` | Seconds between live ingest cycles |
| `ARGUS_INGEST_OVERLAP_PAGES` | `2` | API pages re-walked each cycle, for late-arriving records |
| `ARGUS_KEEP_RAW_JSON` | *(unset)* | `1` re-embeds rawJson in the graph (legacy) |
| `ARGUS_LLM_TIMEOUT` | `120` | LLM request timeout (seconds) |
