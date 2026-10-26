# deploy-tools (PRIVATE — never push)

Builds the public Hugging Face Space in `../hf-spaces` from ARGUS-KGQA. Everything here
names the real sites; nothing here goes to the Space.

| File | Purpose |
|---|---|
| `site_aliases.json` | real site / place names → anonymised names, fictitious site centroids, forbidden words |
| `anonymize_db.py` | anonymises a **copy** of the snapshot (database `argus_anon`) and writes `../hf-spaces/data/snapshot.dump`; refuses to run on `argus_snapshot` / `argus` |
| `build_space.py` | copies the runtime code, ontology and mapping from ARGUS-KGQA into `../hf-spaces`, rewriting site names, the project name/domain and the LLM provider URL; then scans the whole Space for forbidden words |
| `export_repo.py`, `repo_files/` | builds the anonymous code repository `~/workspace/HeriKGQA` (method, evaluation, container; one configuration, unnamed) and the Hugging Face dataset `~/workspace/HeriKGQA-dataset` (benchmark aligned to the paper's questions, neutral dump); README, Dockerfile and dataset card from `repo_files/`; runs the checks, including the dump's content |
| `run_local.sh` | runs the Space locally without Docker against `argus_anon` (http://localhost:7861) |
| `.pgdata/` | private PostgreSQL 16 instance (port 55432) holding `argus_anon` |
| `.local/` | Ontop CLI, conda env `hfspace` test runs and logs |

## Rebuild after changing ARGUS-KGQA

```bash
python build_space.py                # re-copies scripts/*.py, ontology, mapping; must end "scan: clean"
```

## Re-create the anonymised dump (only if the snapshot or the aliases change)

```bash
B=~/miniconda3/envs/pgtools/bin
$B/pg_ctl -D .pgdata -o "-p 55432 -k /tmp" -l .pgdata.log start
$B/dropdb -h localhost -p 55432 -U argus argus_anon && $B/createdb -h localhost -p 55432 -U argus argus_anon
$B/pg_restore -h localhost -p 55432 -U argus -d argus_anon --no-owner --no-privileges -j 2 \
    ~/workspace/argus_snapshot_v2.dump      # pg_dump -Fc of argus_snapshot (snapshot v2, with LoRaWAN)
python anonymize_db.py --dsn postgresql://argus@localhost:55432/argus_anon --out ../hf-spaces/data/snapshot.dump
```

## Publishing a dump

A custom-format dump records the database name and every object's owner (`--no-owner` does
not remove them). `anonymize_db.py` dumps `argus_anon` as `argus`, so its dump must not be
published as it is: `export_repo.py` copies `argus_anon` into `herikg_snapshot`, owned by the
role `herikg`, dumps that, and drops the copy. That neutral dump is the one in the dataset and
in `../hf-spaces/data/` (the earlier one is `.local/snapshot.dump.argus-owner.bak`).
