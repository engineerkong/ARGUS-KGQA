"""
KG Store — loads panoptes3.owl and populates it with dummy cultural-heritage
instance data aligned with the ARGUS Panoptes ontology.

Sensor data model:
  Each Measurement represents one on-site sensor reading tied to:
    - a specific Asset  (via pan:measures)
    - a timestamp       (pan:observation_time  xsd:dateTime)
    - a sensor location (pan:sensor_lat / pan:sensor_lon + GeoSPARQL geometry)
  Multiple Measurements per asset simulate a real time series.
"""

from __future__ import annotations
from pathlib import Path
from rdflib import Graph, Namespace, RDF, Literal, URIRef
from rdflib.namespace import XSD

PAN     = Namespace("http://www.argus-project.eu/")
INST    = Namespace("http://www.argus-project.eu/instance/")
GEO     = Namespace("http://www.opengis.net/ont/geosparql#")
WKT_LIT = URIRef("http://www.opengis.net/ont/geosparql#wktLiteral")

OWL_PATH = Path(__file__).parent / "panoptes3.owl"


def build_graph() -> Graph:
    g = Graph()
    g.bind("pan",  PAN)
    g.bind("inst", INST)
    g.bind("geo",  GEO)
    g.parse(str(OWL_PATH))
    _add_instances(g)
    return g


def _wkt_point(lon: float, lat: float) -> Literal:
    return Literal(f"POINT({lon} {lat})", datatype=WKT_LIT)


def _add_instances(g: Graph) -> None:

    # ------------------------------------------------------------------ Assets
    # (uid, name, country, lat, lon, style, material, condition, period)
    assets = [
        ("parthenon",    "Parthenon",         "Greece",  37.9715,  23.7267,
         "Classical",      "marble",            "fair",    "447–432 BC"),
        ("hagia_sophia", "Hagia Sophia",       "Turkey",  41.0086,  28.9802,
         "Byzantine",      "brick and marble",  "good",    "532–537 AD"),
        ("colosseum",    "Colosseum",          "Italy",   41.8902,  12.4922,
         "Roman",          "travertine",        "fair",    "70–80 AD"),
        ("dubrovnik",    "Dubrovnik Old Town", "Croatia", 42.6406,  18.1083,
         "Medieval",       "limestone",         "good",    "7th–18th century"),
        ("pompeii",      "Pompeii",            "Italy",   40.7502,  14.4890,
         "Roman",          "various",           "damaged", "6th century BC – 79 AD"),
        ("alhambra",     "Alhambra",           "Spain",   37.1760,  -3.5881,
         "Islamic",        "stucco and marble", "good",    "13th–14th century"),
    ]
    for uid, name, country, lat, lon, style, material, condition, period in assets:
        a = INST[uid]
        g.add((a, RDF.type,                PAN.Asset))
        g.add((a, PAN.name,                Literal(name)))
        g.add((a, PAN.country,             Literal(country)))
        g.add((a, PAN.latitude,            Literal(str(lat), datatype=XSD.float)))
        g.add((a, PAN.longitude,           Literal(str(lon), datatype=XSD.float)))
        g.add((a, PAN.coordinates,         Literal(f"{lat},{lon}")))
        g.add((a, PAN.architectural_style, Literal(style)))
        g.add((a, PAN.material_used,       Literal(material)))
        g.add((a, PAN.current_condition,   Literal(condition)))
        g.add((a, PAN.construction_period, Literal(period)))
        # GeoSPARQL geometry
        geom = INST[uid + "_geom"]
        g.add((a,    GEO.hasGeometry, geom))
        g.add((geom, RDF.type,        GEO.Geometry))
        g.add((geom, GEO.asWKT,       _wkt_point(lon, lat)))

    # --------------------------------------------------------------- Events
    events = [
        ("evt_earthquake_2023", "Seismic event recorded near Parthenon",    "2023-02-06", INST.parthenon),
        ("evt_flood_2020",      "Heavy coastal flooding in Dubrovnik area",  "2020-11-21", INST.dubrovnik),
        ("evt_fire_2022",       "Wildfire threat near Colosseum",            "2022-07-19", INST.colosseum),
        ("evt_earthquake_2021", "Minor tremor at Pompeii excavation site",   "2021-09-30", INST.pompeii),
    ]
    for uid, desc, date, asset in events:
        e = INST[uid]
        g.add((e,     RDF.type,       PAN.Event))
        g.add((e,     PAN.name,       Literal(desc)))
        g.add((e,     PAN.event_date, Literal(date, datatype=XSD.date)))
        g.add((asset, PAN.hasEvent,   e))

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
        ("risk_parthenon", INST.parthenon, INST.threat_earthquake_parthenon, 0.3, 0.8, 0.5, 5.2),
        ("risk_dubrovnik", INST.dubrovnik, INST.threat_flood_dubrovnik,      0.2, 0.6, 0.3, 3.6),
        ("risk_pompeii",   INST.pompeii,   INST.threat_earthquake_pompeii,   0.25,0.7, 0.4, 4.2),
    ]
    for uid, asset, threat, freq, loss, frac, mr in risks:
        r = INST[uid]
        g.add((r, RDF.type,            PAN.RiskAssessment))
        g.add((r, PAN.assessesRiskFor, asset))
        g.add((r, PAN.relatedThreat,   threat))
        g.add((r, PAN.FrequencyA,      Literal(freq, datatype=XSD.float)))
        g.add((r, PAN.LossB,           Literal(loss, datatype=XSD.float)))
        g.add((r, PAN.FractionC,       Literal(frac, datatype=XSD.float)))
        g.add((r, PAN.MagnitudeOfRisk, Literal(mr,   datatype=XSD.float)))

    # ---- On-site sensor time series ----------------------------------------
    # Simulates sensors deployed at or near each heritage site.
    # Each row: (uid, asset, obs_time, sensor_lat, sensor_lon, qty_type, value, unit)
    sensor_readings = [
        # Seismometer near Parthenon (37.9718 N, 23.7270 E)
        ("meas_seis_parth_1", INST.parthenon,    "2023-01-15T10:00:00", 37.9718, 23.7270, "seismic activity", 1.2, "Richter"),
        ("meas_seis_parth_2", INST.parthenon,    "2023-02-06T14:30:00", 37.9718, 23.7270, "seismic activity", 2.3, "Richter"),
        ("meas_seis_parth_3", INST.parthenon,    "2023-03-20T08:00:00", 37.9718, 23.7270, "seismic activity", 0.8, "Richter"),
        ("meas_seis_parth_4", INST.parthenon,    "2023-06-10T11:15:00", 37.9718, 23.7270, "seismic activity", 0.5, "Richter"),
        # Humidity sensor inside Hagia Sophia (41.0088 N, 28.9800 E)
        ("meas_humi_hagia_1", INST.hagia_sophia, "2022-06-01T09:00:00", 41.0088, 28.9800, "relative humidity", 65.0, "%"),
        ("meas_humi_hagia_2", INST.hagia_sophia, "2022-12-01T09:00:00", 41.0088, 28.9800, "relative humidity", 72.0, "%"),
        ("meas_humi_hagia_3", INST.hagia_sophia, "2023-06-01T09:00:00", 41.0088, 28.9800, "relative humidity", 68.0, "%"),
        # Surface thermometer at Colosseum (41.8900 N, 12.4925 E)
        ("meas_temp_colos_1", INST.colosseum,    "2022-07-01T12:00:00", 41.8900, 12.4925, "surface temperature", 28.5, "°C"),
        ("meas_temp_colos_2", INST.colosseum,    "2022-10-01T12:00:00", 41.8900, 12.4925, "surface temperature", 18.2, "°C"),
        ("meas_temp_colos_3", INST.colosseum,    "2023-07-01T12:00:00", 41.8900, 12.4925, "surface temperature", 29.1, "°C"),
        # Seismometer at Pompeii (40.7505 N, 14.4892 E)
        ("meas_seis_pompe_1", INST.pompeii,      "2021-09-30T16:00:00", 40.7505, 14.4892, "seismic activity", 1.8, "Richter"),
        ("meas_seis_pompe_2", INST.pompeii,      "2022-04-15T11:00:00", 40.7505, 14.4892, "seismic activity", 0.9, "Richter"),
        ("meas_seis_pompe_3", INST.pompeii,      "2023-05-20T07:00:00", 40.7505, 14.4892, "seismic activity", 1.1, "Richter"),
        # Structural tilt sensor at Dubrovnik (42.6408 N, 18.1085 E)
        ("meas_tilt_dubr_1",  INST.dubrovnik,    "2022-11-20T15:00:00", 42.6408, 18.1085, "structural tilt",    0.02, "degrees"),
        ("meas_tilt_dubr_2",  INST.dubrovnik,    "2023-03-15T10:30:00", 42.6408, 18.1085, "structural tilt",    0.03, "degrees"),
        # Air quality sensor at Alhambra (37.1762 N, -3.5879 E)
        ("meas_air_alham_1",  INST.alhambra,     "2023-01-10T08:00:00", 37.1762, -3.5879, "air quality index",  45.0, "AQI"),
        ("meas_air_alham_2",  INST.alhambra,     "2023-08-15T14:00:00", 37.1762, -3.5879, "air quality index",  62.0, "AQI"),
    ]

    for uid, asset, obs_time, s_lat, s_lon, qty_type, val, unit in sensor_readings:
        m    = INST[uid]
        q    = INST[uid + "_qty"]
        geom = INST[uid + "_sensor_geom"]

        # Measurement node
        g.add((m, RDF.type,             PAN.Measurement))
        g.add((m, PAN.measures,         asset))
        g.add((m, PAN.observation_time, Literal(obs_time, datatype=XSD.dateTime)))
        g.add((m, PAN.sensor_lat,       Literal(str(s_lat), datatype=XSD.float)))
        g.add((m, PAN.sensor_lon,       Literal(str(s_lon), datatype=XSD.float)))
        g.add((m, PAN.quantifies,       q))

        # Sensor location geometry (GeoSPARQL)
        g.add((m,    PAN.hasSensorLocation, geom))
        g.add((geom, RDF.type,              GEO.Geometry))
        g.add((geom, GEO.asWKT,            _wkt_point(s_lon, s_lat)))

        # Quantity node
        g.add((q, RDF.type,           PAN.Quantity))
        g.add((q, PAN.name,           Literal(qty_type)))
        g.add((q, PAN.quantity_value, Literal(str(val), datatype=XSD.float)))
        g.add((q, PAN.quantity_unit,  Literal(unit)))

    # --------------------------------------------------------- Cultural Docs
    docs = [
        ("doc_parthenon_survey", "Parthenon Structural Survey 2022",
         "2022-06-01", "English", INST.parthenon),
        ("doc_pompeii_report",   "Pompeii Excavation and Conservation Report",
         "2021-11-15", "Italian", INST.pompeii),
    ]
    for uid, title, date, lang, asset in docs:
        d = INST[uid]
        g.add((d, RDF.type,                PAN.CulturalDocumentation))
        g.add((d, PAN.documentation_title, Literal(title)))
        g.add((d, PAN.creation_date,       Literal(date, datatype=XSD.date)))
        g.add((d, PAN.language,            Literal(lang)))
        g.add((d, PAN.documents,           asset))
