"""
Ontology metadata extracted from the OWL files: shared namespaces, structured
maps for the SPARQL builder, and schema text for the LLM prompt.
"""

from __future__ import annotations

from pathlib import Path
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import OWL, RDF, RDFS

# ── Shared namespaces ────────────────────────────────────────────────────────

SOSA = Namespace("http://www.w3.org/ns/sosa/")
ARGUS = Namespace("http://www.argus-project.eu/ontology/")
EX = Namespace("http://www.argus-project.eu/resource/")
PANOPTES = Namespace("http://www.argus-project.eu/panoptes#")

OWL_DIR = Path(__file__).resolve().parent.parent / "material"
OWL_FILES = [
    OWL_DIR / "panoptes3.owl",
    OWL_DIR / "panoptes3_extension.owl",
]

# The prompt describes only the extension, which declares exactly the classes the
# readings graph instantiates. The base ontology adds ~18 classes (Asset, Decision,
# Measurement, …) that have no instances — offering them as target_class choices
# costs tokens and invites queries that can only return nothing.
SCHEMA_OWL_FILES = [OWL_DIR / "panoptes3_extension.owl"]

_PREFIX_MAP = {
    "http://www.w3.org/ns/sosa/": "sosa:",
    "http://www.argus-project.eu/ontology/": "argus:",
    "http://www.argus-project.eu/panoptes#": "panoptes:",
    "http://www.w3.org/2000/01/rdf-schema#": "rdfs:",
    "http://www.w3.org/2001/XMLSchema#": "xsd:",
    "http://www.w3.org/ns/ssn/": "ssn:",
    "http://www.opengis.net/ont/geosparql#": "geo:",
    "http://www.w3.org/ns/prov#": "prov:",
    "http://www.w3.org/2006/time#": "time:",
    "http://www.cidoc-crm.org/cidoc-crm/": "crm:",
    "http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#": "dul:",
    "http://purl.org/dc/elements/1.1/": "dc:",
}


# ── Helpers ──────────────────────────────────────────────────────────────────

def _short(uri: URIRef) -> str:
    s = str(uri)
    for full, prefix in _PREFIX_MAP.items():
        if s.startswith(full):
            return prefix + s[len(full):]
    return s.rsplit("/", 1)[-1].rsplit("#", 1)[-1]


def _local(uri: URIRef) -> str:
    s = str(uri)
    for full in _PREFIX_MAP:
        if s.startswith(full):
            return s[len(full):]
    return s.rsplit("/", 1)[-1].rsplit("#", 1)[-1]


def _label(g: Graph, uri: URIRef) -> str:
    for lit in g.objects(uri, RDFS.label):
        return str(lit)
    return ""


def _comment(g: Graph, uri: URIRef) -> str:
    for lit in g.objects(uri, RDFS.comment):
        return str(lit)
    return ""


def _superclass(g: Graph, uri: URIRef) -> str | None:
    for parent in g.objects(uri, RDFS.subClassOf):
        if isinstance(parent, URIRef):
            return _short(parent)
    return None


# ── Load OWL graph ───────────────────────────────────────────────────────────

_cached_graph: Graph | None = None
_cached_schema_graph: Graph | None = None


def _load(files: list[Path]) -> Graph:
    g = Graph()
    for owl_file in files:
        if owl_file.exists():
            g.parse(str(owl_file), format="xml")
    return g


def load_ontology_graph() -> Graph:
    # Full vocabulary — drives the SPARQL builder's name resolution.
    global _cached_graph
    if _cached_graph is None:
        _cached_graph = _load(OWL_FILES)
    return _cached_graph


def load_schema_graph() -> Graph:
    # Prompt-facing subset (see SCHEMA_OWL_FILES).
    global _cached_schema_graph
    if _cached_schema_graph is None:
        _cached_schema_graph = _load(SCHEMA_OWL_FILES)
    return _cached_schema_graph


# ── Structured extractions (for sparql_retriever) ───────────────────────────

def extract_class_map(g: Graph | None = None) -> dict[str, str]:
    """Map short class name → prefixed name, e.g. {"Site": "argus:Site"}."""
    if g is None:
        g = load_ontology_graph()
    result = {}
    for cls in g.subjects(RDF.type, OWL.Class):
        if not isinstance(cls, URIRef):
            continue
        local = _local(cls)
        prefixed = _short(cls)
        result[local] = prefixed
    return result


def extract_prop_map(g: Graph | None = None) -> dict[str, str]:
    """Map short property name → prefixed name, e.g. {"hasSite": "argus:hasSite"}."""
    if g is None:
        g = load_ontology_graph()
    result = {}
    for prop_type in (OWL.ObjectProperty, OWL.DatatypeProperty):
        for prop in g.subjects(RDF.type, prop_type):
            if not isinstance(prop, URIRef):
                continue
            local = _local(prop)
            prefixed = _short(prop)
            result[local] = prefixed
    result["label"] = "rdfs:label"
    return result


def extract_object_props(g: Graph | None = None) -> set[str]:
    """Set of property names that are object properties (both short and prefixed forms)."""
    if g is None:
        g = load_ontology_graph()
    result = set()
    for prop in g.subjects(RDF.type, OWL.ObjectProperty):
        if not isinstance(prop, URIRef):
            continue
        local = _local(prop)
        prefixed = _short(prop)
        result.add(local)
        result.add(prefixed)
    return result


def extract_prop_domain(g: Graph | None = None) -> dict[str, str]:
    """Map short property name → domain class short name, e.g. {"hasSite": "ObservationCollection"}."""
    if g is None:
        g = load_ontology_graph()
    result = {}
    for prop_type in (OWL.ObjectProperty, OWL.DatatypeProperty):
        for prop in g.subjects(RDF.type, prop_type):
            if not isinstance(prop, URIRef):
                continue
            local = _local(prop)
            for domain in g.objects(prop, RDFS.domain):
                if isinstance(domain, URIRef):
                    result[local] = _local(domain)
                    break
    return result


def extract_prop_range(g: Graph | None = None) -> dict[str, str]:
    """Map short property name → range class short name, e.g. {"hasObservation": "Observation"}."""
    if g is None:
        g = load_ontology_graph()
    result = {}
    for prop in g.subjects(RDF.type, OWL.ObjectProperty):
        if not isinstance(prop, URIRef):
            continue
        local = _local(prop)
        for range_cls in g.objects(prop, RDFS.range):
            if isinstance(range_cls, URIRef):
                result[local] = _local(range_cls)
                break
    return result


def extract_class_list(g: Graph | None = None) -> str:
    """Comma-separated list of short class names for the LLM prompt."""
    if g is None:
        g = load_schema_graph()
    names = set()
    for cls in g.subjects(RDF.type, OWL.Class):
        if isinstance(cls, URIRef):
            names.add(_local(cls))
    return ", ".join(sorted(names))


# ── Human-readable schema text (for LLM prompt) ─────────────────────────────

def extract_schema_text(g: Graph | None = None) -> str:
    if g is None:
        g = load_schema_graph()

    used_prefixes = {_short(t).split(":")[0] + ":"
                     for t in set(g.subjects()) | set(g.predicates()) | set(g.objects())
                     if isinstance(t, URIRef) and ":" in _short(t)}

    lines: list[str] = []
    lines.append("ARGUS ontology (auto-generated from panoptes3_extension.owl)")
    lines.append("")

    lines.append("Namespaces:")
    for full, prefix in sorted(_PREFIX_MAP.items(), key=lambda x: x[1]):
        if prefix in used_prefixes:
            lines.append(f"  {prefix:12s} <{full}>")
    lines.append("")

    # Classes
    classes: list[tuple[str, str, str, str | None]] = []
    for cls in sorted(set(g.subjects(RDF.type, OWL.Class)), key=str):
        if not isinstance(cls, URIRef):
            continue
        short = _short(cls)
        label = _label(g, cls)
        comment = _comment(g, cls)
        parent = _superclass(g, cls)
        classes.append((short, label, comment, parent))

    lines.append("Classes:")
    for short, label, comment, parent in classes:
        desc_parts = []
        if parent:
            desc_parts.append(f"subClassOf {parent}")
        if label:
            desc_parts.append(label)
        if comment:
            desc_parts.append(comment)
        desc = " — " + "; ".join(desc_parts) if desc_parts else ""
        lines.append(f"  {short}{desc}")
    lines.append("")

    # Properties grouped by domain
    domain_props: dict[str, list[str]] = {}

    for prop_type, prop_kind in [(OWL.ObjectProperty, "object"), (OWL.DatatypeProperty, "datatype")]:
        for prop in sorted(set(g.subjects(RDF.type, prop_type)), key=str):
            if not isinstance(prop, URIRef):
                continue
            short = _short(prop)
            label = _label(g, prop)

            domains = [_short(d) for d in g.objects(prop, RDFS.domain) if isinstance(d, URIRef)]
            ranges = [_short(r) for r in g.objects(prop, RDFS.range) if isinstance(r, URIRef)]

            domain_key = domains[0] if domains else "(general)"
            range_str = ranges[0] if ranges else "literal"

            if prop_kind == "object":
                entry = f"  {short:30s} → {range_str}"
            else:
                entry = f"  {short:30s} ({range_str})"

            if label:
                entry += f"  — {label}"

            domain_props.setdefault(domain_key, []).append(entry)

    lines.append("Properties (grouped by domain class — domain →(property)→ range):")
    for domain in sorted(domain_props):
        lines.append(f"\n  [{domain}]")
        for entry in sorted(domain_props[domain]):
            lines.append(entry)

    return "\n".join(lines)


_cached_schema: str | None = None


def get_ontology_schema() -> str:
    global _cached_schema
    if _cached_schema is None:
        _cached_schema = extract_schema_text()
    return _cached_schema
