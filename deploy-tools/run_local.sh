#!/bin/bash
# PRIVATE. Run the Space locally without Docker, against the anonymised copy in the
# private PostgreSQL instance (port 55432, database argus_anon) — the same start.sh
# the container runs, with SKIP_POSTGRES=1. Needs the LLM key in the environment:
#   OPENAI_API_KEY=... OLLAMA_BASE_URL=https://.../v1 ./run_local.sh     -> http://localhost:7861
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
L="$HERE/.local"
PG="$HOME/miniconda3/envs/pgtools/bin"
: "${OPENAI_API_KEY:?set OPENAI_API_KEY}"; : "${OLLAMA_BASE_URL:?set OLLAMA_BASE_URL}"
"$PG/pg_ctl" -D "$HERE/.pgdata" status >/dev/null 2>&1 || \
    "$PG/pg_ctl" -D "$HERE/.pgdata" -o "-p 55432 -k /tmp" -l "$HERE/.pgdata.log" -w start
cd "$HERE/../hf-spaces"
PATH="$HOME/miniconda3/envs/hfspace/bin:$PATH" SKIP_POSTGRES=1 PGPORT=55432 HERIKG_DB=argus_anon \
HERIKG_DB_USER=argus ONTOP_HOME="$L/ontop" ONTOP_PORT=8090 PORT=7861 RUN_DIR="$L/run" \
HERIKG_LOG_DIR="$L/run/logs" exec ./start.sh
