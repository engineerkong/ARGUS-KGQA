# HeriKGQA: Grounded Knowledge-Graph Question Answering over Cultural Heritage Sensor Data

Code, data snapshot and benchmark of the paper *HeriKGQA: Grounded Knowledge-Graph Question
Answering over Cultural Heritage Sensor Data*. HeriKGQA answers
natural-language questions over sensor readings from five heritage sites of the ARGUS project
(Baltanas, Delos, Lucretili, Ranverso, Schenkenberg) and powers the chat assistant of the
[ARGUS Heritage Intelligence Platform](https://argus.athenarc.gr/).

Its principle: **the LLM reasons over data but never computes over it.** The LLM only parses a
question into an ontology-constrained intent and phrases the answer; every number comes from
deterministically compiled SPARQL or from a grounding layer of pre-implemented spatial, temporal
and anomaly-rule functions.

| System | Accuracy | Basic | Spatial | Temporal | Anomaly | Follow-up | Median latency |
|---|---|---|---|---|---|---|---|
| TextRAG | 37.6 | 17 | 63 | 26 | 63 | 19 | 3.9 s |
| TableRAG | 48.2 | 76 | 22 | 57 | 26 | 60 | 8.9 s |
| Interactive-KBQA | 80.8 | 95 | 54 | 91 | 79 | 85 | 46.7 s |
| **HeriKGQA** | **99.0** | 99 | 100 | 98 | 99 | 99 | 12.0 s |
| w/o grounding | 86.8 | 99 | 83 | 98 | 66 | 88 | 11.4 s |
| w/o error correction | 97.6 | 97 | 100 | 98 | 99 | 94 | 8.1 s |

500 benchmark questions, all systems with `gpt-oss-120b` (Table 1 of the paper).

## Repository layout

| Path | Content |
|---|---|
| `scripts/` | the method (`pipeline.py` and the modules below), entry points (`run_eval.py`, `demo.py`, `demo_ad.py`), data ingestion (`0a`–`0c`, `snapshot_add_lorawan.py`, `build_lookups.py`) and benchmark generation (`build_benchmark.py`, `build_verification.py`, `build_user_questions.py`) |
| `obda/` | the virtual knowledge graph: Postgres schema, Ontop mapping onto PANOPTES (`argus.obda`), Docker services |
| `material/` | ontology (`panoptes3.owl`, `panoptes3_extension.owl`), benchmark (`benchmark_500.*`), user questions (`benchmark_user.json`), the SQL verification of every reference (`verify/`), node and channel lookups used to build the snapshot |
| `data/` | the experiment snapshot: a `pg_dump` of the database every experiment runs on, in parts (see `data/README.md`) |
| `domains/multitq/` | the port to MultiTQ (Appendix E of the paper): ontology, parser prompt and examples, entity linker, loader |

## Requirements

- Python 3.10+ and `pip install -r requirements.txt` (`openai`, `httpx`, `rdflib`, `requests`,
  `urllib3`, `psycopg[binary]`); `pyoxigraph` for the MultiTQ domain.
- Docker with Docker Compose, for Postgres and Ontop (`obda/docker-compose.yml`).
- An OpenAI-compatible LLM endpoint. The code defaults to KI:connect NRW
  (`https://chat.kiconnect.nrw/api/v1`, model `openai-gpt-oss-120b`), the endpoint of the paper;
  set `OLLAMA_BASE_URL` and `OLLAMA_MODEL` for another one, and the key in `OPENAI_API_KEY`.
  Never write a key into a file of this repository.

## Reproducing the experiments

1. Start Postgres, restore the snapshot into the database `argus_snapshot` (commands in
   `data/README.md`), and serve it with Ontop on port 8082:

   ```bash
   docker compose -f obda/docker-compose.yml up -d postgres
   # restore data/argus_snapshot_v2.dump into argus_snapshot (data/README.md)
   docker compose -f obda/docker-compose.yml up -d ontop_snapshot
   ```

2. Run HeriKGQA and its two ablations on the benchmark:

   ```bash
   export ARGUS_SPARQL_ENDPOINT=http://localhost:8082/sparql
   export OPENAI_API_KEY=...            # the LLM endpoint's key
   cd scripts
   python run_eval.py --questions ../material/benchmark_500.json --out results/herikgqa
   python run_eval.py --questions ../material/benchmark_500.json --out results/herikgqa-nogrounding --no-grounding
   python run_eval.py --questions ../material/benchmark_500.json --out results/herikgqa-noerrorcorrection --no-error-correction
   ```

   One JSON file per question (answer, intent, SPARQL, LLM calls, latency); finished questions
   are skipped on a re-run. `--questions ../material/benchmark_user.json` runs the 80 user
   questions of Section 5.

3. Try questions interactively: `python scripts/demo.py --online` (`--no-grounding` and
   `--no-error-correction` work here too; `reset` clears the conversation).

## Method

HeriKGQA answers over a knowledge graph G in three steps, supported by a grounding layer and
guarded by error correction (Section 3 of the paper):

```
Sensor knowledge graph   readings → sosa:ObservationCollection / sosa:Observation, linked to      obda/argus.obda
                         sensor, node (WGS84 position, altitude) and site; each anomaly rule a
                         PANOPTES Policy of its site; served virtually by Ontop over Postgres     backend.py
   │
[1] Semantic parsing     LLM: question (+ last h turns) → JSON intent, constrained by the        1_semantic_parser.py
                         instantiated ontology and the graph's own labels; anomaly questions
                         set anomaly_check and an optional as_of time
   │
[2] SPARQL execution     intent validated and compiled deterministically: filters, joins,        2_sparql_retriever.py
                         GROUP BY aggregates; relative windows end at the latest observation;
                         more than 1,000 rows are declined rather than truncated
   │
    Grounding layer      temporal facts (span, recency)                                          analysis_temp.py
                         spatial facts (centroid, bounding box, nearest/farthest pairs)          analysis_geo.py
                         anomaly rules, per sensor and observed property → exceeds / within      analysis_ek.py
   │
[3] Answer generation    LLM: verbalises the rows, facts and verdicts exactly as given;          3_answer_generator.py
                         an anomaly answer opens with Yes / No / Cannot be determined; a note
                         on the data's time range is appended by code
```

Error correction (`pipeline.py`): **intent voting** over n = 3 parses (the greedy one and two at
temperature 0.7; ties go to the greedy parse), **error-driven retry** of an invalid intent or a
failed or empty query, at most k = 2 times, and **answer verification**: every number in the
answer must occur in the rows, facts, verdicts or question, and an anomaly answer must lead with
the computed verdict; a failing answer is regenerated once, then replaced by a template answer.
Follow-ups use the last h = 2 question–intent pairs.

This is the paper's configuration (`thorough` in the code; the earlier `fast` and `balanced`
ones are kept commented out in `pipeline.CONFIGS`). The ablations of the paper:

| | flag | what changes |
|---|---|---|
| w/o grounding | `--no-grounding` | no grounding layer: the answer LLM receives the rows and the anomaly rules' raw readings and computes facts and verdicts itself (raw readings count toward the 1,000-row cap); SPARQL aggregates unchanged; no answer verification |
| w/o error correction | `--no-error-correction` | one greedy parse, no retries, no answer verification |

Each deterministic module states its own rules to the LLM: the compiler, the temporal, spatial
and anomaly modules export `PARSER_*` texts and an `ANSWER_GUIDE`, from which the parser and
answer prompts are assembled, so the prompts describe exactly what the code does. The schema the
parser sees (classes, properties, labels) is read from the OWL files and the graph at start-up.

### Details

- **Time anchoring.** "Now" is the newest observation in G, not the wall clock (readings arrive
  late; a snapshot never moves). It is looked up at start-up (cached for `ARGUS_LATEST_TTL`
  seconds, default 3600) and ends relative windows ("last 24 hours"), measures the age of
  readings, and is given to the parser for calendar phrases ("yesterday").
- **Anomaly rules.** `analysis_ek.py` re-implements the experts' AD-RT rules: each rule's
  quantity matcher, computation (direct threshold, windowed sum/mean/range, z-score, rate of
  change, step/offset, composite) and site-specific threshold. Every (sensor, quantity) series is
  evaluated separately, with windows ending at the rule's latest matching reading (at or before
  `as_of`), and combined by maximum or minimum, never by pooling readings across sensors. The
  verdict is Yes if an applicable rule fires, No if every applicable rule was evaluated and none
  fired, and Cannot be determined otherwise.
- **Large results.** Aggregates are always computed in SPARQL, never from fetched rows; every
  distinct row goes to the LLM, and more than 1,000 rows prompt for an aggregate or a narrower
  question instead of a silent truncation.
- **Follow-ups.** Interactive mode keeps the last h turns; a follow-up becomes a standalone intent,
  taking from earlier turns only what it leaves open (e.g. the site). Batch runs reset the history
  per question, except for a benchmark question's own earlier turns.

## Data and benchmark

**Snapshot** (`data/`): sensor readings of 13 May–12 August 2026 (data end 09:15 UTC) at the five
sites: 71 nodes, 1,677,556 readings, 5,227,617 observations, 37 anomaly rules (19 with readings
they apply to). It is the live database of 1 October 2026 (`argus_postgres_20261001_180439.dump`)
plus the LoRaWAN measurements up to the data end, every reading at its pilot site
(`scripts/snapshot_add_lorawan.py`).

**Benchmark** (`material/benchmark_500.json`): 500 questions, 100 each basic, spatial, temporal,
anomaly-related and follow-up, generated from 52 templates by `scripts/build_benchmark.py`, which
computes every reference with SQL and Python, independently of the evaluated systems.
Conventions: times in UTC; relative windows end at the data end; distances are haversine
distances on a 6,371 km sphere, and a distance between nodes is also accepted with the altitude
difference (`reference_value_alt`), since the questions do not say which is meant; centroids are
mean node coordinates. `scripts/build_verification.py` recomputes every reference with a second,
independent SQL implementation (`material/verify/`): 489 of 500 match, none disagrees, and the 11
whose answer is a judgement (unanswerable questions, anomaly questions without an applicable or
evaluable rule) were validated by hand.

**User questions** (`material/benchmark_user.json`): 80 questions asked in the deployment between
21 August and 14 October 2026, with references computed on the snapshot under the same conventions
(`scripts/build_user_questions.py`).

## Deployment

In the ARGUS platform, HeriKGQA's data layer runs as four Docker services
(`obda/docker-compose.yml`): Postgres; `ingest`, which polls live readings from the site gateways
(`scripts/0b_online_ingest.py`); `governance_ingest`, which loads the context data (sites, nodes,
sensors, rules; `scripts/0c_ingest_governance_pg.py`, upserting by the API's ids); and Ontop 5.5,
which serves the database as a SPARQL endpoint through the mapping onto PANOPTES, so new readings
are queryable immediately. The ingest services create the schema on their first cycle, so start
Ontop after them:

```bash
docker compose -f obda/docker-compose.yml up -d postgres
docker compose -f obda/docker-compose.yml up -d ingest governance_ingest
docker compose -f obda/docker-compose.yml up -d ontop
export ARGUS_SPARQL_ENDPOINT=http://localhost:8081/sparql
python scripts/demo.py --online
```

Without Docker, `scripts/0a_offline_readings.py --max-records 500` writes a small local TTL
graph that the pipeline queries with rdflib. Node positions come from `material/ARGUS_nodes.csv`;
an edit reaches existing rows only through a backfill (SQL, or `0a_offline_readings.py
--enrich-geo-only` for the TTL graph).

## Generality: MultiTQ

`domains/multitq/` ports HeriKGQA to the temporal KGQA dataset MultiTQ (ICEWS05-15): a small OWL
ontology of events, actors, recipients and timestamps, a parser prompt with its own examples, an
entity linker for the graph's ~10.5k entities, and a loader into an Oxigraph store; the compiler
and error correction are unchanged, the temporal layer gains time filters anchored at another
event's time. With MultiTQ's `kg/full.txt`:

```bash
pip install pyoxigraph
python domains/multitq/build_kg.py --kg <MultiTQ>/data/MultiTQ/kg/full.txt --store data_multitq/oxigraph
export HERIKGQA_DOMAIN=multitq HERIKGQA_OXIGRAPH_STORE=$PWD/data_multitq/oxigraph
export ARGUS_EMBED_MODEL=qwen3-embedding-8b      # the entity linker's embedding model
unset ARGUS_SPARQL_ENDPOINT
cd scripts && python run_eval.py --questions <questions.json> --out results/multitq
```
