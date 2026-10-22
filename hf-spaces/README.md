---
title: HeriKGQA
emoji: 🏛️
colorFrom: indigo
colorTo: green
sdk: docker
app_port: 7860
pinned: false
short_description: Grounded question answering over heritage sensor data
---

# HeriKGQA demo

Natural-language question answering over sensor readings from five cultural heritage
sites. A question is parsed by an LLM into an intent constrained by the ontology,
compiled deterministically into SPARQL, and answered from the query results and a
deterministic analysis layer (spatial, temporal, and expert anomaly rules), so that
every number in an answer is computed by SPARQL or code rather than by the model.

The interface runs the system in its THOROUGH configuration. Its configuration options are
shown beside the conversation and can be changed:

| Option | Default | Range |
|---|---|---|
| parse candidates n (majority vote over n parses of a new question) | 3 | 1–5 |
| retry budget k (re-parses after an invalid, failed or empty query) | 2 | 0–3 |
| history turns h (earlier turns given to the parser) | 2 | 0–4 |
| answer check (numbers, timestamps and verdict checked against the evidence; one regeneration, then the template answer) | on | on / off |

The interface shows the parsed intent and SPARQL behind each answer, and lets users rate each
answer (good / fine / bad, with a comment for bad); each logged question records the options
it was answered with.

## Data

A frozen snapshot of the sensor database, 13 May – 12 August 2026: 3,737,747
observations at five heritage sites, plus the expert anomaly
rules. It is anonymised: sites are named `site_a` … `site_e`, place names in node, rule
and threat descriptions are replaced, and each
site is moved to a fictitious location while keeping the distances between its nodes.
The ontology namespaces are replaced by `heritage-kg.example.org`. The snapshot is
served by PostgreSQL 16 through an Ontop 5.5 virtual SPARQL endpoint inside the container.

## Configuration (Space settings → Secrets)

| Name | Required | Meaning |
|---|---|---|
| `OPENAI_API_KEY` | yes | key of the OpenAI-compatible LLM endpoint |
| `OLLAMA_BASE_URL` | yes | URL of that endpoint (`…/v1`) |
| `OLLAMA_MODEL` | no | model name (default `openai-gpt-oss-120b`) |
| `HF_TOKEN`, `FEEDBACK_REPO` | no | write token and a private dataset repo (`user/name`) to which questions, answers and ratings are pushed every 5 minutes |

## Run locally

```bash
docker build -t herikgqa .
docker run --rm -p 7860:7860 -e OPENAI_API_KEY=... -e OLLAMA_BASE_URL=... herikgqa
# then open http://localhost:7860 (start-up takes about two minutes)
```

`start.sh` starts PostgreSQL, Ontop and the app; its paths and ports can be overridden
with `PGDATA`, `PGPORT`, `HERIKG_DB`, `HERIKG_DB_USER`, `ONTOP_HOME`, `ONTOP_PORT`, and
`SKIP_POSTGRES=1` uses an already running database.
