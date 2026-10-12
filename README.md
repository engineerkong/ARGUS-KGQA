# ARGUS KGQA — Knowledge Graph Question Answering

Natural-language question answering over real ARGUS sensor readings, grounded in
the SOSA/ARGUS RDF vocabularies. A question is parsed into a structured intent,
compiled to SPARQL, executed against a knowledge graph, and turned into a concise
answer — with the statistics computed *in the query*, not guessed by the LLM.

Default LLM endpoint: `https://chat.kiconnect.nrw/api/v1` (KI:connect NRW), model `openai-gpt-oss-120b` (override with `OLLAMA_BASE_URL` / `OLLAMA_MODEL`; the key goes in `OPENAI_API_KEY`). The experiments and the baselines (TextRAG, Interactive-KBQA) all use `openai-gpt-oss-120b`; the endpoint allows 3 concurrent requests.

## Requirements

- **Python 3.10+** — the codebase uses `X | None` type hints throughout.
- **Python packages:** `openai`, `rdflib`, `requests` (core, both modes); `psycopg[binary]` (only for the deploy/Postgres ingest scripts).
  ```bash
  pip install openai rdflib requests "psycopg[binary]"
  ```
- **Docker + Docker Compose** — deploy mode only (`postgres`, `ontop`, `ingest`, `governance_ingest` in `obda/docker-compose.yml`). Not needed for dev mode.
- An **LLM API key** (`OPENAI_API_KEY`) for the configured endpoint.

## Getting started

**Deploy — live data via Postgres + Ontop.** `ingest`/`governance_ingest` create
the schema and start loading on their first cycle; `ontop` needs those tables to
exist, so bring it up after:

```bash
docker compose -f obda/docker-compose.yml up -d postgres
docker compose -f obda/docker-compose.yml up -d ingest governance_ingest
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

## Time anchoring

"Now" is the newest observation in the knowledge graph, not the wall clock —
readings arrive late and a snapshot never moves. The pipeline looks it up at
start-up (cached for `ARGUS_LATEST_TTL` seconds, default 3600, the ingest
interval) and uses it three ways:

- **Relative windows** ("last 24 hours", "past week"): the parser only emits
  `relative_time: {amount, unit}`; the pipeline turns it into an absolute
  `resultTime` filter ending at the newest observation. The parser is also
  given that time to resolve calendar phrases ("yesterday") into dates.
- **Recency** in `analysis_geo` (days ago) is measured from it.
- **Every answer ends with the data it rests on**, appended by code, e.g.
  `(Data: readings from 2026-08-11 09:15 UTC to 2026-08-12 09:15 UTC.)`.

AD-RT rule windows were already anchored to the newest matching reading (or
to the date the question names).

## Configurations

How much LLM work a turn may spend is one of three configurations, chosen with
`--config` (default `balanced`, the original behaviour):

|                    | `fast`   | `balanced` | `thorough`    |
|--------------------|----------|------------|---------------|
| Parse candidates   | 1        | 1          | n (voted)     |
| Retry budget k     | 0        | 2          | 2             |
| History turns h    | 1        | 2          | 2             |
| Answer             | template | LLM        | LLM + check   |
| LLM calls          | 1        | 2 to 4     | n+1 to n+4    |

- **Voted parse**: one greedy and n−1 sampled parses (temperature
  `ARGUS_VOTE_TEMPERATURE`, default 0.7) run in parallel; the most frequent
  intent wins, ties go to the greedy one. Retries always parse once.
- **Template answer**: no LLM — the AD-RT verdict; or the analysis fact that
  answers the question (a named pair's distance, the node nearest to a named
  node, the nodes within a radius, …); or else the result rows plus the
  pre-computed analysis, rendered as text.
- **Check**: every number and timestamp in the answer must appear (up to
  rounding) in the results, the analysis or the AD-RT summary, and an anomaly
  answer must lead with the computed verdict; on failure the answer is
  regenerated once with the problems as feedback, and if it still fails, the
  template answer is returned.
- **Verdict**: in every configuration with analysis, an anomaly answer that does
  not lead with the computed verdict is replaced by the template answer.
- **Declines without a query**: a question the parser marks `unanswerable`
  (it needs something the KG does not model, e.g. a river), or whose time
  window lies wholly outside the readings, is answered "Cannot be answered"
  directly.

```bash
python scripts/demo.py --online --config fast
python scripts/demo.py --online --config thorough --n 3
```

**Ablation `--no-analysis`** (any configuration; analysis is on by default)
removes the deterministic analysis layer: no temporal/spatial/numeric summary,
and for anomaly questions the rule windows' raw readings are fetched as usual
but nothing is computed — no per-sensor grouping, window statistics or
threshold comparison. Statistics are still SPARQL aggregates. Raw readings
count toward the 1,000-row cap (declined, not truncated, like any oversized
result).

| | `fast` | `balanced` | `thorough` |
|---|---|---|---|
| w/o analysis | rows only; anomaly → "Cannot be determined" | LLM computes and judges from rows and raw readings | as `balanced`, voted parse; answer check skipped (it checks against analysis output), n+1 to n+3 calls |

```python
from pipeline import Pipeline, get_config
p = Pipeline(config=get_config("thorough", n=3))
r = p.run("What is the maximum temperature recorded at Schenkenberg?")
r["answer"], r["llm_calls"], r["latency_s"]
```

## Pipeline

```
[Step 0] Query backend (connected once at startup)          backend.py
         local TTL in rdflib  OR  remote SPARQL endpoint (Ontop over Postgres)
   │
   ▼ (per query)
[Step 1] Semantic parser (LLM)                              1_semantic_parser.py
         NL query + ontology schema → intent JSON (target_class, anomaly_check, as_of)
   │
   ▼
[Anomaly] AD-RT expert-rule check — only when anomaly_check  analysis_ek.py
         intent's site+quantity → applicable Policy rule(s) → each rule's own
         windowed/per-sensor Observation queries → EXCEEDS/within verdict
   │
   ▼
[Step 2] SPARQL retrieval + unfolding                       2_sparql_retriever.py
         intent → SPARQL → rows → URIs unfolded to labels
   │     ├── OK → continue
   │     └── empty / error → feedback to Step 1 (up to 2 retries)
   ▼
[Analysis] Pre-computed stats over ALL rows                 analysis_geo.py
         temporal (recency/span; analysis_temp.py) · spatial (distances)
         · numeric (per quantity)
   │
   ▼
[Step 3] Answer generator (LLM)                             3_answer_generator.py
         query + rows + analysis + AD-RT verdict → concise answer
```

Each deterministic layer also states its own rules for the LLM: the query
compiler (`2_sparql_retriever.py`), the temporal layer (`analysis_temp.py`:
time filters, buckets, relative windows), the spatial layer (`analysis_geo.py`)
and the AD-RT rule evaluation (`analysis_ek.py`) each export `PARSER_*` texts
and an `ANSWER_GUIDE`, which the parser and answer prompts are assembled from —
so the prompts describe exactly what the code does.

Design principle throughout: **the LLM reasons over data, it does not compute
over it.** Counts, averages, ranges, distances and threshold comparisons are
produced by SPARQL, `analysis_geo.py` or `analysis_ek.py` — never derived by
the model from raw rows.

## Live ingestion

`scripts/0b_online_ingest.py` pulls new readings from the ARGUS API into
Postgres on a loop; `scripts/0c_ingest_governance_pg.py` does the same for the
AD-RT expert-rule data (threats/policies/decisions/assets), upserting by the
API's own id since — unlike readings — it's mutable reference data, not an
append-only stream. `scripts/0a_offline_readings.py` is the local-dev
counterpart of both: it writes a TTL snapshot instead of touching Postgres.
`obda/` holds the Postgres schema and the Ontop mapping that projects those
tables back into the same SOSA/ARGUS RDF the pipeline queries either way.

## Node coordinates

Node lat/long/altitude come from `material/ARGUS_nodes.csv`. Editing that CSV
doesn't retroactively update either backend — new nodes pick it up on their
next ingest automatically, but existing rows need a one-off backfill (SQL for
the Postgres path, or `0a_offline_readings.py --enrich-geo-only` for the local
TTL path).

## Handling large result sets

Aggregate statistics are always computed inside SPARQL, never from
already-fetched rows — detail rows pass through `SELECT DISTINCT`
de-duplication, so averaging them client-side would be wrong. Every distinct
row is still sent to the LLM (no silent truncation); very large result sets
are rejected with an explanation instead, asking for an aggregation or a
narrower filter.

## Spatial & temporal analysis

`analysis_geo.py` runs over the full result set before Step 3 and appends
structured facts to the prompt, appearing only when the data supports them:
temporal recency (newest/oldest/span), spatial stats (centroid, bounding box,
altitude range, nearest/farthest node pairs) when rows carry coordinates, and
numeric ranges grouped by observed property so a temperature range is never
mixed with voltages into one meaningless figure.

## Follow-up questions

Interactive mode (`--online`) keeps a short conversation history so follow-ups
resolve against earlier turns (e.g. "among these, how many are about
temperature?"); batch mode stays stateless so preset runs are reproducible. A
follow-up is self-contained by default — a newly named site/quantity replaces
the old one rather than adding to it. `reset` clears history.

## Anomaly detection

A question asking for a yes/no verdict against a known threshold ("has X
exceeded threshold", "is there an anomaly") is flagged by Step 1
(`anomaly_check: true`) and routed to `analysis_ek.py`, which mirrors
AD-RT's expert-rule table (`AD-RT/RT/rules.py`) rather than recomputing it
from scratch: each rule's own column matcher, computation shape (direct
threshold / windowed sum-mean-range / z-score / rate-of-change / normalized
step-offset / composite) and threshold are looked up, then evaluated against
real Observation data — grouped by physical sensor first, since a site can
have several sensors sharing one quantity label, and combined the same way
AD-RT combines them (elementwise max/min across sensors), never by pooling
raw readings across sensors into one series. A question can also name a
specific point in time ("on 2026-05-15") via the intent's `as_of` field,
evaluated against readings as of that day instead of the latest available.

## Ontology architecture

All schema knowledge (class/property maps, prompt text, valid `target_class`
values) is extracted from the OWL files at load time — no hardcoded schema in
Python. `panoptes3.owl` is the core project ontology (built on SOSA/SSN,
PROV-O, CIDOC-CRM, …); `panoptes3_extension.owl` adds the sensor-reading
classes (`Site`, `Node`, `ObservedProperty`, …) and the governance classes
(`Policy`, `Threat`, `Decision`, `Asset`) that have real instances, so the
LLM-facing prompt only ever offers classes that can actually return data.

## Data model

One API reading becomes a `sosa:ObservationCollection` carrying its site,
sensor, node and timestamp, with one `sosa:Observation` per measured quantity
(observed property, value, unit). Governance data (Policy/Threat/Decision/
Asset) lives alongside it, linked to `Site` via `appliesToSite`/`atSite`.
