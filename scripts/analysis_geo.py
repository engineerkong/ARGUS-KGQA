"""
Pre-computed analysis of a result set, so the answer LLM never does the maths:
spatial metrics when rows carry node coordinates and per-quantity numeric
stats, here; temporal facts (recency, span) from analysis_temp.py.
analyze() assembles all three. Sections are emitted only when the data
supports them.
"""

from __future__ import annotations
import re
from datetime import datetime, timezone
from math import radians, sin, cos, asin, sqrt
from typing import Any

from analysis_temp import temporal_facts

_MAX_RECENCY_ROWS = 20
_EARTH_RADIUS_M = 6_371_000.0


# ── Row labels ───────────────────────────────────────────────────────────────

def _row_label(row: dict) -> str:
    for key in ("Site_label", "site_label", "label", "node_label", "Node_label",
                "Sensor_label", "sensor_label", "name", "ObservedProperty_label"):
        v = row.get(key)
        if v and not str(v).startswith("http"):
            return str(v)[:50]
    for v in row.values():
        if isinstance(v, str) and not v.startswith("http") and len(v) < 60:
            return v[:50]
    return str(list(row.values())[0])[:50] if row else "?"


# ── Space ────────────────────────────────────────────────────────────────────

def _haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    p1, p2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlam = radians(lon2 - lon1)
    a = sin(dphi / 2) ** 2 + cos(p1) * cos(p2) * sin(dlam / 2) ** 2
    return 2 * _EARTH_RADIUS_M * asin(sqrt(a))


def _find_key(row: dict, needle: str) -> Any:
    for k, v in row.items():
        if needle in k.lower() and v is not None:
            return v
    return None


_MAX_DISTANCE_TABLE = 25  # per-node distance lists only for result sets up to this many nodes


def _point_label(row: dict) -> str:
    # A located row is a node: prefer its own label over a joined site label.
    for key in ("label", "node_label", "Node_label", "name"):
        v = row.get(key)
        if v and not str(v).startswith("http"):
            return str(v)[:50]
    return _row_label(row)


def _extract_points(results: list[dict]) -> list[dict]:
    # One point per distinct (label, lat, lon) — co-located nodes stay separate
    # nodes; altitude and site optional.
    seen = set()
    points = []
    for row in results:
        lat, lon = _find_key(row, "latitude"), _find_key(row, "longitude")
        if lat is None or lon is None:
            continue
        try:
            lat_f, lon_f = float(lat), float(lon)
        except (ValueError, TypeError):
            continue
        alt = _find_key(row, "altitude")
        try:
            alt_f = float(alt) if alt is not None else None
        except (ValueError, TypeError):
            alt_f = None
        label = _point_label(row)
        key = (label, lat_f, lon_f)
        if key in seen:
            continue
        seen.add(key)
        site = _find_key(row, "site_label")
        points.append({"label": label, "lat": lat_f, "lon": lon_f, "alt": alt_f,
                       "site": str(site) if site is not None else None})
    return points


def _spatial_lines(points: list[dict]) -> list[str]:
    n = len(points)
    lines = [f"\n=== Spatial ({n} located node{'s' if n != 1 else ''}) ==="]
    lats = [p["lat"] for p in points]
    lons = [p["lon"] for p in points]
    lines.append(f"  centroid: {sum(lats)/n:.6f}, {sum(lons)/n:.6f}")
    lines.append(f"  bounding box: lat [{min(lats):.6f}, {max(lats):.6f}], "
                 f"lon [{min(lons):.6f}, {max(lons):.6f}]")

    alts = [p["alt"] for p in points if p["alt"] is not None]
    if alts:
        lines.append(f"  altitude: min {min(alts):.2f} m, max {max(alts):.2f} m "
                     f"(spread {max(alts) - min(alts):.2f} m)")

    if n >= 2:
        far = (-1.0, None, None)
        near = (float("inf"), None, None)
        for i in range(n):
            for j in range(i + 1, n):
                d = _haversine_m(points[i]["lat"], points[i]["lon"],
                                 points[j]["lat"], points[j]["lon"])
                if d > far[0]:
                    far = (d, points[i]["label"], points[j]["label"])
                if d < near[0]:
                    near = (d, points[i]["label"], points[j]["label"])
        lines.append(f"  max separation: {far[0]:.1f} m between {far[1]} and {far[2]}")
        lines.append(f"  closest pair: {near[0]:.1f} m between {near[1]} and {near[2]}")

    # Distances from every node to every other one, nearest first — what
    # "closest to X", "within R m of X" and "distance between A and B" need.
    if 2 <= n <= _MAX_DISTANCE_TABLE:
        lines.append("  distances from each node (m), nearest first:")
        for p in points:
            others = sorted((_haversine_m(p["lat"], p["lon"], q["lat"], q["lon"]), q["label"])
                            for q in points if q is not p)
            lines.append(f"    {p['label']}: " + ", ".join(f"{lbl} {d:.1f}" for d, lbl in others))

    # Several sites in one result: a centroid per site and the distances between them.
    sites = sorted({p["site"] for p in points if p["site"]})
    if len(sites) >= 2:
        cents = {}
        lines.append("  per-site centroids:")
        for st in sites:
            ps = [p for p in points if p["site"] == st]
            cents[st] = (sum(p["lat"] for p in ps) / len(ps), sum(p["lon"] for p in ps) / len(ps))
            lines.append(f"    {st}: {cents[st][0]:.6f}, {cents[st][1]:.6f} ({len(ps)} nodes)")
        lines.append("  distances between site centroids:")
        for i, a in enumerate(sites):
            for b in sites[i + 1:]:
                d = _haversine_m(*cents[a], *cents[b])
                lines.append(f"    {a} – {b}: {d / 1000:.1f} km")

    lines.append("  points (label: lat, lon, alt):")
    for p in points[:_MAX_RECENCY_ROWS]:
        alt = f", {p['alt']:.1f} m" if p["alt"] is not None else ""
        lines.append(f"    {p['label']:20s} {p['lat']:.6f}, {p['lon']:.6f}{alt}")
    if n > _MAX_RECENCY_ROWS:
        lines.append(f"    … and {n - _MAX_RECENCY_ROWS} more")
    return lines


# ── Facts for the question at hand ───────────────────────────────────────────
# The spatial section lists every distance; which one answers the question is
# picked here, deterministically, from the nodes, sites and radius it names —
# so neither the template answer nor the LLM has to search a distance table.

_RADIUS = re.compile(r"within\s+(\d+(?:\.\d+)?)\s*(km|kilomet(?:er|re)s?|m|met(?:er|re)s?)\b", re.I)


def _tok(s: str) -> str:
    return " " + " ".join(re.findall(r"[a-z0-9]+", str(s).lower())) + " "


def _named(label: str, q: str) -> bool:
    forms = [_tok(label)]
    m = re.match(r"(LS-\d+)", label, re.I)       # "LS-152608 - Tiltmeter Conventillo"
    if m:
        forms.append(_tok(m.group(1)))
    return any(f.strip() and f in q for f in forms)


def _site_centroids(points: list[dict]) -> dict[str, tuple[float, float, int]]:
    out = {}
    for st in sorted({p["site"] for p in points if p["site"]}):
        ps = [p for p in points if p["site"] == st]
        out[st] = (sum(p["lat"] for p in ps) / len(ps), sum(p["lon"] for p in ps) / len(ps), len(ps))
    return out


def _focus_lines(query: str, points: list[dict]) -> list[str]:
    q = _tok(query)
    labels = list(dict.fromkeys(p["label"] for p in points))
    # A label that contains another named label ("AF1" in "AF10") is not a second mention.
    named = [l for l in labels if _named(l, q)]
    named = [l for l in named if not any(l != o and _tok(l) in _tok(o) for o in named)]
    dist = lambda a, b: _haversine_m(a["lat"], a["lon"], b["lat"], b["lon"])
    out = []
    if len(named) == 2:
        a = [p for p in points if p["label"] == named[0]]
        b = [p for p in points if p["label"] == named[1]]
        d = min(dist(x, y) for x in a for y in b)
        out.append(f"  distance between {named[0]} and {named[1]}: {d:.1f} m")
    elif len(named) == 1:
        xs = [p for p in points if p["label"] == named[0]]
        others = sorted((min(dist(x, o) for x in xs), o["label"]) for o in points if o["label"] != named[0])
        m = _RADIUS.search(query)
        if m and others:
            r = float(m.group(1)) * (1000 if m.group(2).lower().startswith("k") else 1)
            inside = [(d, l) for d, l in others if d <= r]
            out.append(f"  other nodes within {m.group(1)} {m.group(2)} of {named[0]}: {len(inside)}"
                       + (" (" + ", ".join(f"{l} {d:.1f} m" for d, l in inside) + ")" if inside else ""))
        elif others:
            out.append(f"  node nearest to {named[0]}: {others[0][1]}, {others[0][0]:.1f} m away")
    else:
        cents = _site_centroids(points)
        if len(cents) >= 2 and re.search(r"far apart|distance|between|centroid", query, re.I):
            sites = list(cents)
            for i, a in enumerate(sites):
                for b in sites[i + 1:]:
                    d = _haversine_m(cents[a][0], cents[a][1], cents[b][0], cents[b][1])
                    out.append(f"  distance between the centroids of {a} and {b}: {d / 1000:.1f} km")
        elif re.search(r"centroid|cent(?:er|re) of", query, re.I) and points:
            n = len(points)
            out.append(f"  centroid of the {n} located nodes: latitude {sum(p['lat'] for p in points) / n:.6f}, "
                       f"longitude {sum(p['lon'] for p in points) / n:.6f}")
        elif len(points) >= 2 and re.search(r"most distant|farthest|furthest|far apart|maximum distance", query, re.I):
            d, a, b = max((dist(x, y), x["label"], y["label"])
                          for i, x in enumerate(points) for y in points[i + 1:])
            out.append(f"  largest distance between two nodes: {d:.1f} m, between {a} and {b}")
        elif len(points) >= 2 and re.search(r"closest (?:two|pair)|two closest|nearest (?:two|pair)", query, re.I):
            d, a, b = min((dist(x, y), x["label"], y["label"])
                          for i, x in enumerate(points) for y in points[i + 1:])
            out.append(f"  smallest distance between two nodes: {d:.1f} m, between {a} and {b}")
        elif re.search(r"altitude range|elevation range|range of (?:the )?altitude", query, re.I):
            alts = [p["alt"] for p in points if p["alt"] is not None]
            if alts:
                out.append(f"  altitude range: {max(alts) - min(alts):.2f} m (from {min(alts):.2f} m to {max(alts):.2f} m)")
    return out


# ── Numeric (grouped by measured property so ranges stay meaningful) ─────────

def _numeric_lines(results: list[dict]) -> list[str]:
    value_key = next((k for row in results for k in row
                      if "hassimpleresult" in k.lower()), None)
    if not value_key:
        return []
    series_key = next((k for row in results for k in row
                       if "observedproperty" in k.lower() or k.lower().endswith("_label")
                       and "site" not in k.lower()), None)

    groups: dict[str, list[float]] = {}
    for row in results:
        v = row.get(value_key)
        if v is None:
            continue
        try:
            fv = float(v)
        except (ValueError, TypeError):
            continue
        series = str(row.get(series_key)) if series_key else "value"
        groups.setdefault(series, []).append(fv)

    if not groups:
        return []
    lines = ["\n=== Numeric summary (grouped so ranges are per measured quantity) ==="]
    for series, vals in sorted(groups.items()):
        lines.append(f"  {series:24s} count {len(vals)}, min {min(vals):.4f}, "
                     f"max {max(vals):.4f}, avg {sum(vals)/len(vals):.4f}")
    return lines


# ── What the parser and the answer generator are told about this layer ───────
# Imported into the parser prompt and the answer prompt, so the LLM is told to
# return coordinates exactly because this module computes everything from them.

PARSER_SCHEMA = """\
Node geo-location (datatype properties on Node; populated for the nodes of all five heritage sites):
  Node.latitude    (decimal degrees, WGS84)
  Node.longitude   (decimal degrees, WGS84)
  Node.altitude    (metres)
  For location/distance/elevation questions, return these Node properties. Distances,
  nearest/farthest pairs, centroid and spread are computed downstream from the
  coordinates — you only need to RETURN latitude/longitude/altitude, not compute them."""

PARSER_GUIDE = """\
  - Counting or picking nodes BY DISTANCE ("how many nodes are within R m of X", "which node is closest to X") is a spatial question, not an aggregation: set aggregation to null and return the coordinates of all nodes of that site — the count or the nearest node is computed downstream from the distances. An aggregation here would count the site's nodes without any distance.
  - Distances: between two named nodes, target Node with label "in" [both names]; nearest node / nodes within R m of a node, return all nodes of that site; between sites, target Node joined to Site with label "in" [the sites] and return Site.label. Always return the coordinates — the distances from each node, and per-site centroids, are computed downstream.
  - Location/where/distance/nearest/elevation questions: set target_class=Node and return_properties=["label","latitude","longitude","altitude"]; link to a Site by joining ObservationCollection via hasNode (incoming) then Site via hasSite (outgoing, filtered). Do NOT try to compute distances/centroids in the query — just return the coordinates; the analysis layer computes spatial metrics."""

PARSER_EXAMPLES = """\
Q: "Where are the sensor nodes at the baltanas site?"
{
  "target_class": "Node",
  "filters": [],
  "return_properties": ["label", "latitude", "longitude", "altitude"],
  "joins": [
    {"class": "ObservationCollection", "via": "hasNode", "direction": "incoming",
     "return_properties": [], "filters": []},
    {"class": "Site", "via": "hasSite", "direction": "outgoing",
     "return_properties": [], "filters": [{"property": "label", "op": "equals", "value": "baltanas"}]}
  ],
  "aggregation": null,
  "order_by": null,
  "limit": null,
  "anomaly_check": false,
  "as_of": null,
  "explanation": "List baltanas nodes with their coordinates; spatial metrics are derived downstream from lat/long/altitude."
}"""

ANSWER_GUIDE = """\
Numbers and facts:
- If the analysis has a section "Facts for this question", it was computed for exactly what was asked (a named pair's distance, the node nearest to a named node, the nodes within a radius, the distance between site centroids) — answer from it.
- Report numbers as the results/analysis give them, in the same unit (do not convert m to km or back) and with at least the decimals shown in the analysis (distances to 0.1 m or 0.1 km)."""


# ── Entry point ──────────────────────────────────────────────────────────────

def analyze(results: list[dict[str, Any]], now: datetime | None = None,
            query: str | None = None) -> dict[str, Any]:
    """`now` is the reference time for recency (days_ago): the latest reading in
    the knowledge graph, so relative statements hold for a frozen snapshot or a
    feed that lags — the wall clock is only the fallback. With `query`, the
    facts that answer it (a named pair's distance, the node nearest to a named
    one, …) are listed first, as "focus"."""
    now = now or datetime.now(timezone.utc)
    recency, temporal_lines = temporal_facts(results, now, _row_label)

    lines = [f"Total results: {len(results)}"]
    points = _extract_points(results)
    focus = _focus_lines(query, points) if query and points else []
    if focus:
        lines.append("\n=== Facts for this question ===")
        lines += focus

    lines += temporal_lines

    if points:
        lines.extend(_spatial_lines(points))

    lines.extend(_numeric_lines(results))

    return {
        "recency": recency,
        "points": points,
        "focus": focus,
        "summary_text": "\n".join(lines),
    }
