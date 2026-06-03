"""
KG Store — loads panoptes3.owl and populates it with dummy cultural-heritage
instance data aligned with the ARGUS Panoptes ontology.
"""

from __future__ import annotations
from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, Literal, URIRef
from rdflib.namespace import XSD

PAN  = Namespace("http://www.argus-project.eu/")
INST = Namespace("http://www.argus-project.eu/instance/")
GEO  = Namespace("http://www.opengis.net/ont/geosparql#")

OWL_PATH = Path(__file__).parent / "panoptes3.owl"


def build_graph() -> Graph:
    g = Graph()
    g.bind("pan",  PAN)
    g.bind("inst", INST)
    g.bind("geo",  GEO)
    g.parse(str(OWL_PATH))
    _add_instances(g)
    return g


def _add_instances(g: Graph) -> None:
    # ------------------------------------------------------------------ Assets
    assets = [
        ("parthenon",      "Parthenon",         "Greece",  "37.9715,23.7267",
         "Classical",      "marble",            "fair"),
        ("hagia_sophia",   "Hagia Sophia",       "Turkey",  "41.0086,28.9802",
         "Byzantine",      "brick and marble",  "good"),
        ("colosseum",      "Colosseum",          "Italy",   "41.8902,12.4922",
         "Roman",          "travertine",        "fair"),
        ("dubrovnik",      "Dubrovnik Old Town", "Croatia", "42.6406,18.1083",
         "Medieval",       "limestone",         "good"),
        ("pompeii",        "Pompeii",            "Italy",   "40.7502,14.4890",
         "Roman",          "various",           "damaged"),
        ("alhambra",       "Alhambra",           "Spain",   "37.1760,-3.5881",
         "Islamic",        "stucco and marble", "good"),
    ]
    for uid, name, country, coords, style, material, condition in assets:
        a = INST[uid]
        g.add((a, RDF.type,                 PAN.Asset))
        g.add((a, PAN.name,                 Literal(name)))
        g.add((a, PAN.country,              Literal(country)))
        g.add((a, PAN.coordinates,          Literal(coords)))
        g.add((a, PAN.architectural_style,  Literal(style)))
        g.add((a, PAN.material_used,        Literal(material)))
        g.add((a, PAN.current_condition,    Literal(condition)))

    # Additional construction periods
    g.add((INST.parthenon,   PAN.construction_period, Literal("447–432 BC")))
    g.add((INST.hagia_sophia,PAN.construction_period, Literal("532–537 AD")))
    g.add((INST.colosseum,   PAN.construction_period, Literal("70–80 AD")))
    g.add((INST.dubrovnik,   PAN.construction_period, Literal("7th–18th century")))
    g.add((INST.pompeii,     PAN.construction_period, Literal("6th century BC – 79 AD")))
    g.add((INST.alhambra,    PAN.construction_period, Literal("13th–14th century")))

    # --------------------------------------------------------------- Events
    events = [
        ("evt_earthquake_2023", "Seismic event recorded near Parthenon", "2023-02-06",
         INST.parthenon),
        ("evt_flood_2020",      "Heavy coastal flooding in Dubrovnik area", "2020-11-21",
         INST.dubrovnik),
        ("evt_fire_2022",       "Wildfire threat near Colosseum", "2022-07-19",
         INST.colosseum),
        ("evt_earthquake_2021", "Minor tremor affecting Pompeii excavation site", "2021-09-30",
         INST.pompeii),
    ]
    for uid, desc, date, asset in events:
        e = INST[uid]
        g.add((e,     RDF.type,         PAN.Event))
        g.add((e,     PAN.name,         Literal(desc)))
        g.add((e,     PAN.event_date,   Literal(date, datatype=XSD.date)))
        g.add((asset, PAN.hasEvent,     e))

    # --------------------------------------------------------------- Threats
    threats = [
        ("threat_earthquake_parthenon", "High seismic risk due to tectonic activity", "high",
         INST.parthenon, INST.evt_earthquake_2023),
        ("threat_flood_dubrovnik",      "Coastal flood risk from storm surges",       "medium",
         INST.dubrovnik, INST.evt_flood_2020),
        ("threat_fire_colosseum",       "Wildfire risk from dry vegetation nearby",   "low",
         INST.colosseum, INST.evt_fire_2022),
        ("threat_earthquake_pompeii",   "Seismic risk to unexcavated ruins",          "medium",
         INST.pompeii,   INST.evt_earthquake_2021),
    ]
    for uid, desc, level, asset, event in threats:
        t = INST[uid]
        g.add((t,     RDF.type,               PAN.Threat))
        g.add((t,     PAN.threat_description, Literal(desc)))
        g.add((t,     PAN.threat_level,       Literal(level)))
        g.add((event, PAN.generatesThreat,    t))
        g.add((asset, PAN.isTriggeredBy,      t))

    # -------------------------------------------------------- Risk Assessments
    risks = [
        ("risk_parthenon", INST.parthenon, INST.threat_earthquake_parthenon,
         "0.3", "0.8", "0.5", "5.2"),
        ("risk_dubrovnik", INST.dubrovnik, INST.threat_flood_dubrovnik,
         "0.2", "0.6", "0.3", "3.6"),
        ("risk_pompeii",   INST.pompeii,   INST.threat_earthquake_pompeii,
         "0.25","0.7", "0.4", "4.2"),
    ]
    for uid, asset, threat, freq, loss, frac, mr in risks:
        r = INST[uid]
        g.add((r, RDF.type,            PAN.RiskAssessment))
        g.add((r, PAN.assessesRiskFor, asset))
        g.add((r, PAN.relatedThreat,   threat))
        g.add((r, PAN.FrequencyA,      Literal(freq,  datatype=XSD.float)))
        g.add((r, PAN.LossB,           Literal(loss,  datatype=XSD.float)))
        g.add((r, PAN.FractionC,       Literal(frac,  datatype=XSD.float)))
        g.add((r, PAN.MagnitudeOfRisk, Literal(mr,    datatype=XSD.float)))

    # ------------------------------------------------------------ Measurements
    measurements = [
        ("meas_seismic_parthenon", "seismic activity", "2.3",  "Richter",
         INST.parthenon),
        ("meas_humidity_hagia",    "relative humidity", "68",  "%",
         INST.hagia_sophia),
        ("meas_temp_colosseum",    "surface temperature","24.5","°C",
         INST.colosseum),
        ("meas_seismic_pompeii",   "seismic activity",  "1.8", "Richter",
         INST.pompeii),
    ]
    for uid, qtype, val, unit, asset in measurements:
        m = INST[uid]
        q = INST[uid + "_qty"]
        g.add((m,     RDF.type,           PAN.Measurement))
        g.add((m,     PAN.measures,       asset))
        g.add((m,     PAN.quantifies,     q))
        g.add((q,     RDF.type,           PAN.Quantity))
        g.add((q,     PAN.name,           Literal(qtype)))
        g.add((q,     PAN.quantity_value, Literal(val,  datatype=XSD.float)))
        g.add((q,     PAN.quantity_unit,  Literal(unit)))

    # --------------------------------------------------------- Cultural Docs
    docs = [
        ("doc_parthenon_survey", "Parthenon Structural Survey 2022",
         "2022-06-01", "English", INST.parthenon),
        ("doc_pompeii_report",   "Pompeii Excavation and Conservation Report",
         "2021-11-15", "Italian", INST.pompeii),
    ]
    for uid, title, date, lang, asset in docs:
        d = INST[uid]
        g.add((d,     RDF.type,                 PAN.CulturalDocumentation))
        g.add((d,     PAN.documentation_title,  Literal(title)))
        g.add((d,     PAN.creation_date,        Literal(date, datatype=XSD.date)))
        g.add((d,     PAN.language,             Literal(lang)))
        g.add((d,     PAN.documents,            asset))
