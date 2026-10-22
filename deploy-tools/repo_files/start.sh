#!/bin/bash
# Start PostgreSQL (the read-only snapshot restored at build time) and Ontop (SPARQL
# over it), then run the given command, or the web demo when there is none. Paths
# and ports can be overridden to run outside the container (see README.md).
set -euo pipefail
cd "$(dirname "$0")"

export PGDATA="${PGDATA:-$HOME/pgdata}"
export PGPORT="${PGPORT:-5432}"
export HERIKG_DB="${HERIKG_DB:-herikg_snapshot}"
export HERIKG_DB_USER="${HERIKG_DB_USER:-herikg}"
ONTOP_HOME="${ONTOP_HOME:-/opt/ontop}"
ONTOP_PORT="${ONTOP_PORT:-8080}"
RUN_DIR="${RUN_DIR:-/tmp/herikg}"
mkdir -p "$RUN_DIR"

if [ $# -eq 0 ]; then   # the demo needs the LLM; scoring and the benchmark builder do not
    : "${OPENAI_API_KEY:?set OPENAI_API_KEY (LLM endpoint key)}"
    : "${OLLAMA_BASE_URL:?set OLLAMA_BASE_URL (OpenAI-compatible LLM endpoint URL)}"
fi

if [ -z "${SKIP_POSTGRES:-}" ]; then
    echo "[start] PostgreSQL on port $PGPORT"
    pg_ctl -D "$PGDATA" -o "-p $PGPORT -k $RUN_DIR -c listen_addresses=localhost" -l "$RUN_DIR/postgres.log" -w start
fi

echo "[start] Ontop on port $ONTOP_PORT"
sed -e "s/\${PGPORT}/$PGPORT/" -e "s/\${HERIKG_DB}/$HERIKG_DB/" -e "s/\${HERIKG_DB_USER}/$HERIKG_DB_USER/g" \
    ontop/ontop.properties.template > "$RUN_DIR/ontop.properties"
cp -n ontop/jdbc/*.jar "$ONTOP_HOME/jdbc/" 2>/dev/null || true
"$ONTOP_HOME/ontop" endpoint --mapping ontop/mapping.obda --properties "$RUN_DIR/ontop.properties" \
    --port "$ONTOP_PORT" > "$RUN_DIR/ontop.log" 2>&1 &
ONTOP_PID=$!

export HERIKG_SPARQL_ENDPOINT="http://localhost:$ONTOP_PORT/sparql"
for i in $(seq 1 120); do
    if curl -sf -o /dev/null -H 'Accept: application/sparql-results+json' \
        --data-urlencode 'query=SELECT * WHERE { ?s ?p ?o } LIMIT 1' "$HERIKG_SPARQL_ENDPOINT"; then
        echo "[start] Ontop ready after ${i}x2 s"; break
    fi
    if ! kill -0 "$ONTOP_PID" 2>/dev/null; then echo "[start] Ontop exited:"; tail -30 "$RUN_DIR/ontop.log"; exit 1; fi
    sleep 2
done

if [ $# -gt 0 ]; then
    exec "$@"
fi
echo "[start] web demo on port ${PORT:-7860} (initialising the pipeline takes about a minute)"
exec python app/app.py
