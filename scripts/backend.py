"""
Query backend behind one interface, so the pipeline does not care whether the
RDF lives in a local rdflib graph or behind a remote SPARQL endpoint (Fuseki,
Ontop, …). Selected by make_backend(): ARGUS_SPARQL_ENDPOINT picks remote.

URI unfolding needs each result URI's predicate/object pairs. Locally that is a
cheap in-memory lookup; remotely it must be batched (one VALUES query) or it
becomes one HTTP round-trip per URI. prefetch() warms that batch.
"""

from __future__ import annotations
import os
from pathlib import Path
from typing import Any, Iterable, Iterator

from rdflib import Graph, URIRef

_PREFETCH_BATCH = 100


def _run_query(graph: Graph, sparql: str) -> list[dict[str, Any]]:
    try:
        qres = graph.query(sparql)
        rows = []
        for row in qres:
            rows.append({str(v): (str(row[v]) if row[v] is not None else None)
                         for v in qres.vars})
        return rows
    except Exception as e:
        return [{"error": str(e)}]


def _chunks(seq: list, n: int) -> Iterator[list]:
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


class Backend:
    def query(self, sparql: str) -> list[dict[str, Any]]:
        raise NotImplementedError

    def predicate_objects(self, uri: str) -> list[tuple[str, str]]:
        raise NotImplementedError

    def prefetch(self, uris: Iterable[str]) -> None:
        # Optional: warm a cache before many predicate_objects() calls.
        pass

    def describe(self) -> str:
        return self.__class__.__name__


class RdflibBackend(Backend):
    def __init__(self, graph: Graph):
        self.graph = graph

    def query(self, sparql: str) -> list[dict[str, Any]]:
        return _run_query(self.graph, sparql)

    def predicate_objects(self, uri: str) -> list[tuple[str, str]]:
        return [(str(p), str(o)) for p, o in self.graph.predicate_objects(URIRef(uri))]

    def describe(self) -> str:
        return f"local rdflib graph — {len(self.graph)} triples"


class RemoteSparqlBackend(Backend):
    def __init__(self, endpoint: str):
        from rdflib.plugins.stores.sparqlstore import SPARQLStore
        self.endpoint = endpoint
        self.graph = Graph(store=SPARQLStore(endpoint, returnFormat="json"))
        self._cache: dict[str, list[tuple[str, str]]] = {}

    def query(self, sparql: str) -> list[dict[str, Any]]:
        return _run_query(self.graph, sparql)

    def prefetch(self, uris: Iterable[str]) -> None:
        pending = [u for u in dict.fromkeys(uris) if u not in self._cache]
        for batch in _chunks(pending, _PREFETCH_BATCH):
            values = " ".join(f"<{u}>" for u in batch)
            rows = _run_query(self.graph,
                              f"SELECT ?s ?p ?o WHERE {{ VALUES ?s {{ {values} }} ?s ?p ?o }}")
            for u in batch:
                self._cache.setdefault(u, [])  # negative cache: don't re-fetch empties
            for row in rows:
                if "error" in row:
                    break
                s, p, o = row.get("s"), row.get("p"), row.get("o")
                if s is not None and p is not None:
                    self._cache.setdefault(s, []).append((p, o))

    def predicate_objects(self, uri: str) -> list[tuple[str, str]]:
        if uri not in self._cache:
            self.prefetch([uri])
        return self._cache.get(uri, [])

    def describe(self) -> str:
        return f"remote SPARQL endpoint — {self.endpoint}"


def make_backend(ttl_path: str | Path | None = None, endpoint: str | None = None) -> Backend:
    endpoint = endpoint or os.environ.get("ARGUS_SPARQL_ENDPOINT")
    if endpoint:
        return RemoteSparqlBackend(endpoint)
    g = Graph()
    if ttl_path and Path(ttl_path).exists():
        g.parse(str(ttl_path), format="turtle")
    return RdflibBackend(g)
