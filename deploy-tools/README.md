# deploy-tools (PRIVATE — never push)

Builds the public Hugging Face Space in `../hf-spaces` from ARGUS-KGQA. Everything here
names the real sites; nothing here goes to the Space.

| File | Purpose |
|---|---|
| `site_aliases.json` | real site / place names → anonymised names, fictitious site centroids, forbidden words |
| `anonymize_db.py` | anonymises a **copy** of the snapshot (database `argus_anon`) and writes `../hf-spaces/data/snapshot.dump`; refuses to run on `argus_snapshot` / `argus` |
| `build_space.py` | copies the runtime code, ontology and mapping from ARGUS-KGQA into `../hf-spaces`, rewriting site names, the project name/domain and the LLM provider URL; then scans the whole Space for forbidden words |
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
    ~/workspace/argus_postgres_20261001_180439.dump
python anonymize_db.py --dsn postgresql://argus@localhost:55432/argus_anon --out ../hf-spaces/data/snapshot.dump
```
