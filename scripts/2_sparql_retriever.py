"""
Step 2 — intent → SPARQL → results, with resource URIs unfolded into labels.

Class and property mappings come from the OWL files via ontology_schema, so
there is no hardcoded schema knowledge here.
"""

from __future__ import annotations
from typing import Any
from rdflib import Graph
from ontology_schema import (
    EX,
    extract_class_map, extract_prop_map,
    extract_object_props, extract_prop_domain, extract_prop_range,
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
PROP_RANGE = extract_prop_range()


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


def _type_check_redundant(jclass: str, via: str, direction: str) -> bool:
    # True when the join edge already pins the join variable's class, making an
    # extra `?var a <Class>` triple a no-op filter. Worth skipping: rdflib treats
    # it as a low-selectivity rdf:type pattern — measured 0.05s → 19s on a 24k
    # triple graph for an identical result set.
    via_short = _strip_prefix(via)
    implied = (PROP_RANGE.get(via_short) if direction == "outgoing"
               else PROP_DOMAIN.get(via_short))
    return implied is not None and implied == _strip_prefix(jclass)


def _resolve_group_var(raw: str | None, joins: list) -> str:
    # Qualified form ("Site.label" → "site_label") or bare form ("label",
    # resolved by scanning join return_properties). Empty when unset: an
    # aggregation with no group_by is a valid ungrouped total.
    if not raw:
        return ""
    if "." in raw:
        cls, prop = raw.split(".", 1)
        return _var(cls, prop)
    bare = _var(raw)
    for j in joins:
        for p in j.get("return_properties", []):
            if _var(p) == bare:
                return _var(j["class"], p)
    return bare


def _bind_order_join(cls: str, prop: str, joins: list,
                     target_var: str, inner_lines: list, inner_vars: list) -> str | None:
    # Emit the edge from target to the ordering entity plus its property, so the
    # order variable is bound inside the LIMIT subquery. Returns the order var,
    # or None if no matching join describes how to reach the ordering entity.
    ojoin = next((j for j in joins if _strip_prefix(j.get("class", "")).lower() == cls.lower()), None)
    if not ojoin:
        return None
    via = ojoin.get("via", "")
    jvar = "?" + _strip_prefix(cls).lower()
    if ojoin.get("direction", "outgoing") == "outgoing":
        inner_lines.append(f"    {target_var} {_prop(via)} {jvar} .")
    else:
        inner_lines.append(f"    {jvar} {_prop(via)} {target_var} .")
    ovar = f"?{_var(cls, prop)}"
    inner_lines.append(f"    {jvar} {_prop(prop)} {ovar} .")
    inner_vars.append(ovar)
    return ovar


def _build_subquery_sparql(
    target_class: str, target_var: str,
    filters: list, return_props: list,
    joins: list, order_by: dict | None, limit: int,
) -> str:
    # Inner subquery makes LIMIT apply at the entity level (N target entities,
    # not N joined rows). Outer joins everything else OPTIONAL onto that result.
    # ── Inner subquery: target entity + its direct properties ────────────
    inner_vars = [target_var]
    inner_lines = [f"    {target_var} a {_class(target_class)} ."]

    for p in return_props:
        if p not in OBJECT_PROPS:
            pvar = f"?{_var(p)}"
            inner_lines.append(f"    OPTIONAL {{ {target_var} {_prop(p)} {pvar} . }}")
            inner_vars.append(pvar)

    for f in filters:
        prop = f.get("property", "")
        val  = f.get("value", "")
        op   = f.get("op", "contains")
        fvar = f"?_f_{_var(prop)}"
        inner_lines.append(f"    {target_var} {_prop(prop)} {fvar} .")
        inner_lines.append("    " + _filter_expr(fvar, op, val))

    inner_order = ""
    if order_by:
        raw_ovar = order_by.get("variable", "")
        if "." in raw_ovar:
            cls, prop = raw_ovar.split(".", 1)
            if cls.lower() == target_class.lower():
                ovar = "?" + _var(prop)  # target's own property, bound above
            else:
                # Ordering by a joined entity's property: bind the join edge and
                # the property inside the subquery so LIMIT ranks target entities.
                ovar = _bind_order_join(cls, prop, joins, target_var, inner_lines, inner_vars)
        else:
            ovar = "?" + _resolve_group_var(raw_ovar, joins)
        if ovar and ovar in inner_vars:
            inner_order = f"\n    ORDER BY {order_by.get('direction', 'DESC')}({ovar})"

    inner_block = (
        "  {\n"
        f"  SELECT {' '.join(inner_vars)}\n"
        f"  WHERE {{\n" + "\n".join(inner_lines) + "\n  }"
        + inner_order
        + f"\n  LIMIT {int(limit)}\n"
        "  }"
    )

    # ── Outer query: OPTIONAL joins onto the subquery result ─────────────
    outer_select_vars = [v for v in inner_vars if v != target_var]
    outer_lines = [inner_block]
    join_vars = {target_class: target_var}

    for j in joins:
        jclass    = j.get("class", "")
        via       = j.get("via", "")
        direction = j.get("direction", "outgoing")
        jvar      = "?" + jclass.lower()
        jreturn   = j.get("return_properties", [])
        jfilters  = j.get("filters", [])

        via_short = _strip_prefix(via)
        if direction == "incoming":
            prop_range = PROP_RANGE.get(via_short)
            anchor_var = join_vars.get(prop_range, target_var) if prop_range else target_var
        else:
            prop_domain = PROP_DOMAIN.get(via_short)
            anchor_var = (
                join_vars[prop_domain]
                if prop_domain and prop_domain != target_class and prop_domain in join_vars
                else target_var
            )

        use_optional = not jfilters
        if use_optional:
            outer_lines.append("  OPTIONAL {")
        if direction == "outgoing":
            outer_lines.append(f"    {anchor_var} {_prop(via)} {jvar} .")
        else:
            outer_lines.append(f"    {jvar} {_prop(via)} {anchor_var} .")
        if not _type_check_redundant(jclass, via, direction):
            outer_lines.append(f"    {jvar} a {_class(jclass)} .")
        join_vars[jclass] = jvar

        for p in jreturn:
            if p not in OBJECT_PROPS:
                pvar = f"?{_var(jclass, p)}"
                outer_lines.append(f"    OPTIONAL {{ {jvar} {_prop(p)} {pvar} . }}")
                outer_select_vars.append(pvar)

        for f in jfilters:
            prop = f.get("property", "")
            val  = f.get("value", "")
            op   = f.get("op", "contains")
            # Scope the filter variable to the join class: two joins filtering on
            # the same property name (e.g. Site.label and ObservedProperty.label)
            # would otherwise share one variable and force both values to be equal.
            fvar = f"?_jf_{_var(jclass, prop)}"
            outer_lines.append(f"    {jvar} {_prop(prop)} {fvar} .")
            outer_lines.append("    " + _filter_expr(fvar, op, val))

        if use_optional:
            outer_lines.append("  }")

    if not outer_select_vars:
        outer_select_vars = [target_var]
    outer_select_vars = list(dict.fromkeys(outer_select_vars))  # dedup, keep order

    select_clause = "SELECT DISTINCT " + " ".join(outer_select_vars)
    where_clause  = "WHERE {\n" + "\n".join(outer_lines) + "\n}"
    return PREFIXES + "\n" + select_clause + "\n" + where_clause


def _augment_value_projection(intent: dict) -> dict:
    # A bare hasSimpleResult projection loses identity under SELECT DISTINCT:
    # two observations of different properties sharing a value (e.g. pulse=0 and
    # overThreshold=0) collapse into one row. Auto-join ObservedProperty so the
    # property label enters the DISTINCT key. Skipped if already joined.
    joins = intent.get("joins", [])
    projects_value = (
        "hasSimpleResult" in intent.get("return_properties", [])
        or any("hasSimpleResult" in j.get("return_properties", []) for j in joins)
    )
    if not projects_value:
        return intent
    if any(_strip_prefix(j.get("via", "")) == "observedProperty" for j in joins):
        return intent

    intent = dict(intent)
    intent["joins"] = list(joins) + [{
        "class": "ObservedProperty",
        "via": "observedProperty",
        "direction": "outgoing",
        "return_properties": ["label"],
        "filters": [],
    }]
    return intent


def build_sparql(intent: dict) -> str:
    intent = _augment_value_projection(intent)
    target_class = intent.get("target_class", "ObservationCollection")
    filters      = intent.get("filters", [])
    return_props = intent.get("return_properties", [])
    joins        = intent.get("joins", [])
    aggregation  = intent.get("aggregation")
    order_by     = intent.get("order_by")
    limit        = intent.get("limit")

    target_var = "?" + target_class.lower()

    # When LIMIT is requested without aggregation and there are joins, use a
    # subquery so the LIMIT applies at the entity level, not the observation row level.
    if limit and not aggregation and joins:
        return _build_subquery_sparql(
            target_class, target_var, filters, return_props, joins, order_by, limit
        )

    # ── SELECT variables ─────────────────────────────────────────────────
    # For ObservationCollection the target URI is an opaque internal hash —
    # exclude it from SELECT to avoid bloat and allow value-level DISTINCT.
    # For entity classes (Sensor, Site, ObservedProperty, Node) always include
    # the target URI so DISTINCT deduplicates by entity, matching COUNT queries.
    _TRAVERSAL_CLASSES = {"ObservationCollection", "Observation"}
    has_explicit_props = (
        target_class in _TRAVERSAL_CLASSES
        and (bool(return_props) or any(j.get("return_properties") for j in joins))
    )
    select_vars = [] if has_explicit_props else [target_var]
    for p in return_props:
        select_vars.append(f"?{_var(p)}")
    for j in joins:
        jreturn = j.get("return_properties", [])
        for p in jreturn:
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
        gb = _resolve_group_var(aggregation.get("group_by", ""), joins)
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

        # Route through the correct anchor variable.
        # outgoing: anchor is the domain class (property comes FROM it).
        # incoming: anchor is the range class (what the property points TO).
        via_short = _strip_prefix(via)
        if direction == "incoming":
            prop_range = PROP_RANGE.get(via_short)
            anchor_var = join_vars.get(prop_range, target_var) if prop_range else target_var
        else:
            prop_domain = PROP_DOMAIN.get(via_short)
            anchor_var = (
                join_vars[prop_domain]
                if prop_domain and prop_domain != target_class and prop_domain in join_vars
                else target_var
            )

        use_optional = (jclass not in agg_group_refs
                        and not jfilters
                        and jclass not in required_join_classes)

        if use_optional:
            lines.append("  OPTIONAL {")
        if direction == "outgoing":
            lines.append(f"    {anchor_var} {_prop(via)} {jvar} .")
        else:
            lines.append(f"    {jvar} {_prop(via)} {anchor_var} .")
        if not _type_check_redundant(jclass, via, direction):
            lines.append(f"    {jvar} a {_class(jclass)} .")

        join_vars[jclass] = jvar

        for p in jreturn:
            if p not in OBJECT_PROPS:
                lines.append(f"    OPTIONAL {{ {jvar} {_prop(p)} ?{_var(jclass, p)} . }}")

        for f in jfilters:
            prop = f.get("property", "")
            val  = f.get("value", "")
            op   = f.get("op", "contains")
            # Scope the filter variable to the join class: two joins filtering on
            # the same property name (e.g. Site.label and ObservedProperty.label)
            # would otherwise share one variable and force both values to be equal.
            fvar = f"?_jf_{_var(jclass, prop)}"
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
            prop_key = _strip_prefix(aggregation.get("target", ""))
            prop_full = _prop(aggregation.get("target", ""))
            domain = PROP_DOMAIN.get(prop_key)
            anchor = join_vars.get(domain, target_var) if domain else target_var
            required_line = f"  {anchor} {prop_full} {agg_target} ."
            if required_line not in lines:
                lines.append(required_line)
        elif _strip_prefix(aggregation.get("target", "")) in PROP_MAP:
            agg_target = "?" + raw_agg_target
            prop_key = _strip_prefix(aggregation.get("target", ""))
            prop_full = _prop(aggregation.get("target", ""))
            domain = PROP_DOMAIN.get(prop_key)
            anchor = join_vars.get(domain, target_var) if domain else target_var
            lines.append(f"  {anchor} {prop_full} {agg_target} .")
        else:
            agg_target = target_var

        group_name = _resolve_group_var(aggregation.get("group_by"), joins)
        group_var = f"?{group_name}" if group_name else ""

        agg_var = f"?{agg_type.lower()}"

        use_distinct = aggregation.get("distinct", agg_type == "COUNT")
        distinct_kw = "DISTINCT " if use_distinct else ""
        agg_expr = f"({agg_type}({distinct_kw}{agg_target}) AS {agg_var})"
        # No group_by → a single ungrouped total, so no GROUP BY clause.
        select_clause = f"SELECT {group_var} {agg_expr}" if group_var else f"SELECT {agg_expr}"
        group_clause = f"\nGROUP BY {group_var}" if group_var else ""
    else:
        select_clause = "SELECT DISTINCT " + " ".join(select_vars)
        group_clause = ""

    where_clause = "WHERE {\n" + "\n".join(lines) + "\n}"

    # ── ORDER BY / LIMIT ─────────────────────────────────────────────────
    order_clause = ""
    if order_by:
        ovar = "?" + _resolve_group_var(order_by.get("variable", ""), joins)
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

_RESOURCE_PREFIX = str(EX)
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
                # Direct SPARQL binding — keep even if it looks like a UUID/ID,
                # since the query explicitly requested it. Only drop None and
                # values exceeding the length cap.
                if val is not None and len(val) <= _MAX_VALUE_LEN:
                    new_row[key] = val
        unfolded.append(new_row)

    return unfolded
