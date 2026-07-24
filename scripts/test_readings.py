"""
Inspect raw ARGUS readings before they become ontology triples: the API JSON,
the (quantity, value, unit) tuples extracted from the payload, what gets
dropped, and optionally the RDF each reading turns into. Reuses the real
0_readings functions so the output matches actual ingestion.

Reads offline from the argus:rawJson literals in the TTL by default.

    python scripts/test_readings.py                    # 3 samples
    python scripts/test_readings.py --limit 10 --show-triples
    python scripts/test_readings.py --stats-only --limit 500
    python scripts/test_readings.py --source api --limit 5
"""

from __future__ import annotations
import argparse
import importlib
import json
from collections import Counter
from typing import Any, Dict, Iterator, List

from rdflib import Graph

_rd = importlib.import_module("0_readings")
from ontology_schema import ARGUS  # noqa: E402


def _load_from_ttl(limit: int | None) -> Iterator[Dict[str, Any]]:
    ttl = _rd.TTL_FILE
    if not ttl.exists():
        raise SystemExit(f"TTL not found: {ttl}. Run 0_readings.py first, or use --source api.")
    g = Graph()
    g.parse(str(ttl), format="turtle")
    n = 0
    for _, _, raw in g.triples((None, ARGUS.rawJson, None)):
        try:
            yield json.loads(str(raw))
        except json.JSONDecodeError:
            continue
        n += 1
        if limit is not None and n >= limit:
            return


def _load_from_api(limit: int | None) -> Iterator[Dict[str, Any]]:
    n = 0
    for reading in _rd.fetch_readings_iter():
        yield reading
        n += 1
        if limit is not None and n >= limit:
            return


def _payload_shape(payload: Any) -> str:
    if payload is None:
        return "none"
    if isinstance(payload, list):
        return f"list[{len(payload)}]"
    if isinstance(payload, dict):
        return f"dict[{len(payload)} keys]"
    return type(payload).__name__


def _value_kind(value: Any) -> str:
    # Mirror the branch _add_observation_value would take.
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        text = value.strip()
        try:
            if "." in text:
                float(text); return "str→decimal"
            int(text); return "str→integer"
        except ValueError:
            return "str→literal"
    return type(value).__name__


def inspect_reading(reading: Dict[str, Any], show_triples: bool) -> None:
    rid = _rd.reading_stable_id(reading)
    payload = reading.get("payload")
    print("=" * 78)
    print(f"reading id : {rid}")
    print(f"ts         : {reading.get('ts')}")
    print(f"site       : {reading.get('site')}")
    print(f"sensor_id  : {reading.get('sensor_id')}   node: {reading.get('node_name')!r}")
    print(f"reading_type: {reading.get('reading_type')}")
    print(f"payload     : {_payload_shape(payload)}")

    top_fields = {k: v for k, v in reading.items() if not isinstance(v, (dict, list))}
    print("\nscalar fields:")
    for k, v in top_fields.items():
        sv = str(v)
        print(f"  {k:20} = {sv[:80]}")

    obs = list(_rd._extract_observations(payload))
    kept = [o for o in obs if o.get("quantity") is not None and o.get("value") is not None]
    dropped = [o for o in obs if o not in kept]
    print(f"\nextracted observations: {len(obs)}  (kept {len(kept)}, dropped {len(dropped)})")
    print(f"  {'quantity':22} {'value':>16}  {'unit':8} {'-> RDF value kind'}")
    for o in obs:
        flag = "" if (o.get("quantity") is not None and o.get("value") is not None) else "  [DROPPED]"
        q = str(o.get("quantity"))
        val = str(o.get("value"))
        unit = str(o.get("unit"))
        print(f"  {q:22} {val[:16]:>16}  {unit[:8]:8} {_value_kind(o.get('value'))}{flag}")

    if show_triples:
        g = Graph()
        _rd._bind_namespaces(g)
        _rd.add_reading_to_graph(g, reading)
        # Drop the giant rawJson triple from the preview for readability.
        g.remove((None, ARGUS.rawJson, None))
        print(f"\nRDF triples generated: {len(g) + 1} (rawJson omitted from preview)")
        print(g.serialize(format="turtle"))


def summarize(readings: List[Dict[str, Any]]) -> None:
    payload_shapes = Counter()
    quantities = Counter()
    value_kinds = Counter()
    missing = Counter()
    obs_per_reading = []
    dropped_total = 0

    scalar_field_freq = Counter()
    for r in readings:
        payload_shapes[_payload_shape(r.get("payload"))] += 1
        for k, v in r.items():
            if not isinstance(v, (dict, list)):
                scalar_field_freq[k] += 1
        for key in ("ts", "site", "sensor_id", "node_id", "reading_type"):
            if r.get(key) in (None, "", "null"):
                missing[key] += 1
        obs = list(_rd._extract_observations(r.get("payload")))
        obs_per_reading.append(len(obs))
        for o in obs:
            if o.get("quantity") is None or o.get("value") is None:
                dropped_total += 1
                continue
            quantities[str(o.get("quantity"))] += 1
            value_kinds[_value_kind(o.get("value"))] += 1

    print("=" * 78)
    print(f"SUMMARY over {len(readings)} readings")
    print("=" * 78)
    print("\npayload shapes:")
    for shape, c in payload_shapes.most_common():
        print(f"  {shape:18} {c}")

    if obs_per_reading:
        print(f"\nobservations per reading: min {min(obs_per_reading)}, "
              f"max {max(obs_per_reading)}, avg {sum(obs_per_reading)/len(obs_per_reading):.1f}")
    print(f"observations dropped (quantity/value None): {dropped_total}")

    print("\nvalue kinds (-> how hasSimpleResult gets typed):")
    for k, c in value_kinds.most_common():
        print(f"  {k:16} {c}")

    print(f"\ndistinct quantities: {len(quantities)}")
    for q, c in quantities.most_common(30):
        print(f"  {q:24} {c}")
    if len(quantities) > 30:
        print(f"  … and {len(quantities) - 30} more")

    if missing:
        print("\nMISSING key fields (may hurt joins/labels):")
        for k, c in missing.most_common():
            print(f"  {k:16} {c}")

    print("\nscalar field coverage:")
    for k, c in scalar_field_freq.most_common():
        print(f"  {k:24} {c}/{len(readings)}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Inspect raw ARGUS readings before ontology conversion.")
    ap.add_argument("--source", choices=["ttl", "api"], default="ttl",
                    help="Where to read raw readings from (default: ttl, offline).")
    ap.add_argument("--limit", type=int, default=3, help="Number of readings to load.")
    ap.add_argument("--reading-id", type=str, default=None,
                    help="Inspect only the reading whose stable id matches (scans up to --limit).")
    ap.add_argument("--show-triples", action="store_true", help="Also print the RDF each reading becomes.")
    ap.add_argument("--stats-only", action="store_true", help="Print only the aggregate summary.")
    args = ap.parse_args()

    loader = _load_from_ttl if args.source == "ttl" else _load_from_api
    # For stats we usually want a larger sample; for id-search we must scan.
    load_limit = args.limit
    readings = list(loader(load_limit))

    if not readings:
        raise SystemExit("No readings loaded.")

    if args.reading_id:
        match = next((r for r in readings if _rd.reading_stable_id(r) == args.reading_id), None)
        if match is None:
            raise SystemExit(f"reading id {args.reading_id} not found in first {load_limit} readings.")
        inspect_reading(match, args.show_triples)
        return

    if args.stats_only:
        summarize(readings)
        return

    for r in readings:
        inspect_reading(r, args.show_triples)
    print()
    summarize(readings)


if __name__ == "__main__":
    main()
