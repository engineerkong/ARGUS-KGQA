"""
Step 3 — SPARQL Retriever.

Converts a parsed intent (from semantic_parser) into a SPARQL SELECT query,
executes it against the rdflib graph, and returns results as a list of dicts.
"""

from __future__ import annotations
from typing import Any
from rdflib import Graph

PREFIXES = """\
PREFIX sosa:  <http://www.w3.org/ns/sosa/>
PREFIX argus: <http://www.argus-project.eu/ontology/>
PREFIX ex:    <http://www.argus-project.eu/resource/>
PREFIX rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd:   <http://www.w3.org/2001/XMLSchema#>
PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
"""

# Map short class names to full prefixed forms
CLASS_MAP = {
    "ObservationCollection": "sosa:ObservationCollection",
    "Observation": "sosa:Observation",
    "Sensor": "sosa:Sensor",
    "Site": "argus:Site",
    "Node": "argus:Node",
    "ObservedProperty": "argus:ObservedProperty",
    "EngineeringUnit": "argus:EngineeringUnit",
}

# Map short property names to full prefixed forms
PROP_MAP = {
    "resultTime": "sosa:resultTime",
    "hasSite": "argus:hasSite",
    "madeBySensor": "sosa:madeBySensor",
    "hasNode": "argus:hasNode",
    "hasObservation": "argus:hasObservation",
    "hasEngineeringUnit": "argus:hasEngineeringUnit",
    "observedProperty": "sosa:observedProperty",
    "hasSimpleResult": "sosa:hasSimpleResult",
    "readingType": "argus:readingType",
    "label": "rdfs:label",
    "sensorId": "argus:sensorId",
    "sensorModel": "argus:sensorModel",
    "nodeId": "argus:nodeId",
    "nodeName": "argus:nodeName",
    "topic": "argus:topic",
    "topicId": "argus:topicId",
    "unit": "argus:unit",
    "engineeringUnitId": "argus:engineeringUnitId",
    "rawJson": "argus:rawJson",
}

OBJECT_PROPS = {
    "hasSite", "madeBySensor", "hasNode", "hasObservation",
    "hasEngineeringUnit", "observedProperty",
    "argus:hasSite", "sosa:madeBySensor", "argus:hasNode", "argus:hasObservation",
    "argus:hasEngineeringUnit", "sosa:observedProperty",
}


def _strip_prefix(name: str) -> str:
    """Strip namespace prefix if the LLM included one (e.g. 'argus:hasSite' → 'hasSite')."""
    if ":" in name:
        return name.split(":", 1)[1]
    return name


def _class(name: str) -> str:
    name = _strip_prefix(name)
    return CLASS_MAP.get(name, f"argus:{name}")


def _prop(name: str) -> str:
    stripped = _strip_prefix(name)
    return PROP_MAP.get(stripped, PROP_MAP.get(name, f"argus:{stripped}"))


def _var(*parts: str) -> str:
    cleaned = []
    for p in parts:
        if not p:
            continue
        p = _strip_prefix(p)
        cleaned.append(p.replace("-", "_").replace(" ", "_"))
    return "_".join(cleaned)


def _filter_expr(fvar: str, op: str, val: str) -> str:
    v = val.replace('"', '\\"')
    if op == "contains":
        return f'  FILTER(CONTAINS(LCASE(STR({fvar})), LCASE("{v}")))'
    elif op == "equals":
        return f'  FILTER(LCASE(STR({fvar})) = LCASE("{v}"))'
    elif op == "gt":
        return f'  FILTER(xsd:decimal({fvar}) > {v})'
    elif op == "lt":
        return f'  FILTER(xsd:decimal({fvar}) < {v})'
    elif op == "after":
        return f'  FILTER(STR({fvar}) > "{v}")'
    elif op == "before":
        return f'  FILTER(STR({fvar}) < "{v}")'
    else:
        return f'  FILTER(CONTAINS(LCASE(STR({fvar})), LCASE("{v}")))'


def build_sparql(intent: dict) -> str:
    target_class = intent.get("target_class", "ObservationCollection")
    filters      = intent.get("filters", [])
    return_props = intent.get("return_properties", [])
    joins        = intent.get("joins", [])
    aggregation  = intent.get("aggregation")
    order_by     = intent.get("order_by")
    limit        = intent.get("limit")

    target_var = "?" + target_class.lower()

    # ── SELECT variables ─────────────────────────────────────────────────
    select_vars = [target_var]
    for p in return_props:
        select_vars.append(f"?{_var(p)}")
    for j in joins:
        jvar = "?" + j["class"].lower()
        select_vars.append(jvar)
        for p in j.get("return_properties", []):
            select_vars.append(f"?{_var(j['class'], p)}")

    # ── WHERE body ───────────────────────────────────────────────────────
    lines = [f"  {target_var} a {_class(target_class)} ."]

    for p in return_props:
        if p not in OBJECT_PROPS:
            lines.append(f"  OPTIONAL {{ {target_var} {_prop(p)} ?{_var(p)} . }}")

    for f in filters:
        prop = f.get("property", "")
        val  = f.get("value", "")
        op   = f.get("op", "contains")
        fvar = f"?_f_{_var(prop)}"
        lines.append(f"  {target_var} {_prop(prop)} {fvar} .")
        lines.append(_filter_expr(fvar, op, val))

    # Determine which join classes are referenced in aggregation group_by,
    # so we make them non-optional (required for GROUP BY to bind).
    agg_group_refs = set()
    if aggregation:
        gb = _var(aggregation.get("group_by", ""))
        for j in joins:
            jc = j.get("class", "")
            for p in j.get("return_properties", []):
                if _var(jc, p) == gb or _var(p) == gb:
                    agg_group_refs.add(jc)
            if jc.lower() == gb.lower():
                agg_group_refs.add(jc)

    for j in joins:
        jclass    = j.get("class", "")
        via       = j.get("via", "")
        direction = j.get("direction", "outgoing")
        jvar      = "?" + jclass.lower()
        jreturn   = j.get("return_properties", [])
        jfilters  = j.get("filters", [])

        # Use OPTIONAL unless this join is needed for GROUP BY or has filters
        use_optional = jclass not in agg_group_refs and not jfilters

        if use_optional:
            lines.append("  OPTIONAL {")
        if direction == "outgoing":
            lines.append(f"    {target_var} {_prop(via)} {jvar} .")
        else:
            lines.append(f"    {jvar} {_prop(via)} {target_var} .")
        lines.append(f"    {jvar} a {_class(jclass)} .")

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

        if use_optional:
            lines.append("  }")

    where_clause = "WHERE {\n" + "\n".join(lines) + "\n}"

    # ── Aggregation ──────────────────────────────────────────────────────
    if aggregation:
        agg_type = aggregation.get("type", "count").upper()

        # The LLM may say target="reading" but the actual variable is ?observationcollection.
        # Map any unknown target name back to the target_var from the WHERE clause.
        raw_agg_target = _var(aggregation.get("target", ""))
        known_vars = {target_class.lower()}
        for j in joins:
            known_vars.add(j["class"].lower())
        if raw_agg_target.lower() not in known_vars:
            agg_target = target_var
        else:
            agg_target = "?" + raw_agg_target

        # group_by may reference a join variable like "Site_label" or just "site"
        raw_group = aggregation.get("group_by", "")
        group_var = "?" + _var(raw_group)

        agg_var = f"?{agg_type.lower()}"

        select_clause = f"SELECT {group_var} ({agg_type}({agg_target}) AS {agg_var})"
        group_clause = f"\nGROUP BY {group_var}"
    else:
        select_clause = "SELECT DISTINCT " + " ".join(select_vars)
        group_clause = ""

    # ── ORDER BY / LIMIT ─────────────────────────────────────────────────
    order_clause = ""
    if order_by:
        ovar = "?" + _var(order_by.get("variable", ""))
        odir = order_by.get("direction", "ASC")
        order_clause = f"\nORDER BY {odir}({ovar})"

    limit_clause = ""
    if limit:
        limit_clause = f"\nLIMIT {int(limit)}"

    return (PREFIXES + "\n" + select_clause + "\n" + where_clause
            + group_clause + order_clause + limit_clause)


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
