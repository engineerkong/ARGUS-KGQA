"""
Step 3 — SPARQL Retriever.

Converts a parsed intent (from semantic_parser) into a SPARQL SELECT query,
executes it against the rdflib graph, and returns results as a list of dicts.

All class/property mappings are derived from the OWL ontology files
via ontology_schema — no hardcoded schema knowledge here.
"""

from __future__ import annotations
from typing import Any
from rdflib import Graph
from ontology_schema import (
    extract_class_map, extract_prop_map,
    extract_object_props, extract_prop_domain,
)

PREFIXES = """\
PREFIX sosa:  <http://www.w3.org/ns/sosa/>
PREFIX argus: <http://www.argus-project.eu/ontology/>
PREFIX ex:    <http://www.argus-project.eu/resource/>
PREFIX rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd:   <http://www.w3.org/2001/XMLSchema#>
PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
"""

CLASS_MAP = extract_class_map()
PROP_MAP = extract_prop_map()
OBJECT_PROPS = extract_object_props()
PROP_DOMAIN = extract_prop_domain()


def _strip_prefix(name: str) -> str:
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
    return "_".join(cleaned).lower()


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

    # Determine which join classes are referenced in aggregation group_by
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

    # Pre-scan: find which join classes are depended on by later joins
    required_join_classes = set()
    for j in joins:
        via_short = _strip_prefix(j.get("via", ""))
        prop_domain = PROP_DOMAIN.get(via_short)
        if prop_domain and prop_domain != target_class:
            required_join_classes.add(prop_domain)

    # Track join variables so later joins can reference earlier ones
    join_vars = {target_class: target_var}

    for j in joins:
        jclass    = j.get("class", "")
        via       = j.get("via", "")
        direction = j.get("direction", "outgoing")
        jvar      = "?" + jclass.lower()
        jreturn   = j.get("return_properties", [])
        jfilters  = j.get("filters", [])

        # Route through the correct anchor variable based on property domain
        via_short = _strip_prefix(via)
        prop_domain = PROP_DOMAIN.get(via_short)
        if prop_domain and prop_domain != target_class and prop_domain in join_vars:
            anchor_var = join_vars[prop_domain]
        else:
            anchor_var = target_var

        use_optional = (jclass not in agg_group_refs
                        and not jfilters
                        and jclass not in required_join_classes)

        if use_optional:
            lines.append("  OPTIONAL {")
        if direction == "outgoing":
            lines.append(f"    {anchor_var} {_prop(via)} {jvar} .")
        else:
            lines.append(f"    {jvar} {_prop(via)} {anchor_var} .")
        lines.append(f"    {jvar} a {_class(jclass)} .")

        join_vars[jclass] = jvar

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

    # ── Aggregation ──────────────────────────────────────────────────────
    if aggregation:
        agg_type = aggregation.get("type", "count").upper()

        raw_agg_target = _var(aggregation.get("target", ""))
        known_class_vars = {target_class.lower()}
        for j in joins:
            known_class_vars.add(j["class"].lower())

        known_prop_vars = {_var(p) for p in return_props}
        for j in joins:
            for p in j.get("return_properties", []):
                known_prop_vars.add(_var(j["class"], p))
                known_prop_vars.add(_var(p))

        if raw_agg_target in known_class_vars:
            agg_target = "?" + raw_agg_target
        elif raw_agg_target in known_prop_vars:
            agg_target = "?" + raw_agg_target
            prop_full = _prop(aggregation.get("target", ""))
            required_line = f"  {target_var} {prop_full} {agg_target} ."
            if required_line not in lines:
                lines.append(required_line)
        elif _strip_prefix(aggregation.get("target", "")) in PROP_MAP:
            agg_target = "?" + raw_agg_target
            prop_full = _prop(aggregation.get("target", ""))
            lines.append(f"  {target_var} {prop_full} {agg_target} .")
        else:
            agg_target = target_var

        raw_group = aggregation.get("group_by", "")
        group_var = "?" + _var(raw_group)

        agg_var = f"?{agg_type.lower()}"

        select_clause = f"SELECT {group_var} ({agg_type}({agg_target}) AS {agg_var})"
        group_clause = f"\nGROUP BY {group_var}"
    else:
        select_clause = "SELECT DISTINCT " + " ".join(select_vars)
        group_clause = ""

    where_clause = "WHERE {\n" + "\n".join(lines) + "\n}"

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


# ── URI unfolding ────────────────────────────────────────────────────────

from rdflib import URIRef
from rdflib.namespace import RDFS, RDF

import re

_RESOURCE_PREFIX = "http://www.argus-project.eu/resource/"
_SKIP_PREDS = {str(RDF.type)}
_MAX_VALUE_LEN = 200
_UUID_RE = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.I)
_HEX_ID_RE = re.compile(r'^[0-9a-f]{16,}$', re.I)


def _is_resource_uri(val: str | None) -> bool:
    return val is not None and val.startswith(_RESOURCE_PREFIX)


def _is_id_value(val: str) -> bool:
    if _UUID_RE.match(val) or _HEX_ID_RE.match(val):
        return True
    parts = val.split("/")
    if len(parts) >= 2:
        uuid_count = sum(1 for p in parts if _UUID_RE.match(p) or _HEX_ID_RE.match(p))
        if uuid_count >= 1 and uuid_count >= len(parts) - 1:
            return True
    return False


def _pred_short(pred_str: str) -> str:
    return pred_str.rsplit("/", 1)[-1].rsplit("#", 1)[-1]


def _resolve_uri(graph: Graph, uri_str: str, cache: dict, depth: int = 0) -> dict[str, str]:
    if uri_str in cache:
        return cache[uri_str]

    uri = URIRef(uri_str)
    info = {}

    for pred, obj in graph.predicate_objects(uri):
        pred_str = str(pred)
        if pred_str in _SKIP_PREDS:
            continue
        key = _pred_short(pred_str)
        if key in info:
            continue

        obj_str = str(obj)
        if len(obj_str) > _MAX_VALUE_LEN:
            continue
        if _is_resource_uri(obj_str):
            if depth < 1:
                nested = _resolve_uri(graph, obj_str, cache, depth + 1)
                resolved = nested.get("label")
                if resolved:
                    info[key] = resolved
            else:
                for lbl in graph.objects(URIRef(obj_str), RDFS.label):
                    info[key] = str(lbl)
                    break
        elif _is_id_value(obj_str):
            continue
        else:
            info[key] = obj_str

    cache[uri_str] = info
    return info



def _clean_value(val: str | None) -> str | None:
    if val is None:
        return None
    if len(val) > _MAX_VALUE_LEN:
        return None
    if _is_resource_uri(val):
        short = val.replace(_RESOURCE_PREFIX, "")
        if _is_id_value(short):
            return None
        return short
    if _is_id_value(val):
        return None
    return val


def unfold_results(graph: Graph, results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Unfold resource URIs in results by following all their properties in the graph."""
    if not results or "error" in results[0]:
        return results

    cache: dict[str, dict] = {}
    unfolded = []

    for row in results:
        new_row = {}
        for key, val in row.items():
            if _is_resource_uri(val):
                info = _resolve_uri(graph, val, cache)
                for info_key, info_val in info.items():
                    cleaned = _clean_value(info_val)
                    if cleaned is not None:
                        new_row[f"{key}_{info_key}"] = cleaned
                if not info:
                    cleaned = _clean_value(val)
                    if cleaned is not None:
                        new_row[key] = cleaned
            else:
                cleaned = _clean_value(val)
                if cleaned is not None:
                    new_row[key] = cleaned
        unfolded.append(new_row)

    return unfolded
