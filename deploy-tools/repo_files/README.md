# HeriKGQA

Grounded question answering over a cultural-heritage sensor knowledge graph. This
repository contains the system, the anonymised data snapshot, the 500-question benchmark
and the evaluation scripts used in the paper.

## How it works

1. **Semantic parsing:** an LLM parses the question into an intent (target class, filters,
   joins, aggregation, time window), constrained by the ontology. THOROUGH votes over
   *n* = 3 parses.
2. **Deterministic compilation:** the intent is compiled into SPARQL. Ontop answers the
   query over a virtual knowledge graph on PostgreSQL.
3. **Deterministic analysis:** temporal, spatial and expert anomaly-rule (AD-RT) facts
   are computed from the results in Python.
4. **Answer:** an LLM writes the answer from the results and the computed facts. The
   answer check requires every number, timestamp and anomaly verdict to appear in that
   evidence. A failing answer is regenerated once and, if it fails again, replaced by a
   template answer.

A failed or empty query is re-parsed with feedback (retry budget *k* = 2). Earlier turns
of a conversation are given to the parser (history *h* = 2). Every number in an answer
is computed by SPARQL or deterministic code, not by the LLM.

## Repository layout

| Path | Contents |
|---|---|
| `scripts/` | the pipeline (`pipeline.py`, `1_semantic_parser.py`, `2_sparql_retriever.py`, `3_answer_generator.py`, `analysis_*.py`, `backend.py`, `ontology_schema.py`) and its entry points: `run_eval.py` (batch evaluation), `demo.py` / `demo_ad.py` (command line), `build_benchmark.py` (benchmark generation) |
| `material/` | the ontology (`panoptes3*.owl`) and the benchmark (`benchmark_500.json`, `.csv`, `.meta.json`) |
| `ontop/` | the Ontop mapping (`mapping.obda`), its properties template and the PostgreSQL JDBC driver |
| `data/` | the anonymised PostgreSQL 16 snapshot, split into parts with checksums |
| `evaluation/` | the rule-based scorer (`score.py`), the verdict classifier for lenient scoring (`extract_verdicts.py`) and the node names the scorer uses (`node_labels.csv`) |
| `app/` | the web demo (Gradio) |
| `Dockerfile`, `start.sh` | one container with PostgreSQL, Ontop and the pipeline |

## Data

A frozen snapshot of the sensor database, 13 May – 12 August 2026: 3,737,747 observations
at five heritage sites, plus the expert anomaly rules.

It is anonymised:
- sites are named `site_a` … `site_e`;
- place names in node, rule and threat descriptions are replaced;
- each site is moved to a fictitious location, keeping the distances between its nodes;
- the ontology namespaces are replaced by `heritage-kg.example.org`.

Measured values, timestamps and row counts are unchanged.

## Requirements

- Docker.
- An OpenAI-compatible chat-completion endpoint. The experiments used `gpt-oss-120b`.

## Quick start

```bash
docker build -t herikgqa .            # restores the snapshot at build time (a few minutes)

export OPENAI_API_KEY=...             # key of the LLM endpoint
export OLLAMA_BASE_URL=https://.../v1 # OpenAI-compatible endpoint URL
export OLLAMA_MODEL=openai-gpt-oss-120b

# web demo on http://localhost:7860
docker run --rm -p 7860:7860 -e OPENAI_API_KEY -e OLLAMA_BASE_URL -e OLLAMA_MODEL herikgqa

# interactive session on the command line, showing the intent, SPARQL and analysis of each answer
docker run --rm -it -e OPENAI_API_KEY -e OLLAMA_BASE_URL -e OLLAMA_MODEL herikgqa \
    python scripts/demo.py --online
```

Without `--online`, `demo.py` answers a fixed set of example questions; `demo_ad.py` does the
same for anomaly questions. `--no-grounding` / `--no-error-correction` select the ablations.

## Reproducing the evaluation

The system and its two ablations, on the 500 benchmark questions. Results are written to
`evaluation/results/` on the host, one JSON file per question. Finished questions are
skipped when a run is restarted.

```bash
mkdir -p evaluation/results
RUN="docker run --rm -e OPENAI_API_KEY -e OLLAMA_BASE_URL -e OLLAMA_MODEL \
     -v $PWD/evaluation:/home/user/herikgqa/evaluation herikgqa"
Q=material/benchmark_500.json

$RUN python scripts/run_eval.py --questions $Q --out evaluation/results/herikgqa
$RUN python scripts/run_eval.py --questions $Q --out evaluation/results/herikgqa-nogrounding --no-grounding
$RUN python scripts/run_eval.py --questions $Q --out evaluation/results/herikgqa-noerrorcorrection --no-error-correction

# accuracy per question type (no LLM needed); also writes evaluation/scores.csv
$RUN python evaluation/score.py evaluation/results/herikgqa evaluation/results/herikgqa-nogrounding \
    evaluation/results/herikgqa-noerrorcorrection

# lenient scoring: the verdict an anomaly answer states anywhere, classified once by the LLM
$RUN python evaluation/extract_verdicts.py evaluation/results/*
$RUN python evaluation/score.py --verdicts evaluation/verdicts.json evaluation/results/*
```

| Configuration | Flag | Parse candidates *n* | Retry budget *k* | History turns *h* | Answer check |
|---|---|---|---|---|---|
| HeriKGQA (THOROUGH) | | 3 | 2 | 2 | on |
| w/o grounding | `--no-grounding` | 3 | 2 | 2 | — (it is defined against the analysis output) |
| w/o error correction | `--no-error-correction` | 1 | 0 | 2 | off |

**w/o grounding** removes the deterministic analysis layer:
- the LLM gets the rows, plus each anomaly rule's definition and raw readings, and computes
  temporal, spatial and anomaly facts itself;
- SPARQL aggregates are unchanged;
- the raw readings count toward the 1,000-row cap.

**w/o error correction** keeps the analysis layer and the history.

Numbers obtained on this anonymised copy can differ slightly from those in the paper, for
two reasons:
- site names, node names and coordinates differ from the original data the LLM saw;
- LLM sampling is not deterministic.

## Benchmark

`material/benchmark_500.json` has 500 questions, 100 of each type: basic, spatial,
temporal, anomaly, follow-up.

Each item has:
- a reference answer and a typed `reference_value`, used by `evaluation/score.py`;
- for follow-ups, the earlier turns (`history`).

`scripts/build_benchmark.py` computes every reference directly from the snapshot with SQL
and plain Python, independently of the system. Its conventions (UTC days, relative times
ending at the last reading, haversine distances, AD-RT windows) are in
`benchmark_500.meta.json`. To regenerate the benchmark inside the container:

```bash
docker run --rm herikgqa python scripts/build_benchmark.py
```

## Running without Docker

1. Restore the snapshot into PostgreSQL 16:
   ```bash
   cat data/snapshot.dump.part-* > snapshot.dump
   pg_restore -d <db> --no-owner snapshot.dump
   ```
2. Start Ontop 5.5 with `ontop/mapping.obda` and the properties template filled in.
3. Install the Python dependencies: `pip install -r requirements.txt` (Python 3.10+).
4. Set `HERIKG_SPARQL_ENDPOINT=http://localhost:<port>/sparql` and the LLM variables.
5. Run the scripts as above, without the `docker run …` prefix.

| Variable | Meaning (default) |
|---|---|
| `HERIKG_SPARQL_ENDPOINT` | SPARQL endpoint (set by `start.sh` in the container) |
| `OPENAI_API_KEY`, `OLLAMA_BASE_URL`, `OLLAMA_MODEL` | LLM endpoint, key and model (`openai-gpt-oss-120b`) |
| `HERIKG_VOTE_TEMPERATURE` | temperature of the sampled parse candidates (0.7) |
| `HERIKG_MAX_RESULT_ROWS` | row cap above which a question is declined, not truncated (1000) |
| `HERIKG_LLM_MAX_RETRIES`, `HERIKG_LLM_TIMEOUT` | retries and timeout of LLM requests |
| `HERIKG_SNAPSHOT_DSN` | database of `build_benchmark.py` (`postgresql://herikg@localhost:5432/herikg_snapshot`) |
