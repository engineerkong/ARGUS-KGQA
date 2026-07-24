"""
Diagnose a remote SPARQL backend layer by layer, so a failing endpoint is
attributed to the URL/data/protocol rather than to the pipeline.

    export ARGUS_SPARQL_ENDPOINT=http://localhost:8081/sparql   # e.g. Ontop
    python scripts/test_backend.py
"""

from __future__ import annotations
import os
import sys
import urllib.parse
import urllib.request

ENDPOINT = os.environ.get("ARGUS_SPARQL_ENDPOINT")


def _raw(query: str) -> tuple[int, str]:
    url = ENDPOINT + "?" + urllib.parse.urlencode({"query": query})
    req = urllib.request.Request(url, headers={"Accept": "application/sparql-results+json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status, r.read(600).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read(600).decode("utf-8", "replace")
    except Exception as e:
        return -1, f"{type(e).__name__}: {e}"


def main() -> None:
    if not ENDPOINT:
        sys.exit("Set ARGUS_SPARQL_ENDPOINT first.")
    print(f"Endpoint: {ENDPOINT}\n")

    print("[1] Raw HTTP GET (bypasses rdflib) — trivial query")
    code, body = _raw("SELECT (COUNT(*) AS ?n) WHERE { ?s ?p ?o }")
    print(f"    HTTP {code}")
    print(f"    {body[:300]}")
    if code == -1:
        print("\n    → Could not connect at all. Is the server running and the")
        print("      host:port correct? Start it, e.g.:")
        print("      docker compose -f obda/docker-compose.yml up -d ontop")
        return
    if code != 200:
        print("\n    → Connected, but the endpoint rejected the query. Likely causes:")
        print("      404: wrong path — Ontop's query service is usually")
        print("           http://HOST:8081/sparql.")
        print("      405: querying the wrong path.")
        print("      500: check `docker logs obda-ontop-1` for a mapping/SQL error.")
        print("      Fix the URL, then re-run.")
        return
    print("    → Endpoint reachable and accepts queries.\n")

    print("[2] Is any data loaded?")
    code, body = _raw("SELECT (COUNT(*) AS ?n) WHERE { ?s ?p ?o }")
    print(f"    {body[:200]}")
    print("    → If count is 0, run `python scripts/4_load_postgres.py` first.\n")

    print("[3] Through the pipeline's backend (rdflib SPARQLStore)")
    be = __import__("backend")
    backend = be.RemoteSparqlBackend(ENDPOINT)
    rows = backend.query("SELECT (COUNT(DISTINCT ?s) AS ?n) WHERE { ?s a ?t }")
    print(f"    {rows}")
    if rows and "error" in rows[0]:
        print("    → Raw HTTP worked but rdflib did not: a store-config problem,")
        print("      not Ontop. Report this output back.")
    else:
        print("    → Backend works. The pipeline should now run against this endpoint.")


if __name__ == "__main__":
    main()
