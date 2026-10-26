---
pretty_name: HeriKGQA benchmark and sensor-database snapshot
language:
- en
task_categories:
- question-answering
- table-question-answering
size_categories:
- n<1K
configs:
- config_name: benchmark
  data_files: benchmark_500.csv
---

# HeriKGQA: benchmark and database snapshot

A 500-question benchmark for question answering over a cultural-heritage sensor knowledge
graph, and the anonymised database snapshot the knowledge graph is built on. The code
(system, Ontop mapping, ontology, scorer) is in the accompanying code repository, linked
from the paper.

## Files

| File | Contents |
|---|---|
| `benchmark_500.json` | the benchmark, with typed reference values and conversation history (use this file for evaluation) |
| `benchmark_500.csv` | the same questions and reference answers as text (for browsing) |
| `benchmark_500.meta.json` | counts, data range and the conventions the references follow |
| `snapshot.dump` | the database: PostgreSQL 16, custom format (`pg_restore`) |

## Benchmark

500 questions, 100 of each type:

| Type | Asks about |
|---|---|
| basic | counts, averages and extremes per site and quantity, comparisons between sites |
| spatial | distances between nodes and between sites, nearest nodes, nodes within a radius, centroids, altitudes, northern- and southernmost nodes |
| temporal | first and latest readings, time spans, daily and monthly statistics, values in date ranges and relative windows, when an extreme occurred |
| anomaly | whether a quantity at a site exceeds its expert (AD-RT) rule thresholds on a day or at the latest reading, and the thresholds themselves |
| follow-up | a question that depends on one or two earlier turns (another site, the next day or month, the minimum instead of the maximum, …) |

Every type includes a few unanswerable questions: the answer must say that the data
cannot answer them.

Each item of `benchmark_500.json` has:

| Field | Meaning |
|---|---|
| `id`, `type`, `template` | identifier, question type, question template |
| `question` | the question |
| `history` | earlier turns of a follow-up (`question`, `answer`) |
| `reference` | the reference answer, as text |
| `reference_value` | the value an answer must contain (see below) |
| `answerable` | false when the data cannot answer the question; the answer must say so |

`reference_value` is typed:

| Type | An answer is correct when |
|---|---|
| integer | a number in it equals the count |
| float | a number in it equals the value at the stated precision, within 1% |
| `Yes` / `No` / `Cannot be determined` | it gives that anomaly verdict |
| date or `YYYY-MM-DD HH:MM UTC` | it states that date or time |
| site or node name | it names that site or node |
| list | every element matches |
| null | it declines (no data), not a number |

Every reference is computed directly from the snapshot with SQL and plain Python,
independently of any QA system.

The conventions:
- all times are UTC, and "on a date" means that UTC day;
- relative times ("the last 24 hours") end at the snapshot's last reading;
- distances are haversine on a 6,371,000 m sphere;
- an anomaly verdict is Yes if any applicable rule fires, No if at least one rule was
  evaluated and none fired, and Cannot be determined if none could be evaluated.

They are given in full in `benchmark_500.meta.json`.

## Database snapshot

A frozen copy of the sensor database, 13 May – 12 August 2026: 3,737,747 observations at
five heritage sites, plus the expert anomaly rules (thresholds, windows, quantities).

It is anonymised:
- sites are named `site_a` … `site_e`;
- place names in node, rule and threat descriptions are replaced;
- each site is moved to a fictitious location, keeping the distances between its nodes.

Measured values, timestamps and row counts are unchanged.

To restore it:

```bash
createdb herikg_snapshot
pg_restore -d herikg_snapshot --no-owner --no-privileges snapshot.dump
```

The code repository's `Dockerfile` downloads this dataset and serves the snapshot as a
virtual knowledge graph through Ontop.
