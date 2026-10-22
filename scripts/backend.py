"""
Query backend behind one interface, so the pipeline does not care whether the
RDF lives in a local rdflib graph, behind a remote SPARQL endpoint (Ontop
over Postgres) or in a local Oxigraph store. Selected by make_backend():
HERIKGQA_OXIGRAPH_STORE picks Oxigraph, ARGUS_SPARQL_ENDPOINT picks remote.

URI unfolding needs each result URI's predicate/object pairs. Locally that is a
cheap in-memory lookup; remotely it must be batched (one VALUES query) or it
becomes one HTTP round-trip per URI. prefetch() warms that batch.
"""

from __future__ import annotations
import os
from pathlib import Path
from typing import Any, Iterable, Iterator

from rdflib import Graph, URIRef

# A 100-URI VALUES query is rejected by Ontop (75 verified OK); a failed batch
# would be negative-cached, silently dropping every label it should resolve.
_PREFETCH_BATCH = 50


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
        # bind_namespaces="none": rdflib's Graph.query() otherwise auto-prepends
        # every namespace bound on the graph (including its huge built-in default
        # set — sosa, rdfs, …) as PREFIX lines ahead of the query text. Since our
        # queries already declare their own PREFIXes, that produces duplicate
        # declarations for shared prefixes like "sosa", which strict remote
        # parsers (Ontop/Jena) reject outright.
        self.graph = Graph(store=SPARQLStore(endpoint, returnFormat="json"),
                            bind_namespaces="none")
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
        rows = self.query("SELECT (COUNT(*) AS ?n) WHERE { ?s ?p ?o }")
        if rows and "error" not in rows[0]:
            n = next(iter(rows[0].values()))
            return f"remote SPARQL endpoint — {self.endpoint} — {int(n):,} triples"
        return f"remote SPARQL endpoint — {self.endpoint}"


class OxigraphBackend(Backend):
    """A local Oxigraph store (pyoxigraph), opened read-only: for a graph too large for an
    in-memory rdflib graph and with no endpoint behind it (e.g. domains/multitq)."""

    def __init__(self, path: str | Path):
        import pyoxigraph
        self.path = str(path)
        self.store = pyoxigraph.Store.read_only(self.path)

    def query(self, sparql: str) -> list[dict[str, Any]]:
        try:
            res = self.store.query(sparql)
            if isinstance(res, bool):  # ASK
                return [{"ask": str(res).lower()}]
            names = [v.value for v in res.variables]
            return [{n: (sol[n].value if sol[n] is not None else None) for n in names} for sol in res]
        except Exception as e:
            return [{"error": str(e)}]

    def predicate_objects(self, uri: str) -> list[tuple[str, str]]:
        import pyoxigraph
        return [(q.predicate.value, q.object.value)
                for q in self.store.quads_for_pattern(pyoxigraph.NamedNode(uri), None, None)]

    def describe(self) -> str:
        return f"local Oxigraph store — {self.path} — {len(self.store):,} triples"


def make_backend(ttl_path: str | Path | None = None, endpoint: str | None = None) -> Backend:
    store = os.environ.get("HERIKGQA_OXIGRAPH_STORE")
    if store:
        return OxigraphBackend(store)
    endpoint = endpoint or os.environ.get("ARGUS_SPARQL_ENDPOINT")
    if endpoint:
        return RemoteSparqlBackend(endpoint)
    g = Graph()
    if ttl_path and Path(ttl_path).exists():
        g.parse(str(ttl_path), format="turtle")
    return RdflibBackend(g)
