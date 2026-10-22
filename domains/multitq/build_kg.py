"""
Load the MultiTQ knowledge graph (ICEWS05-15 quadruples, kg/full.txt) into an Oxigraph store.

    python domains/multitq/build_kg.py [--kg ../MultiTQ/data/MultiTQ/kg/full.txt] [--store data_multitq/oxigraph]

Each line "subject<TAB>relation<TAB>object<TAB>YYYY-MM-DD" becomes
    ex:event/<n>  a mtq:Event, sosa:Observation ;
                  mtq:actor ex:entity/<subject> ; mtq:recipient ex:entity/<object> ;
                  mtq:eventType "<relation, underscores as spaces>" ;
                  sosa:resultTime "<date>T00:00:00+00:00"^^xsd:dateTime .
and every entity gets rdfs:label "<name, underscores as spaces>" and the type mtq:Actor
and/or mtq:Recipient for the roles it occurs in. Typing events as sosa:Observation lets the
pipeline read the data window (earliest/latest resultTime) with its usual query.
"""
import argparse
import hashlib
import time
from pathlib import Path

import pyoxigraph as ox

ROOT = Path(__file__).resolve().parents[2]
MTQ = "http://herikgqa.org/multitq/ontology#"
EX = "http://herikgqa.org/multitq/resource/"
SOSA = "http://www.w3.org/ns/sosa/"
RDF_TYPE = ox.NamedNode("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
LABEL = ox.NamedNode("http://www.w3.org/2000/01/rdf-schema#label")
DATETIME = ox.NamedNode("http://www.w3.org/2001/XMLSchema#dateTime")
EVENT, ACTOR, RECIPIENT = (ox.NamedNode(MTQ + c) for c in ("Event", "Actor", "Recipient"))
OBSERVATION = ox.NamedNode(SOSA + "Observation")
P_ACTOR, P_RECIPIENT, P_TYPE = (ox.NamedNode(MTQ + p) for p in ("actor", "recipient", "eventType"))
P_TIME = ox.NamedNode(SOSA + "resultTime")


def label(name: str) -> str:
    return name.replace("_", " ").strip()


def entity(name: str) -> ox.NamedNode:
    # names contain characters that are not safe in an IRI; a short hash keeps IRIs valid and unique
    return ox.NamedNode(EX + "entity/" + hashlib.sha1(name.encode()).hexdigest()[:16])


def triples(kg: Path):
    roles: dict[str, set] = {}
    with open(kg, encoding="utf-8") as f:
        for n, line in enumerate(f):
            s, r, o, d = line.rstrip("\n").split("\t")
            ev = ox.NamedNode(f"{EX}event/{n}")
            yield ox.Quad(ev, RDF_TYPE, EVENT)
            yield ox.Quad(ev, RDF_TYPE, OBSERVATION)
            yield ox.Quad(ev, P_ACTOR, entity(s))
            yield ox.Quad(ev, P_RECIPIENT, entity(o))
            yield ox.Quad(ev, P_TYPE, ox.Literal(label(r)))
            yield ox.Quad(ev, P_TIME, ox.Literal(f"{d}T00:00:00+00:00", datatype=DATETIME))
            roles.setdefault(s, set()).add(ACTOR)
            roles.setdefault(o, set()).add(RECIPIENT)
    for name, cls in roles.items():
        yield ox.Quad(entity(name), LABEL, ox.Literal(label(name)))
        for c in cls:
            yield ox.Quad(entity(name), RDF_TYPE, c)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kg", default=str(ROOT.parent / "MultiTQ/data/MultiTQ/kg/full.txt"))
    ap.add_argument("--store", default=str(ROOT / "data_multitq/oxigraph"))
    args = ap.parse_args()
    Path(args.store).mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    store = ox.Store(args.store)
    store.bulk_extend(triples(Path(args.kg)))
    store.flush()
    store.optimize()
    print(f"{len(store):,} triples in {args.store} ({time.time() - t0:.0f}s)")


if __name__ == "__main__":
    main()
