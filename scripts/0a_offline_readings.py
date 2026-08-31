"""
Step 0a — fetch ARGUS readings and build a local SOSA/ARGUS Turtle knowledge
graph, for the dev-mode RdflibBackend. For a live deployment against Postgres +
Ontop, use 0b_online_ingest.py instead.

    python scripts/0a_offline_readings.py                    # full run
    python scripts/0a_offline_readings.py --max-records 500  # limit records
    python scripts/0a_offline_readings.py --resume           # incremental update
    python scripts/0a_offline_readings.py --enrich-geo-only  # only refresh node coordinates
"""

import argparse
import csv
import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException
from urllib3.util.retry import Retry
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import RDFS, XSD
from ontology_schema import SOSA, ARGUS, EX, PANOPTES


# ---------------------------------------------------------------------------
# Paths — all output goes to ARGUS-KGQA/data/
# ---------------------------------------------------------------------------

_DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR = Path(os.environ.get("ARGUS_DATA_DIR", str(_DEFAULT_DATA_DIR)))

TTL_FILE = DATA_DIR / "argus_readings.ttl"
STATE_FILE = DATA_DIR / "argus_readings_state.json"
SEEN_IDS_FILE = DATA_DIR / "argus_seen_ids.txt"
BACKUP_FILE = DATA_DIR / "argus_readings.backup.ttl"

# Raw API payloads are never queried by the pipeline but measured 42% of the TTL,
# so they live in an append-only sidecar instead of as rdfs literals. Set
# ARGUS_KEEP_RAW_JSON=1 to also embed them in the graph (legacy behaviour).
RAW_JSONL_FILE = DATA_DIR / "argus_readings_raw.jsonl"
KEEP_RAW_JSON_IN_GRAPH = os.environ.get("ARGUS_KEEP_RAW_JSON", "") == "1"

# Per-node coordinates live in material/ARGUS_nodes.csv (site,nodeid,
# latitude,longitude,altitude), one row per node across all sites.
MATERIAL_DIR = Path(__file__).resolve().parent.parent / "material"
NODES_CSV = MATERIAL_DIR / "ARGUS_nodes.csv"

_node_coords: Dict[str, Dict[str, float]] | None = None

# Site names carry accents (e.g. "Baltanás"), so this CSV is not always UTF-8.
# latin-1 decodes any byte, so it is the guaranteed last resort.
_CSV_ENCODINGS = ("utf-8-sig", "utf-8", "cp1252", "latin-1")


def _read_csv_rows(csv_path: Path) -> List[Dict[str, str]]:
    for encoding in _CSV_ENCODINGS:
        try:
            with open(csv_path, newline="", encoding=encoding) as f:
                return list(csv.DictReader(f))
        except UnicodeDecodeError:
            continue
    print(f"WARNING: could not decode {csv_path} with any of {_CSV_ENCODINGS}; skipping.")
    return []


def _load_node_coords() -> Dict[str, Dict[str, float]]:
    global _node_coords
    if _node_coords is not None:
        return _node_coords
    coords: Dict[str, Dict[str, float]] = {}
    for row in _read_csv_rows(NODES_CSV):
        nid = (row.get("nodeid") or "").strip()
        if not nid:
            continue
        try:
            coords[nid] = {
                "latitude": float(row["latitude"]),
                "longitude": float(row["longitude"]),
                "altitude": float(row["altitude"]),
            }
        except (KeyError, ValueError, TypeError):
            continue
    _node_coords = coords
    return coords


def _add_node_coords(g: Graph, node_uri: URIRef, node_id: str) -> None:
    coords = _load_node_coords().get(node_id)
    if not coords:
        return
    _add_literal(g, node_uri, ARGUS.latitude, coords["latitude"], XSD.decimal)
    _add_literal(g, node_uri, ARGUS.longitude, coords["longitude"], XSD.decimal)
    _add_literal(g, node_uri, ARGUS.altitude, coords["altitude"], XSD.decimal)


# ---------------------------------------------------------------------------
# ARGUS API
# ---------------------------------------------------------------------------

BASE_URL = os.environ.get("ARGUS_API_URL", "http://api.argusservices.athenarc.gr/api/readings")
API_ROOT = BASE_URL.rsplit("/", 1)[0]  # .../api/readings -> .../api

API_HEADERS = {"Accept": "application/json"}
REQUEST_TIMEOUT = (10, 180)
PAGE_SLEEP_SECONDS = 0.5
MAX_CONSECUTIVE_FAILURES = 20
SAVE_EVERY_PAGES = 50

# Governance/context endpoints (small, non-paginated-heavy reference data —
# refetched in full each run and upserted by API id, unlike the append-only
# readings stream). "threats" and "policies" mirror the AD-RT expert-rule
# thresholds (RT/rules.py); "assets" are the 5 pilot heritage sites.
GOVERNANCE_ENDPOINTS = ["threats", "policies", "decisions", "assets"]

# Known pilot site slugs, matching RT/realtime_monitor.py SITES and the
# argus:Site individuals minted by add_reading_to_graph().
KNOWN_PILOT_SITES = ["delos", "baltanas", "lucretili", "ranverso", "schenkenberg"]


# ---------------------------------------------------------------------------
# Simple API client (original readings.py functionality)
# ---------------------------------------------------------------------------

def fetch_page(page: int = 1, **params) -> dict:
    response = requests.get(BASE_URL, params={"page": page, **params}, timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_readings_iter(max_pages: Optional[int] = None, **params) -> Iterator[dict]:
    page = 1
    while True:
        data = fetch_page(page, **params)
        yield from data["data"]
        meta = data["meta"]
        if page >= meta["last_page"]:
            break
        if max_pages is not None and page >= max_pages:
            break
        page += 1


# ---------------------------------------------------------------------------
# Robust paginated fetcher (with retry + resume support)
# ---------------------------------------------------------------------------

def _make_session() -> requests.Session:
    retry_strategy = Retry(
        total=5, connect=5, read=5, status=5,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        raise_on_status=False,
    )
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def _fetch_page_robust(session: requests.Session, page: int) -> Dict[str, Any]:
    response = session.get(
        BASE_URL, headers=API_HEADERS,
        params={"page": page}, timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict):
        raise ValueError("Expected paginated API response to be a JSON object.")
    return payload


def _parse_paginated(payload: Dict[str, Any], fallback_page: int) -> Tuple[List[Dict], int, int, Optional[int]]:
    data = payload.get("data", [])
    meta = payload.get("meta", {})
    if not isinstance(data, list):
        data = []
    if not isinstance(meta, dict):
        meta = {}
    current_page = int(meta.get("current_page", fallback_page))
    last_page = int(meta.get("last_page", current_page))
    total = meta.get("total")
    records = [item for item in data if isinstance(item, dict)]
    return records, current_page, last_page, total


def fetch_all_records(session: requests.Session, url: str) -> List[Dict[str, Any]]:
    """Fetch every page of a small paginated endpoint (threats/policies/decisions/assets)."""
    records: List[Dict[str, Any]] = []
    page = 1
    while True:
        response = session.get(url, headers=API_HEADERS, params={"page": page}, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        payload = response.json()
        page_records, current_page, last_page, _ = _parse_paginated(payload, page)
        records.extend(page_records)
        if current_page >= last_page:
            break
        page = current_page + 1
        time.sleep(PAGE_SLEEP_SECONDS)
    return records


def fetch_readings_paginated(
    max_records: Optional[int] = None,
    start_page: int = 1,
) -> Tuple[Iterator[List[Dict[str, Any]]], Dict[str, Any]]:
    """Yields one list of records per page."""
    progress: Dict[str, Any] = {
        "last_successful_page": start_page - 1,
        "last_page": None,
        "total": None,
        "records_downloaded_this_run": 0,
    }

    def _iter_pages() -> Iterator[List[Dict[str, Any]]]:
        print(f"Fetching paginated readings from: {BASE_URL}")
        print(f"Starting from page: {start_page}")

        session = _make_session()
        page = max(1, start_page)
        consecutive_failures = 0
        downloaded = 0

        while True:
            try:
                payload = _fetch_page_robust(session, page)
                records, current_page, last_page_value, total_value = _parse_paginated(payload, page)
                if total_value is not None:
                    progress["total"] = total_value
                progress["last_page"] = last_page_value
                progress["last_successful_page"] = current_page

                downloaded += len(records)
                progress["records_downloaded_this_run"] = downloaded

                print(
                    f"Page {current_page}/{last_page_value} | "
                    f"page records: {len(records)} | "
                    f"downloaded: {downloaded}"
                    + (f" / total: {progress['total']}" if progress["total"] is not None else "")
                )

                yield records

                if max_records is not None and downloaded >= max_records:
                    print(f"Stopped after max_records={max_records}")
                    return
                if current_page >= last_page_value:
                    return

                page = current_page + 1
                consecutive_failures = 0
                time.sleep(PAGE_SLEEP_SECONDS)

            except RequestException as exc:
                consecutive_failures += 1
                wait_seconds = min(300, 10 * consecutive_failures)
                print(
                    f"Failed on page {page}. "
                    f"Consecutive failures: {consecutive_failures}/{MAX_CONSECUTIVE_FAILURES}. "
                    f"Waiting {wait_seconds}s. Error: {repr(exc)}"
                )
                if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                    print("Stopping to avoid hammering the API. Re-run later to resume.")
                    return
                time.sleep(wait_seconds)

    return _iter_pages(), progress


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_text(value: Any, fallback: str = "unknown") -> str:
    if value is None:
        return fallback
    text = str(value).strip()
    return text if text else fallback


def _make_hash(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]


def _make_uri_part(value: Any) -> str:
    text = _safe_text(value)
    allowed = []
    for ch in text:
        if ch.isalnum() or ch in ("-", "_"):
            allowed.append(ch)
        else:
            allowed.append("_")
    return "".join(allowed)[:120]


# ---------------------------------------------------------------------------
# State persistence
# ---------------------------------------------------------------------------

def _load_seen_ids() -> set:
    if not SEEN_IDS_FILE.exists():
        # Migrate from old state file if needed
        if STATE_FILE.exists():
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                old_state = json.load(f)
            ids = set(old_state.get("seen_reading_ids", []))
            if ids:
                print(f"Migrating {len(ids)} seen IDs from state JSON to {SEEN_IDS_FILE}")
                _save_seen_ids(ids)
            return ids
        return set()
    with open(SEEN_IDS_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())


def _save_seen_ids(seen_ids: set) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(SEEN_IDS_FILE, "w", encoding="utf-8") as f:
        for rid in sorted(seen_ids):
            f.write(rid + "\n")


def _append_seen_ids(new_ids: Iterable[str]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(SEEN_IDS_FILE, "a", encoding="utf-8") as f:
        for rid in new_ids:
            f.write(rid + "\n")


def _append_raw_readings(records: List[Tuple[str, Dict[str, Any]]]) -> None:
    # Append-only, so a live run never rewrites what is already on disk.
    if not records:
        return
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(RAW_JSONL_FILE, "a", encoding="utf-8") as f:
        for rid, reading in records:
            f.write(json.dumps({"reading_id": rid, "reading": reading},
                               ensure_ascii=False, default=str) + "\n")


def export_raw_json(g: Graph) -> int:
    # Move rawJson literals out of the graph into the sidecar, so stripping them
    # is lossless. Skips readings already present in the sidecar.
    known = set()
    if RAW_JSONL_FILE.exists():
        with open(RAW_JSONL_FILE, encoding="utf-8") as f:
            for line in f:
                try:
                    known.add(json.loads(line)["reading_id"])
                except (json.JSONDecodeError, KeyError):
                    continue

    records = []
    for subject, raw in g.subject_objects(ARGUS.rawJson):
        rid = str(subject).rsplit("/", 1)[-1]
        if rid in known:
            continue
        try:
            records.append((rid, json.loads(str(raw))))
        except json.JSONDecodeError:
            continue
    _append_raw_readings(records)
    return len(records)


def strip_raw_json(g: Graph) -> int:
    n = sum(1 for _ in g.triples((None, ARGUS.rawJson, None)))
    g.remove((None, ARGUS.rawJson, None))
    return n


def _load_state() -> Dict[str, Any]:
    if not STATE_FILE.exists():
        return {
            "last_update": None,
            "total_seen": 0,
            "last_successful_page": 0,
            "last_page": None,
            "total": None,
            "records_downloaded": 0,
        }
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        state = json.load(f)
    state.pop("seen_reading_ids", None)
    return state


def _save_state(state: Dict[str, Any]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# RDF conversion
# ---------------------------------------------------------------------------

def _bind_namespaces(g: Graph) -> None:
    g.bind("sosa", SOSA)
    g.bind("argus", ARGUS)
    g.bind("ex", EX)
    g.bind("rdfs", RDFS)
    g.bind("xsd", XSD)


def _add_literal(g: Graph, subject: URIRef, predicate: URIRef, value: Any, datatype: Optional[URIRef] = None) -> None:
    if value is None:
        return
    if datatype is not None:
        g.add((subject, predicate, Literal(value, datatype=datatype)))
    else:
        g.add((subject, predicate, Literal(value)))


def reading_stable_id(reading: Dict[str, Any]) -> str:
    key = {
        "ts": reading.get("ts"),
        "site": reading.get("site"),
        "sensor_id": reading.get("sensor_id"),
        "node_id": reading.get("node_id"),
        "topic_id": reading.get("topic_id"),
        "reading_type": reading.get("reading_type"),
        "payload": reading.get("payload"),
    }
    return _make_hash(key)


def _extract_observations(payload: Any) -> Iterable[Dict[str, Any]]:
    if payload is None:
        return []

    observations = []

    if isinstance(payload, dict):
        for key, value in payload.items():
            if isinstance(value, (dict, list)):
                continue
            observations.append({"quantity": key, "value": value, "unit": None})
        return observations

    if isinstance(payload, list):
        for item in payload:
            if not isinstance(item, dict):
                continue
            observations.append({
                "quantity": item.get("n") or item.get("name") or item.get("quantity"),
                "value": item.get("v") or item.get("value"),
                "unit": item.get("u") or item.get("unit"),
            })
        return observations

    return []


def _add_observation_value(g: Graph, obs_uri: URIRef, value: Any) -> None:
    if isinstance(value, bool):
        g.add((obs_uri, SOSA.hasSimpleResult, Literal(value, datatype=XSD.boolean)))
        return
    if isinstance(value, int):
        g.add((obs_uri, SOSA.hasSimpleResult, Literal(value, datatype=XSD.integer)))
        return
    if isinstance(value, float):
        g.add((obs_uri, SOSA.hasSimpleResult, Literal(value, datatype=XSD.decimal)))
        return
    if isinstance(value, str):
        text = value.strip()
        try:
            if "." in text:
                float(text)
                g.add((obs_uri, SOSA.hasSimpleResult, Literal(text, datatype=XSD.decimal)))
                return
            int(text)
            g.add((obs_uri, SOSA.hasSimpleResult, Literal(text, datatype=XSD.integer)))
            return
        except ValueError:
            pass
    g.add((obs_uri, SOSA.hasSimpleResult, Literal(value)))


def add_reading_to_graph(g: Graph, reading: Dict[str, Any]) -> str:
    rid = reading_stable_id(reading)

    site_name = _safe_text(reading.get("site"), "unknown_site")
    sensor_id = _safe_text(reading.get("sensor_id"), "unknown_sensor")
    node_id = _safe_text(reading.get("node_id"), "unknown_node")
    reading_type = _safe_text(reading.get("reading_type"), "unknown_reading_type")

    reading_uri = EX[f"reading/{rid}"]
    site_uri = EX[f"site/{_make_uri_part(site_name)}"]
    sensor_uri = EX[f"sensor/{_make_uri_part(sensor_id)}"]
    node_uri = EX[f"node/{_make_uri_part(node_id)}"]

    # Reading as observation collection
    g.add((reading_uri, RDF.type, SOSA.ObservationCollection))
    g.add((reading_uri, ARGUS.hasSite, site_uri))
    g.add((reading_uri, SOSA.madeBySensor, sensor_uri))
    g.add((reading_uri, ARGUS.hasNode, node_uri))
    _add_literal(g, reading_uri, ARGUS.readingType, reading_type)

    ts = reading.get("ts")
    if ts is not None:
        _add_literal(g, reading_uri, SOSA.resultTime, ts, XSD.dateTime)

    _add_literal(g, reading_uri, ARGUS.topic, reading.get("topic"))
    _add_literal(g, reading_uri, ARGUS.topicId, reading.get("topic_id"))
    _add_literal(g, reading_uri, ARGUS.deviceGroupId, reading.get("device_group_id"))

    # Site
    g.add((site_uri, RDF.type, ARGUS.Site))
    g.add((site_uri, RDFS.label, Literal(site_name)))

    # Sensor — prefer sensor_name, fall back to node_label/node_name, last resort UUID
    sensor_label = (reading.get("sensor_name")
                    or reading.get("node_label")
                    or reading.get("node_name")
                    or sensor_id)
    g.add((sensor_uri, RDF.type, SOSA.Sensor))
    g.add((sensor_uri, RDFS.label, Literal(_safe_text(sensor_label))))
    _add_literal(g, sensor_uri, ARGUS.sensorId, sensor_id)
    _add_literal(g, sensor_uri, ARGUS.sensorModel, reading.get("sensor_model"))

    # Node
    node_label = reading.get("node_label") or reading.get("node_name") or node_id
    g.add((node_uri, RDF.type, ARGUS.Node))
    g.add((node_uri, RDFS.label, Literal(_safe_text(node_label))))
    _add_literal(g, node_uri, ARGUS.nodeId, node_id)
    _add_literal(g, node_uri, ARGUS.nodeName, reading.get("node_name"))
    _add_literal(g, node_uri, ARGUS.nodeModel, reading.get("node_model"))
    _add_node_coords(g, node_uri, node_id)

    # Engineering unit
    eng_unit_id = reading.get("eng_unit_id")
    eng_unit_name = reading.get("eng_unit_name") or reading.get("eng_unit_custom")

    if eng_unit_id is not None or eng_unit_name is not None:
        unit_key = eng_unit_id if eng_unit_id is not None else eng_unit_name
        unit_uri = EX[f"engineering-unit/{_make_uri_part(unit_key)}"]
        g.add((unit_uri, RDF.type, ARGUS.EngineeringUnit))
        g.add((reading_uri, ARGUS.hasEngineeringUnit, unit_uri))
        if eng_unit_name is not None:
            g.add((unit_uri, RDFS.label, Literal(_safe_text(eng_unit_name))))
        _add_literal(g, unit_uri, ARGUS.engineeringUnitId, eng_unit_id)
        _add_literal(g, unit_uri, ARGUS.engineeringUnitCustom, reading.get("eng_unit_custom"))

    # Payload observations
    payload = reading.get("payload")
    for index, obs in enumerate(_extract_observations(payload)):
        quantity = obs.get("quantity")
        value = obs.get("value")
        unit = obs.get("unit")
        if quantity is None or value is None:
            continue

        q_label = _safe_text(quantity)
        obs_hash = _make_hash({
            "reading_id": rid, "index": index,
            "quantity": q_label, "value": value, "unit": unit,
        })

        obs_uri = EX[f"observation/{obs_hash}"]
        quantity_uri = EX[f"quantity/{_make_uri_part(q_label)}"]

        g.add((obs_uri, RDF.type, SOSA.Observation))
        g.add((reading_uri, ARGUS.hasObservation, obs_uri))
        g.add((obs_uri, SOSA.observedProperty, quantity_uri))
        g.add((quantity_uri, RDF.type, ARGUS.ObservedProperty))
        g.add((quantity_uri, RDFS.label, Literal(q_label)))

        _add_observation_value(g, obs_uri, value)

        if ts is not None:
            _add_literal(g, obs_uri, SOSA.resultTime, ts, XSD.dateTime)
        if unit is not None:
            _add_literal(g, obs_uri, ARGUS.unit, unit)

    if KEEP_RAW_JSON_IN_GRAPH:
        g.add((reading_uri, ARGUS.rawJson,
               Literal(json.dumps(reading, ensure_ascii=False, default=str))))
    return rid


# ---------------------------------------------------------------------------
# Governance data (threats / policies / decisions / assets)
# ---------------------------------------------------------------------------

def _parse_metadata(record: Dict[str, Any]) -> Dict[str, Any]:
    raw = record.get("metadata")
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str) and raw.strip():
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {}
    return {}


def _match_pilot_site(*texts: Optional[str]) -> Optional[str]:
    """Find a known pilot slug (delos, baltanas, ...) mentioned in any of the given texts."""
    haystack = " ".join(_safe_text(t, "") for t in texts).lower()
    for slug in KNOWN_PILOT_SITES:
        if slug in haystack:
            return slug
    return None


def _remove_subject(g: Graph, subject: URIRef) -> None:
    # Governance records are mutable reference data (thresholds can change),
    # so re-ingesting is an upsert by API id, not append-only like readings.
    g.remove((subject, None, None))


def add_threat_to_graph(g: Graph, record: Dict[str, Any]) -> URIRef:
    uri = EX[f"threat/{record['id']}"]
    _remove_subject(g, uri)
    md = _parse_metadata(record)

    g.add((uri, RDF.type, PANOPTES.Threat))
    g.add((uri, RDFS.label, Literal(_safe_text(record.get("name")))))
    _add_literal(g, uri, ARGUS.threatDescription, record.get("description"))
    _add_literal(g, uri, ARGUS.threatLevel, md.get("level"))
    return uri


def add_policy_to_graph(g: Graph, record: Dict[str, Any]) -> URIRef:
    uri = EX[f"policy/{record['id']}"]
    _remove_subject(g, uri)
    md = _parse_metadata(record)

    g.add((uri, RDF.type, PANOPTES.Policy))
    g.add((uri, RDFS.label, Literal(_safe_text(record.get("name")))))
    _add_literal(g, uri, ARGUS.policyDescription, record.get("description"))
    _add_literal(g, uri, ARGUS.ruleId, md.get("rule"))
    _add_literal(g, uri, ARGUS.threatName, md.get("threat_name"))

    thresholds = md.get("threshold_overrides")
    if isinstance(thresholds, dict) and thresholds:
        if len(thresholds) == 1:
            (_, value), = thresholds.items()
            if isinstance(value, (int, float)):
                _add_literal(g, uri, ARGUS.thresholdValue, value, XSD.decimal)
        _add_literal(g, uri, ARGUS.thresholdJson,
                     json.dumps(thresholds, ensure_ascii=False, sort_keys=True))

    pilot = md.get("pilot") or _match_pilot_site(record.get("name"), record.get("description"))
    if pilot:
        g.add((uri, ARGUS.appliesToSite, EX[f"site/{_make_uri_part(pilot)}"]))
    return uri


def add_decision_to_graph(g: Graph, record: Dict[str, Any]) -> URIRef:
    uri = EX[f"decision/{record['id']}"]
    _remove_subject(g, uri)
    md = _parse_metadata(record)

    g.add((uri, RDF.type, PANOPTES.Decision))
    g.add((uri, RDFS.label, Literal(_safe_text(record.get("name")))))
    _add_literal(g, uri, ARGUS.decisionDescription, record.get("description") or md.get("recommendation"))
    _add_literal(g, uri, ARGUS.urgency, md.get("urgency"))
    return uri


def add_asset_to_graph(g: Graph, record: Dict[str, Any]) -> URIRef:
    uri = EX[f"asset/{record['id']}"]
    _remove_subject(g, uri)
    md = _parse_metadata(record)

    g.add((uri, RDF.type, PANOPTES.Asset))
    g.add((uri, RDFS.label, Literal(_safe_text(record.get("name")))))
    _add_literal(g, uri, ARGUS.assetDescription, record.get("description"))
    _add_literal(g, uri, ARGUS.assetCode, md.get("code"))
    _add_literal(g, uri, ARGUS.pilotNumber, md.get("pilot_number"), XSD.integer)
    _add_literal(g, uri, ARGUS.sourceUrl, md.get("source_url"))
    _add_literal(g, uri, ARGUS.country, md.get("country"))

    pilot = _match_pilot_site(md.get("code"), record.get("name"))
    if pilot:
        g.add((uri, ARGUS.atSite, EX[f"site/{_make_uri_part(pilot)}"]))
    return uri


_GOVERNANCE_ADDERS = {
    "threats": add_threat_to_graph,
    "policies": add_policy_to_graph,
    "decisions": add_decision_to_graph,
    "assets": add_asset_to_graph,
}


def ingest_governance(g: Graph, session: Optional[requests.Session] = None) -> Dict[str, int]:
    """Fetch threats/policies/decisions/assets and upsert them into the graph."""
    session = session or _make_session()
    counts: Dict[str, int] = {}
    for endpoint in GOVERNANCE_ENDPOINTS:
        url = f"{API_ROOT}/{endpoint}"
        records = fetch_all_records(session, url)
        adder = _GOVERNANCE_ADDERS[endpoint]
        for record in records:
            adder(g, record)
        counts[endpoint] = len(records)
        print(f"Governance: {endpoint} -> {len(records)} record(s)")
    return counts


# ---------------------------------------------------------------------------
# Graph I/O
# ---------------------------------------------------------------------------

def enrich_existing_nodes(g: Graph) -> int:
    # Attach coordinates to Node instances already in the graph, matched by
    # nodeId. Idempotent: replaces any existing coord triples. Returns #nodes hit.
    hit = 0
    for node_uri, nid_lit in g.subject_objects(ARGUS.nodeId):
        coords = _load_node_coords().get(str(nid_lit))
        if not coords:
            continue
        for pred in (ARGUS.latitude, ARGUS.longitude, ARGUS.altitude):
            g.remove((node_uri, pred, None))
        _add_node_coords(g, node_uri, str(nid_lit))
        hit += 1
    return hit


def load_graph() -> Graph:
    g = Graph()
    _bind_namespaces(g)
    if TTL_FILE.exists():
        print(f"Loading existing TTL: {TTL_FILE}")
        g.parse(str(TTL_FILE), format="turtle")
        print(f"Existing triples: {len(g)}")
    else:
        print("No existing TTL found. Creating new graph.")
    return g


def save_graph(g: Graph) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if TTL_FILE.exists():
        print(f"Creating backup: {BACKUP_FILE}")
        BACKUP_FILE.write_text(TTL_FILE.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"Saving TTL: {TTL_FILE}")
    g.serialize(destination=str(TTL_FILE), format="turtle")
    print(f"Saved triples: {len(g)}")


# ---------------------------------------------------------------------------
# Main update procedure
# ---------------------------------------------------------------------------

def update_kg(
    max_records: Optional[int] = None,
    start_page: int = 1,
    resume: bool = False,
    overlap_pages: int = 2,
    skip_governance: bool = False,
) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    state = _load_state()
    seen_ids = _load_seen_ids()

    if resume:
        previous_last = int(state.get("last_successful_page") or 0)
        start_page = max(1, previous_last - overlap_pages + 1)
        print(
            f"Resume mode. Previous last page: {previous_last}. "
            f"Overlap: {overlap_pages}. Starting from page: {start_page}."
        )

    g = load_graph()
    pages_iter, progress = fetch_readings_paginated(
        max_records=max_records,
        start_page=start_page,
    )

    added = 0
    skipped = 0
    pages_since_save = 0
    records_downloaded_before = int(state.get("records_downloaded") or 0)

    def _checkpoint() -> None:
        nonlocal pages_since_save
        state["last_update"] = _now_utc_iso()
        state["total_seen"] = len(seen_ids)
        state["last_successful_page"] = max(
            int(state.get("last_successful_page") or 0),
            int(progress.get("last_successful_page") or 0),
        )
        state["last_page"] = progress.get("last_page")
        state["total"] = progress.get("total")
        state["records_downloaded"] = records_downloaded_before + added + skipped
        save_graph(g)
        _save_state(state)
        pages_since_save = 0
        print(f"  [checkpoint] saved {len(g)} triples, {len(seen_ids)} seen IDs")

    for page_records in pages_iter:
        new_ids = []
        new_raw = []
        for reading in page_records:
            rid = reading_stable_id(reading)
            if rid in seen_ids:
                skipped += 1
                continue
            add_reading_to_graph(g, reading)
            seen_ids.add(rid)
            new_ids.append(rid)
            new_raw.append((rid, reading))
            added += 1

        if new_ids:
            _append_seen_ids(new_ids)
            _append_raw_readings(new_raw)

        pages_since_save += 1
        if pages_since_save >= SAVE_EVERY_PAGES:
            _checkpoint()

    # Coordinates are static per-node metadata, so refresh them for every node in
    # the graph — not just nodes touched by newly ingested readings. Without this,
    # a re-run whose readings are all duplicates would never pick up CSV edits.
    enriched = enrich_existing_nodes(g)
    print(f"Node coordinates refreshed from CSV: {enriched} node(s)")

    if not skip_governance:
        ingest_governance(g)

    _checkpoint()

    print()
    print("Update complete.")
    print(f"Fetched this run: {added + skipped}")
    print(f"Added new: {added}")
    print(f"Skipped duplicates: {skipped}")
    print(f"Total seen: {len(seen_ids)}")
    print(f"Last successful page: {state['last_successful_page']}")
    print(f"API last page: {state['last_page']}")
    print(f"API total records: {state['total']}")
    print(f"TTL file: {TTL_FILE}")
    print(f"State file: {STATE_FILE}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch ARGUS sensor readings and build an RDF knowledge graph."
    )
    parser.add_argument("--max-records", type=int, default=None,
                        help="Max number of API readings to process.")
    parser.add_argument("--start-page", type=int, default=1,
                        help="API page to start from (default: 1).")
    parser.add_argument("--resume", action="store_true",
                        help="Resume near the previous last successful page.")
    parser.add_argument("--overlap-pages", type=int, default=2,
                        help="Pages to re-fetch when resuming (default: 2).")
    parser.add_argument("--enrich-geo-only", action="store_true",
                        help="Attach node coordinates from material/ARGUS_nodes.csv "
                             "to the existing TTL and exit (no API fetch).")
    parser.add_argument("--strip-raw-json", action="store_true",
                        help="Remove argus:rawJson literals from the existing TTL "
                             "and exit. Raw payloads stay available in the JSONL sidecar.")
    parser.add_argument("--governance-only", action="store_true",
                        help="Fetch/upsert threats, policies, decisions and assets "
                             "into the existing TTL and exit (no readings fetch).")
    parser.add_argument("--skip-governance", action="store_true",
                        help="Skip fetching threats/policies/decisions/assets during "
                             "a normal readings update.")
    args = parser.parse_args()

    if args.governance_only:
        g = load_graph()
        counts = ingest_governance(g)
        save_graph(g)
        print(f"Governance upsert complete: {counts}")
        return

    if args.strip_raw_json:
        g = load_graph()
        before = len(g)
        exported = export_raw_json(g)
        removed = strip_raw_json(g)
        save_graph(g)
        print(f"Exported {exported} raw reading(s) to {RAW_JSONL_FILE}")
        print(f"Removed {removed} rawJson triple(s): {before} → {len(g)} triples.")
        return

    if args.enrich_geo_only:
        g = load_graph()
        n = enrich_existing_nodes(g)
        save_graph(g)
        print(f"Enriched {n} node(s) with coordinates from {NODES_CSV}")
        return

    update_kg(
        max_records=args.max_records,
        start_page=args.start_page,
        resume=args.resume,
        overlap_pages=args.overlap_pages,
        skip_governance=args.skip_governance,
    )


if __name__ == "__main__":
    main()
