"""
Step 2 — intent → SPARQL → results, with resource URIs unfolded into labels.

Class and property mappings come from the OWL files via ontology_schema, so
there is no hardcoded schema knowledge here.
"""

from __future__ import annotations
import json
import re
from typing import Any
from rdflib import Graph
from analysis_temp import TIME_OPS, TIME_BUCKETS, TIME_CLASSES, time_bounds, bucket_bind
from ontology_schema import (
    EX,
    extract_class_map, extract_prop_map,
    extract_object_props, extract_prop_domain, extract_prop_range,
)

PREFIXES = """\
PREFIX sosa:     <http://www.w3.org/ns/sosa/>
PREFIX argus:    <http://www.argus-project.eu/ontology/>
PREFIX panoptes: <http://www.argus-project.eu/panoptes#>
PREFIX ex:       <http://www.argus-project.eu/resource/>
PREFIX rdfs:     <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd:      <http://www.w3.org/2001/XMLSchema#>
PREFIX rdf:      <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX mtq:      <http://herikgqa.org/multitq/ontology#>
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


def _filter_expr(fvar: str, op: str, val) -> str:
    if op == "in":
        vals = val if isinstance(val, list) else [x.strip() for x in str(val).split(",")]
        opts = ", ".join('LCASE("' + str(x).replace('"', '\\"') + '")' for x in vals)
        return f'  FILTER(LCASE(STR({fvar})) IN ({opts}))'
    v = str(val).replace('"', '\\"')
    if op == "contains":
        return f'  FILTER(CONTAINS(LCASE(STR({fvar})), LCASE("{v}")))'
    elif op == "equals":
        return f'  FILTER(LCASE(STR({fvar})) = LCASE("{v}"))'
    elif op == "gt":
        return f'  FILTER(xsd:decimal({fvar}) > {v})'
    elif op == "lt":
        return f'  FILTER(xsd:decimal({fvar}) < {v})'
    elif op in TIME_OPS:
        cmp, bound = time_bounds(op, val)
        return f'  FILTER(STR({fvar}) {cmp} "{bound}")'
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


SUPPORTED_AGGREGATIONS = {"count", "min", "max", "avg", "sum", "range"}


def validate_intent(intent: dict) -> str | None:
    """A problem that would make build_sparql emit invalid SPARQL, as feedback
    for the parser's retry loop; None when the intent can be compiled."""
    agg = intent.get("aggregation")
    if agg:
        t = str(agg.get("type", "count")).lower()
        if t not in SUPPORTED_AGGREGATIONS:
            return (f"Unsupported aggregation type {t!r}; use one of {', '.join(sorted(SUPPORTED_AGGREGATIONS))}, "
                    f"or no aggregation to list the values.")
        bucket = agg.get("time_bucket")
        if bucket and bucket not in TIME_BUCKETS:
            return f"Unsupported time_bucket {bucket!r}; use one of {', '.join(TIME_BUCKETS)} or null."
    scopes = [(intent.get("target_class", ""), intent.get("filters") or [])]
    scopes += [(j.get("class", ""), j.get("filters") or []) for j in intent.get("joins") or []]
    for cls, filters in scopes:
        equals = {}
        for f in filters:
            prop = str(f.get("property", ""))
            if "." in prop or "/" in prop:
                return (f"Filter property {prop!r} on {cls} is a path; a filter applies to the class's own "
                        f"property — add a join to the related class and put the filter on that join.")
            if f.get("op") == "equals":
                equals.setdefault(prop.lower(), []).append(f.get("value"))
        for prop, vals in equals.items():
            if len(vals) > 1:
                return (f"{cls}.{prop} has several 'equals' filters ({vals}), which can never all match; use one "
                        f"filter with op 'in' and a list of values.")
    return None


def _join_anchor_class(j: dict, target_class: str, joined: set) -> str:
    # The class a join hangs off — same routing rule as the join emitters below.
    via_short = _strip_prefix(j.get("via", ""))
    if j.get("direction", "outgoing") == "incoming":
        rng = PROP_RANGE.get(via_short)
        return rng if rng in joined else target_class
    dom = PROP_DOMAIN.get(via_short)
    return dom if dom and dom != target_class and dom in joined else target_class


def _required_join_classes(joins: list, target_class: str, extra: tuple = ()) -> set:
    """Classes of joins that constrain the result: joins with filters (and the
    `extra` ones, e.g. the class the ranking is on), plus every join on the
    path from the target to them, and joins a later join hangs off."""
    joined, anchor = set(), {}
    for j in joins:
        anchor[j.get("class", "")] = _join_anchor_class(j, target_class, joined)
        joined.add(j.get("class", ""))
    known = {j.get("class", "") for j in joins}
    required = {j.get("class", "") for j in joins if j.get("filters")} | {c for c in extra if c in known}
    required |= {a for c, a in anchor.items() if a != target_class}
    frontier = list(required)
    while frontier:
        a = anchor.get(frontier.pop())
        if a and a != target_class and a not in required:
            required.add(a)
            frontier.append(a)
    return required


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

    # What the LIMIT ranks by: (class, property). A bare name is the target's own
    # property unless a join returns it.
    order_cls = order_prop = None
    if order_by and order_by.get("variable"):
        raw_ovar = order_by["variable"]
        if "." in raw_ovar:
            order_cls, order_prop = raw_ovar.split(".", 1)
        else:
            order_cls, order_prop = target_class, raw_ovar
            for j in joins:
                if any(_var(p) == _var(raw_ovar) for p in j.get("return_properties", [])):
                    order_cls = j.get("class", "")
        order_cls = next((j.get("class", "") for j in joins
                          if j.get("class", "").lower() == order_cls.lower()), order_cls)

    # Constraining joins (filters and the path to them) go inside, so LIMIT ranks
    # only entities that satisfy them — not the first N entities overall. So does
    # the join carrying the ranking value.
    extra = (order_cls,) if order_cls and order_cls.lower() != target_class.lower() else ()
    required = _required_join_classes(joins, target_class, extra)
    inner_join_vars = {target_class: target_var}
    for j in joins:
        jclass = j.get("class", "")
        if jclass not in required:
            continue
        via, direction = j.get("via", ""), j.get("direction", "outgoing")
        jvar = "?" + jclass.lower()
        avar = inner_join_vars.get(_join_anchor_class(j, target_class, set(inner_join_vars)), target_var)
        if direction == "outgoing":
            inner_lines.append(f"    {avar} {_prop(via)} {jvar} .")
        else:
            inner_lines.append(f"    {jvar} {_prop(via)} {avar} .")
        if not _type_check_redundant(jclass, via, direction):
            inner_lines.append(f"    {jvar} a {_class(jclass)} .")
        inner_join_vars[jclass] = jvar
        for f in j.get("filters", []):
            fvar = f"?_jf_{_var(jclass, f.get('property', ''))}"
            inner_lines.append(f"    {jvar} {_prop(f.get('property', ''))} {fvar} .")
            inner_lines.append("    " + _filter_expr(fvar, f.get("op", "contains"), f.get("value", "")))

    inner_order = ""
    if order_cls:
        # Bind the ranking value inside the subquery — on the target itself or on
        # the (now inner) join carrying it — so LIMIT keeps the top-ranked
        # entities. Without it the LIMIT kept an arbitrary one.
        if order_cls.lower() == target_class.lower():
            ovar = "?" + _var(order_prop)
            if ovar not in inner_vars:
                inner_lines.append(f"    {target_var} {_prop(order_prop)} {ovar} .")
                inner_vars.append(ovar)
        elif order_cls in inner_join_vars:
            ovar = f"?{_var(order_cls, order_prop)}"
            inner_lines.append(f"    {inner_join_vars[order_cls]} {_prop(order_prop)} {ovar} .")
            inner_vars.append(ovar)
        else:
            ovar = _bind_order_join(order_cls, order_prop, joins, target_var, inner_lines, inner_vars)
        if ovar and ovar in inner_vars:
            keys = [f"{order_by.get('direction', 'DESC')}({ovar})"]
            # Ranking readings by value: ties go to the earliest reading (the
            # time the maximum was first reached), so the answer is deterministic.
            # Entities (nodes, sensors) are not readings — no tie-break by time.
            if _strip_prefix(target_class) in TIME_CLASSES and "time" not in ovar:
                time_owner = target_var
                inner_lines.append(f"    {time_owner} sosa:resultTime ?tie_resulttime .")
                inner_vars.append("?tie_resulttime")
                keys.append("ASC(?tie_resulttime)")
            inner_order = f"\n    ORDER BY {' '.join(keys)}"
            # Ranking needs the value: SPARQL sorts unbound first in ASC order,
            # so an entity without it would otherwise be "the lowest".
            inner_lines.append(f"    FILTER(BOUND({ovar}))")

    inner_block = (
        "  {\n"
        f"  SELECT DISTINCT {' '.join(inner_vars)}\n"
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

        # A join that later joins hang off (or that filters) must not be OPTIONAL:
        # a variable bound only inside an OPTIONAL and reused outside it turns
        # into a cross product.
        use_optional = not jfilters and jclass not in required
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


def _augment_in_projection(intent: dict) -> dict:
    # A filter matching several values ("in" [delos, schenkenberg]) leaves the
    # rows unable to say which value each one matched, so per-value analysis
    # (per-site centroids, per-node distances) has nothing to group on.
    # Return the filtered property as well.
    def needs(filters, returned):
        return [f["property"] for f in filters or []
                if f.get("op") == "in" and isinstance(f.get("value"), list) and len(f["value"]) > 1
                and f.get("property") and f["property"] not in returned]
    intent = json.loads(json.dumps(intent))
    intent["return_properties"] = (intent.get("return_properties") or []) + needs(
        intent.get("filters"), intent.get("return_properties") or [])
    for j in intent.get("joins") or []:
        j["return_properties"] = (j.get("return_properties") or []) + needs(
            j.get("filters"), j.get("return_properties") or [])
    return intent


def build_sparql(intent: dict) -> str:
    intent = _augment_value_projection(_augment_in_projection(intent))
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

        # value_owner: the entity each aggregated value belongs to (an Observation
        # for a measured value, a Node for an altitude) — what n_values counts.
        if raw_agg_target in known_class_vars:
            agg_target = "?" + raw_agg_target
            value_owner = agg_target
        elif raw_agg_target in known_prop_vars:
            agg_target = "?" + raw_agg_target
            prop_key = _strip_prefix(aggregation.get("target", ""))
            prop_full = _prop(aggregation.get("target", ""))
            domain = PROP_DOMAIN.get(prop_key)
            anchor = join_vars.get(domain, target_var) if domain else target_var
            required_line = f"  {anchor} {prop_full} {agg_target} ."
            if required_line not in lines:
                lines.append(required_line)
            value_owner = anchor
        elif _strip_prefix(aggregation.get("target", "")) in PROP_MAP:
            agg_target = "?" + raw_agg_target
            prop_key = _strip_prefix(aggregation.get("target", ""))
            prop_full = _prop(aggregation.get("target", ""))
            domain = PROP_DOMAIN.get(prop_key)
            anchor = join_vars.get(domain, target_var) if domain else target_var
            lines.append(f"  {anchor} {prop_full} {agg_target} .")
            value_owner = anchor
        elif raw_agg_target and aggregation.get("type", "count").lower() != "count":
            # A property the schema maps don't list (e.g. altitude) and nobody
            # projected: bind it on the target — aggregating the target's URI
            # itself would make MIN/MAX/AVG meaningless.
            agg_target = "?" + raw_agg_target
            lines.append(f"  {target_var} {_prop(aggregation.get('target', ''))} {agg_target} .")
            value_owner = target_var
        else:
            agg_target = target_var
            value_owner = target_var

        group_name = _resolve_group_var(aggregation.get("group_by"), joins)
        bucket = aggregation.get("time_bucket")
        if bucket in TIME_BUCKETS:
            # One group per UTC day/month of the reading time (analysis_temp).
            owner = (target_var if _strip_prefix(target_class) in TIME_CLASSES
                     else join_vars.get("ObservationCollection") or join_vars.get("Observation"))
            if owner is None:
                owner = "?_bucket_oc"
                lines.append(f"  ?_bucket_oc {_prop('hasObservation')} {target_var} .")
            lines.append(f"  {owner} sosa:resultTime ?_bucket_time .")
            lines.append(f"  {bucket_bind('?_bucket_time', bucket)}")
            if "time" in group_name or "date" in group_name:
                group_name = ""          # the bucket replaces grouping on the raw timestamp
            group_name = f"{group_name} ?{bucket}".strip() if group_name else bucket
        group_var = " ".join(f"?{g.lstrip('?')}" for g in group_name.split()) if group_name else ""

        agg_var = f"?{agg_type.lower()}"

        use_distinct = aggregation.get("distinct", agg_type == "COUNT")
        distinct_kw = "DISTINCT " if use_distinct else ""
        if agg_type == "RANGE":
            # min and max together (a value range, a time span); their difference
            # only for numbers — xsd:dateTime subtraction is not portable SPARQL.
            agg_var = "?min"
            agg_expr = f"(MIN({agg_target}) AS ?min) (MAX({agg_target}) AS ?max)"
            if "time" not in agg_target.lower() and "date" not in agg_target.lower():
                agg_expr += f" ((MAX({agg_target}) - MIN({agg_target})) AS ?range)"
        else:
            agg_expr = f"({agg_type}({distinct_kw}{agg_target}) AS {agg_var})"
        if agg_type != "COUNT":
            # How many values the aggregate ran over (distinct value owners, e.g.
            # observations or nodes — not joined rows). 0 means nothing matched,
            # which AVG/SUM would otherwise report as a plain 0.
            agg_expr += f" (COUNT(DISTINCT {value_owner}) AS ?n_values)"
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
        if aggregation and ovar not in group_var.split():
            # Grouped rows can only be ranked by the group key or the aggregate;
            # anything else ("avg_hasSimpleResult", "hasSimpleResult") means the aggregate.
            ovar = agg_var
        odir = order_by.get("direction", "ASC")
        order_clause = f"\nORDER BY {odir}({ovar})"
        if limit and not aggregation:
            # top-N ranks by the value: unbound sorts first in ASC (see subquery path)
            where_clause = where_clause[:-2] + f"\n  FILTER(BOUND({ovar}))\n}}"

    limit_clause = ""
    if limit:
        limit_clause = f"\nLIMIT {int(limit)}"

    return (PREFIXES + "\n" + select_clause + "\n" + where_clause
            + group_clause + order_clause + limit_clause)


# ── What the parser and the answer generator are told about this layer ───────
# The intent language is defined here, by the compiler that executes it (time
# filters and buckets: analysis_temp.py); the parser prompt and the answer
# prompt import these texts, so what the LLM is told is what this code does.

PARSER_OPERATORS = """\
  contains  — case-insensitive substring match on string literals
  equals    — exact case-insensitive match
  gt / lt   — numeric comparison (for measured values)
  in        — matches any of a list of values (case-insensitive), e.g. two named nodes or several sites"""

PARSER_GUIDE = """\
  - For COUNT aggregations: set "target" to the class name in lowercase (e.g. "sensor"), distinct=true. For min/max/avg/sum: set "target" to the property name (e.g. "hasSimpleResult"), distinct=false.
  - AGGREGATE FIRST — this is a correctness rule, not an optimisation. If the question asks for a statistic ("average", "mean", "total", "sum", "how many", "highest", "lowest", "maximum", "minimum"), you MUST set "aggregation" so the statistic is computed inside the query. Detail rows go through DISTINCT de-duplication, so any average, sum or count derived from them afterwards is WRONG (measured: 15% error on an average). Only omit "aggregation" when the user genuinely wants the individual values listed, or when the statistic depends on distances between nodes (see the spatial rules: those are computed downstream from the coordinates).
  - When aggregating on a property, put it in "aggregation.target" only — it does not also need to be in return_properties. Set group_by to null for a single overall figure, or to "ClassName.property" for a per-group breakdown.
  - group_by and order_by variables MUST use the dotted "ClassName.property" form (e.g. "Site.label", "ObservationCollection.resultTime"). The join for that class MUST be present and include the property in return_properties.
  - "latest/most recent N readings/values/measurements": one reading = one Observation, so set target_class=Observation (NOT ObservationCollection) and limit=N; join ObservationCollection via hasObservation (incoming) returning resultTime, and order_by ObservationCollection.resultTime DESC. This makes LIMIT count individual readings. (A timestamp lives on the ObservationCollection, so reach it through that join.)
  - WHICH entity / WHEN / WHERE an extreme occurs ("which node is highest", "when was the maximum temperature recorded"): the answer is the entity or time, so use order_by on that value with limit 1 and return the label / resultTime — NOT an aggregation, which returns only the value. Use aggregation only when the value itself is asked ("what is the maximum temperature").
  - "range" aggregation: min and max together (and their difference for numbers) — for "what range", "how much spread", "over which dates does the data extend" (target resultTime). Never invent other aggregation types.
  - Several values of the same property (two named nodes, several sites): ONE filter with op "in" and a list — two "equals" filters on the same property can never both match."""

PARSER_EXAMPLES = """\
Q: "What are the temperature values recorded at each site?"
{
  "target_class": "ObservationCollection",
  "filters": [],
  "return_properties": [],
  "joins": [
    {"class": "Observation", "via": "hasObservation", "direction": "outgoing",
     "return_properties": ["hasSimpleResult"], "filters": []},
    {"class": "ObservedProperty", "via": "observedProperty", "direction": "outgoing",
     "return_properties": [], "filters": [{"property": "label", "op": "equals", "value": "temperature"}]},
    {"class": "Site", "via": "hasSite", "direction": "outgoing",
     "return_properties": ["label"], "filters": []}
  ],
  "aggregation": null,
  "order_by": null, "limit": null,
  "anomaly_check": false,
  "as_of": null,
  "explanation": "Lists the individual values, so no aggregation — contrast with 'average temperature', which must aggregate."
}

Q: "What is the average temperature at each site?"
{
  "target_class": "ObservationCollection",
  "filters": [],
  "return_properties": [],
  "joins": [
    {"class": "Observation", "via": "hasObservation", "direction": "outgoing",
     "return_properties": [], "filters": []},
    {"class": "ObservedProperty", "via": "observedProperty", "direction": "outgoing",
     "return_properties": [], "filters": [{"property": "label", "op": "equals", "value": "temperature"}]},
    {"class": "Site", "via": "hasSite", "direction": "outgoing",
     "return_properties": ["label"], "filters": []}
  ],
  "aggregation": {"type": "avg", "group_by": "Site.label",
                  "target": "hasSimpleResult", "distinct": false},
  "order_by": null, "limit": null,
  "anomaly_check": false,
  "as_of": null,
  "explanation": "AVG computed in the query over every observation, so de-duplication of detail rows cannot skew it."
}

Q: "How many sensors are deployed per site?"
{
  "target_class": "ObservationCollection",
  "filters": [],
  "return_properties": [],
  "joins": [
    {"class": "Sensor", "via": "madeBySensor", "direction": "outgoing",
     "return_properties": [], "filters": []},
    {"class": "Site", "via": "hasSite", "direction": "outgoing",
     "return_properties": ["label"], "filters": []}
  ],
  "aggregation": {"type": "count", "group_by": "Site.label",
                  "target": "sensor", "distinct": true},
  "order_by": null, "limit": null,
  "anomaly_check": false,
  "as_of": null,
  "explanation": "Count distinct sensors per site."
}

Q: "What are the latest 10 readings?"
{
  "target_class": "Observation",
  "filters": [],
  "return_properties": ["hasSimpleResult"],
  "joins": [
    {"class": "ObservationCollection", "via": "hasObservation", "direction": "incoming",
     "return_properties": ["resultTime"], "filters": []},
    {"class": "Site", "via": "hasSite", "direction": "outgoing",
     "return_properties": ["label"], "filters": []}
  ],
  "aggregation": null,
  "order_by": {"variable": "ObservationCollection.resultTime", "direction": "DESC"},
  "limit": 10,
  "anomaly_check": false,
  "as_of": null,
  "explanation": "10 most recent individual readings (Observations), ranked by their collection's resultTime so LIMIT counts readings, not collections."
}

Q: "Which physical quantities are measured at the delos site?"
{
  "target_class": "ObservationCollection",
  "filters": [],
  "return_properties": [],
  "joins": [
    {"class": "Site", "via": "hasSite", "direction": "outgoing",
     "return_properties": [], "filters": [{"property": "label", "op": "equals", "value": "delos"}]},
    {"class": "Observation", "via": "hasObservation", "direction": "outgoing",
     "return_properties": [], "filters": []},
    {"class": "ObservedProperty", "via": "observedProperty", "direction": "outgoing",
     "return_properties": ["label"], "filters": []}
  ],
  "aggregation": null,
  "order_by": null,
  "limit": null,
  "anomaly_check": false,
  "as_of": null,
  "explanation": "Forward-traverse from ObservationCollection to Site (filtered) → Observation → ObservedProperty to list distinct measured quantities."
}"""

ANSWER_GUIDE = """\
Statistics:
- When the query already computed an aggregate (a count/avg/min/max/sum column), report that value — it is the authoritative one.
- Otherwise the rows are a de-duplicated listing, so do NOT compute an average, total or record count from them; give the values, ranges or examples the rows support and leave it there.
- With many rows, summarise and name a few representative examples rather than enumerating everything.
- If the query has a LIMIT, the rows are only the top N it asked for — do not claim they are the only ones that exist."""


def execute(backend, sparql: str) -> list[dict[str, Any]]:
    return backend.query(sparql)


# ── URI unfolding ────────────────────────────────────────────────────────

from rdflib import URIRef
from rdflib.namespace import RDFS, RDF

import re

_RESOURCE_PREFIX = str(EX)
_SKIP_PREDS = {str(RDF.type)}
_RDFS_LABEL = str(RDFS.label)
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


def _resolve_uri(backend, uri_str: str, cache: dict, depth: int = 0) -> dict[str, str]:
    if uri_str in cache:
        return cache[uri_str]

    info = {}
    for pred_str, obj_str in backend.predicate_objects(uri_str):
        if pred_str in _SKIP_PREDS:
            continue
        key = _pred_short(pred_str)
        if key in info:
            continue
        if len(obj_str) > _MAX_VALUE_LEN:
            continue
        if _is_resource_uri(obj_str):
            if depth < 1:
                nested = _resolve_uri(backend, obj_str, cache, depth + 1)
                resolved = nested.get("label")
                if resolved:
                    info[key] = resolved
            else:
                for p2, o2 in backend.predicate_objects(obj_str):
                    if p2 == _RDFS_LABEL:
                        info[key] = o2
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


def unfold_results(backend, results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Unfold resource URIs in results into their linked properties, via the backend."""
    if not results or "error" in results[0]:
        return results

    # Warm the batch so a remote backend resolves all URIs in one round-trip.
    backend.prefetch([v for row in results for v in row.values() if _is_resource_uri(v)])

    cache: dict[str, dict] = {}
    unfolded = []

    for row in results:
        new_row = {}
        row_lower = {k.lower(): v for k, v in row.items()}
        for key, val in row.items():
            if _is_resource_uri(val):
                info = _resolve_uri(backend, val, cache)
                for info_key, info_val in info.items():
                    cleaned = _clean_value(info_val)
                    if cleaned is None:
                        continue
                    # Unfolding a URI re-emits properties the query already
                    # selected directly (?node → node_label beside ?label).
                    # Drop the copy only when name and value both match.
                    direct = row_lower.get(info_key.lower())
                    if direct is not None and str(direct) == str(cleaned):
                        continue
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
