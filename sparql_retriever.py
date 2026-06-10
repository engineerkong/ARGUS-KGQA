"""
Step 3 — SPARQL Retriever.

Converts a parsed intent (from semantic_parser) into a SPARQL SELECT query,
executes it against the in-memory rdflib graph, and returns results as a list
of dicts.
"""

from __future__ import annotations
from typing import Any
from rdflib import Graph

PREFIXES = """\
PREFIX pan:  <http://www.argus-project.eu/>
PREFIX inst: <http://www.argus-project.eu/instance/>
PREFIX geo:  <http://www.opengis.net/ont/geosparql#>
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
"""

# Properties that are object links (need OPTIONAL block, not simple literal bind)
OBJECT_PROPS = {
    "hasEvent", "isTriggeredBy", "assessesRiskFor", "relatedThreat",
    "generatesThreat", "measures", "documents", "usesPrediction",
    "hasSpatiotemporalRepresentation", "hasMeasurement", "quantifies",
    "hasSensorLocation", "hasGeometry",
}

# Properties that live in the geo: namespace rather than pan:
GEO_PROPS = {"asWKT", "hasGeometry", "sfWithin"}


def _prop(name: str) -> str:
    return f"geo:{name}" if name in GEO_PROPS else f"pan:{name}"


def build_sparql(intent: dict) -> str:
    target_class = intent.get("target_class", "Asset")
    filters      = intent.get("filters", [])
    return_props = intent.get("return_properties", ["name"])
    joins        = intent.get("joins", [])

    target_var = "?" + target_class.lower()

    # ── SELECT variables ──────────────────────────────────────────────────────
    select_vars = [target_var]
    for p in return_props:
        select_vars.append(f"?{_var(p)}")
    for j in joins:
        jvar = "?" + j["class"].lower()
        select_vars.append(jvar)
        for p in j.get("return_properties", []):
            select_vars.append(f"?{_var(j['class'], p)}")

    select_clause = "SELECT DISTINCT " + " ".join(select_vars)

    # ── WHERE body ────────────────────────────────────────────────────────────
    lines = [f"  {target_var} a pan:{target_class} ."]

    # Return properties (OPTIONALs so missing values don't drop rows)
    for p in return_props:
        if p not in OBJECT_PROPS:
            lines.append(f"  OPTIONAL {{ {target_var} {_prop(p)} ?{_var(p)} . }}")

    # Filters on target
    for f in filters:
        prop = f.get("property", "")
        val  = f.get("value", "")
        op   = f.get("op", "contains")
        fvar = f"?_f_{_var(prop)}"
        lines.append(f"  {target_var} {_prop(prop)} {fvar} .")
        lines.append(_filter_expr(fvar, op, val))

    # Joins
    for j in joins:
        jclass    = j.get("class", "")
        via       = j.get("via", "")
        direction = j.get("direction", "outgoing")
        jvar      = "?" + jclass.lower()
        jreturn   = j.get("return_properties", [])
        jfilters  = j.get("filters", [])

        lines.append("  OPTIONAL {")
        if direction == "outgoing":
            lines.append(f"    {target_var} {_prop(via)} {jvar} .")
        else:
            lines.append(f"    {jvar} {_prop(via)} {target_var} .")
        lines.append(f"    {jvar} a pan:{jclass} .")

        for p in jreturn:
            if p not in OBJECT_PROPS:
                lines.append(f"    OPTIONAL {{ {jvar} {_prop(p)} ?{_var(jclass, p)} . }}")

        for f in jfilters:
            prop = f.get("property", "")
            val  = f.get("value", "")
            op   = f.get("op", "contains")
            fvar = f"?_jf_{_var(prop)}"
            lines.append(f"    {jvar} {_prop(prop)} {fvar} .")
            lines.append("    " + _filter_expr(fvar, op, val))

        lines.append("  }")

    where_clause = "WHERE {\n" + "\n".join(lines) + "\n}"
    return PREFIXES + "\n" + select_clause + "\n" + where_clause


def execute(graph: Graph, sparql: str) -> list[dict[str, Any]]:
    results = []
    try:
        qres = graph.query(sparql)
        for row in qres:
            record = {}
            for var in qres.vars:
                val = row[var]
                record[str(var)] = str(val) if val is not None else None
            results.append(record)
    except Exception as e:
        results = [{"error": str(e)}]
    return results


# ── Helpers ───────────────────────────────────────────────────────────────────

def _var(*parts: str) -> str:
    return "_".join(p.replace("-", "_").replace(" ", "_") for p in parts if p)


def _filter_expr(fvar: str, op: str, val: str) -> str:
    v = val.replace('"', '\\"')
    if op == "contains":
        return f'  FILTER(CONTAINS(LCASE(STR({fvar})), LCASE("{v}")))'
    elif op == "equals":
        return f'  FILTER(LCASE(STR({fvar})) = LCASE("{v}"))'
    elif op == "gt":
        return f'  FILTER(xsd:float({fvar}) > "{v}"^^xsd:float)'
    elif op == "lt":
        return f'  FILTER(xsd:float({fvar}) < "{v}"^^xsd:float)'
    elif op == "after":
        # Works for both xsd:dateTime and xsd:date
        return f'  FILTER(STR({fvar}) > "{v}")'
    elif op == "before":
        return f'  FILTER(STR({fvar}) < "{v}")'
    else:
        return f'  FILTER(CONTAINS(LCASE(STR({fvar})), LCASE("{v}")))'
