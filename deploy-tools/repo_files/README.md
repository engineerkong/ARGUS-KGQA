# HeriKGQA

Grounded question answering over a cultural-heritage sensor knowledge graph: the system and
the evaluation scripts used in the paper.

- **Demo:** [huggingface.co/spaces/{{SPACE_REPO}}](https://huggingface.co/spaces/{{SPACE_REPO}})
- **Benchmark and database:** the 500-question benchmark and the anonymised database snapshot,
  [huggingface.co/datasets/{{DATASET_REPO}}](https://huggingface.co/datasets/{{DATASET_REPO}})

**How it works.**
1. An LLM parses the question into an intent; the system votes over *n* = 3 parses.
2. The intent is compiled deterministically into SPARQL, which Ontop answers over PostgreSQL.
   A failed or empty query is re-parsed with feedback (*k* = 2 retries).
3. Python computes the temporal, spatial and anomaly-rule (AD-RT) facts.
4. An LLM writes the answer. Every number, timestamp and verdict in it must appear in the
   evidence, or the answer is regenerated once and then replaced by a template answer.

Follow-ups see the last *h* = 2 turns.

| Path | Contents |
|---|---|
| `scripts/` | the pipeline, `run_eval.py` (batch evaluation), `demo.py` / `demo_ad.py`, `build_benchmark.py` |
| `evaluation/` | `score.py` (rule-based scorer), `extract_verdicts.py` (lenient verdict scoring), `node_labels.csv` |
| `material/`, `ontop/` | ontology; Ontop mapping and JDBC driver |
| `data/SHA256SUMS` | checksums of the dataset files |
| `app/`, `Dockerfile`, `start.sh` | web demo; one container with PostgreSQL, Ontop and the pipeline |

## Quick start

You need Docker and an OpenAI-compatible LLM endpoint (the paper used `gpt-oss-120b`).

```bash
docker build -t herikgqa .     # downloads and verifies the dataset, restores the snapshot

export OPENAI_API_KEY=... OLLAMA_BASE_URL=https://.../v1 OLLAMA_MODEL=openai-gpt-oss-120b
docker run --rm -p 7860:7860 -e OPENAI_API_KEY -e OLLAMA_BASE_URL -e OLLAMA_MODEL herikgqa   # demo: http://localhost:7860
```

## Reproducing the evaluation

```bash
mkdir -p evaluation/results
RUN="docker run --rm -e OPENAI_API_KEY -e OLLAMA_BASE_URL -e OLLAMA_MODEL \
     -v $PWD/evaluation:/home/user/herikgqa/evaluation herikgqa"
Q=material/benchmark_500.json

$RUN python scripts/run_eval.py --questions $Q --out evaluation/results/herikgqa
$RUN python scripts/run_eval.py --questions $Q --out evaluation/results/herikgqa-nogrounding --no-grounding
$RUN python scripts/run_eval.py --questions $Q --out evaluation/results/herikgqa-noerrorcorrection --no-error-correction

$RUN python evaluation/score.py evaluation/results/*                    # accuracy per question type
$RUN python evaluation/extract_verdicts.py evaluation/results/*         # optional: lenient verdict scoring
$RUN python evaluation/score.py --verdicts evaluation/verdicts.json evaluation/results/*
```

| System | Flag | *n* | *k* | *h* | Answer check |
|---|---|---|---|---|---|
| HeriKGQA | | 3 | 2 | 2 | on |
| w/o grounding | `--no-grounding` | 3 | 2 | 2 | — |
| w/o error correction | `--no-error-correction` | 1 | 0 | 2 | off |

- **w/o grounding:** the analysis layer computes nothing. The LLM gets the rows and the
  anomaly rules' raw readings and works out the facts itself.
- **Resuming:** finished questions are skipped when a run restarts.
- **Expect small differences from the paper:** on this anonymised copy, names and
  coordinates differ, and LLM sampling is not deterministic.

## Without Docker

1. Download the dataset:
   ```bash
   hf download {{DATASET_REPO}} --repo-type dataset --local-dir hf-data
   mv hf-data/benchmark_500.* material/
   mv hf-data/snapshot.dump data/
   ```
2. Restore it: `pg_restore -d <db> --no-owner data/snapshot.dump` (PostgreSQL 16).
3. Start Ontop 5.5 with `ontop/`.
4. `pip install -r requirements.txt`.
5. Set `HERIKG_SPARQL_ENDPOINT` plus the LLM variables above. Optional:
   - `HERIKG_VOTE_TEMPERATURE` (0.7)
   - `HERIKG_MAX_RESULT_ROWS` (1000)
   - `HERIKG_SNAPSHOT_DSN`, used by `build_benchmark.py`
