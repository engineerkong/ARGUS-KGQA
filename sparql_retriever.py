"""
Step 3 — SPARQL Retriever.

Converts a parsed intent (from semantic_parser) into a SPARQL SELECT query,
executes it against the in-memory rdflib graph, and returns results as a list
of dicts.
"""

from __future__ import annotations
from typing import Any
from rdflib import Graph

PAN_NS  = "http://www.argus-project.eu/"
INST_NS = "http://www.argus-project.eu/instance/"

PREFIXES = """\
PREFIX pan:  <http://www.argus-project.eu/>
PREFIX inst: <http://www.argus-project.eu/instance/>
PREFIX geo:  <http://www.opengis.net/ont/geosparql#>
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
"""

# Properties that are object properties (point to another named instance)
OBJECT_PROPS = {
    "hasEvent", "isTriggeredBy", "assessesRiskFor", "relatedThreat",
    "generatesThreat", "measures", "documents", "usesPrediction",
    "hasSpatiotemporalRepresentation", "hasMeasurement", "quantifies",
}


def build_sparql(intent: dict) -> str:
    target_class   = intent.get("target_class", "Asset")
    filters        = intent.get("filters", [])
    return_props   = intent.get("return_properties", ["name"])
    joins          = intent.get("joins", [])

    target_var = "?" + target_class.lower()

    # SELECT variables
    select_vars = [target_var]
    for p in return_props:
        select_vars.append(f"?{_var(p)}")
    for j in joins:
        jvar = "?" + j["class"].lower()
        select_vars.append(jvar)
        for p in j.get("return_properties", []):
            select_vars.append(f"?{_var(j['class'], p)}")

    select_clause = "SELECT DISTINCT " + " ".join(select_vars)

    # WHERE body
    lines = [f"  {target_var} a pan:{target_class} ."]

    # Return properties as OPTIONALs
    for p in return_props:
        if p in OBJECT_PROPS:
            lines.append(f"  OPTIONAL {{ {target_var} pan:{p} ?{_var(p)} . }}")
        else:
            lines.append(f"  OPTIONAL {{ {target_var} pan:{p} ?{_var(p)} . }}")

    # Filters on the target
    for f in filters:
        prop = f.get("property", "")
        val  = f.get("value", "")
        op   = f.get("op", "contains")
        fvar = f"?_f_{_var(prop)}"
        lines.append(f"  {target_var} pan:{prop} {fvar} .")
        lines.append(_filter_expr(fvar, op, val))

    # Joins
    for j in joins:
        jclass = j.get("class", "")
        via    = j.get("via", "")
        direction = j.get("direction", "outgoing")
        jvar   = "?" + jclass.lower()
        jfilters = j.get("filters", [])
        jreturn  = j.get("return_properties", [])

        if direction == "outgoing":
            lines.append(f"  OPTIONAL {{")
            lines.append(f"    {target_var} pan:{via} {jvar} .")
        else:  # incoming
            lines.append(f"  OPTIONAL {{")
            lines.append(f"    {jvar} pan:{via} {target_var} .")

        lines.append(f"    {jvar} a pan:{jclass} .")

        for p in jreturn:
            lines.append(f"    OPTIONAL {{ {jvar} pan:{p} ?{_var(jclass, p)} . }}")

        for f in jfilters:
            prop = f.get("property", "")
            val  = f.get("value", "")
            op   = f.get("op", "contains")
            fvar = f"?_jf_{_var(prop)}"
            lines.append(f"    {jvar} pan:{prop} {fvar} .")
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
    """Make a safe SPARQL variable name from one or more strings."""
    return "_".join(p.replace("-", "_").replace(" ", "_") for p in parts if p)


def _filter_expr(fvar: str, op: str, val: str) -> str:
    val_escaped = val.replace('"', '\\"')
    if op == "contains":
        return f'  FILTER(CONTAINS(LCASE(STR({fvar})), LCASE("{val_escaped}")))'
    elif op == "equals":
        return f'  FILTER(LCASE(STR({fvar})) = LCASE("{val_escaped}"))'
    elif op == "gt":
        return f'  FILTER(xsd:float({fvar}) > {val_escaped})'
    elif op == "lt":
        return f'  FILTER(xsd:float({fvar}) < {val_escaped})'
    else:
        return f'  FILTER(CONTAINS(LCASE(STR({fvar})), LCASE("{val_escaped}")))'
