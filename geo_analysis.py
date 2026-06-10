"""
Spatial and temporal analysis helpers.

Pre-computes distances, recency, and proximity clusters from SPARQL results
so the answer generator receives hard numbers rather than raw coordinates.
"""

from __future__ import annotations
import math
from datetime import datetime, timezone
from typing import Any


# ── Haversine distance ─────────────────────────────────────────────────────────

def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


# ── Extract lat/lon from a result row ─────────────────────────────────────────

def _extract_coords(row: dict) -> tuple[float, float] | None:
    """Try common lat/lon field names produced by the SPARQL retriever."""
    lat_keys = [k for k in row if "lat" in k.lower()]
    lon_keys = [k for k in row if "lon" in k.lower()]
    try:
        if lat_keys and lon_keys:
            return float(row[lat_keys[0]]), float(row[lon_keys[0]])
    except (TypeError, ValueError):
        pass
    return None


def _extract_time(row: dict) -> datetime | None:
    """Try common observation/event time field names."""
    time_keys = [k for k in row if "time" in k.lower() or "date" in k.lower()]
    for k in time_keys:
        v = row.get(k)
        if not v:
            continue
        for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
            try:
                return datetime.strptime(v[:19], fmt).replace(tzinfo=timezone.utc)
            except ValueError:
                continue
    return None


# ── Main analysis function ─────────────────────────────────────────────────────

def analyze(
    results: list[dict[str, Any]],
    pilot_lat: float,
    pilot_lon: float,
    pilot_name: str = "pilot site",
    proximity_threshold_km: float = 300.0,
) -> dict[str, Any]:
    """
    Returns a structured analysis dict with:
      - distances_to_pilot: each row labelled with its distance to the pilot site
      - proximity_groups: clusters of rows within proximity_threshold_km of each other
      - recency: rows ranked by how recent their timestamp is
      - summary_text: a pre-formatted text block the LLM can quote directly
    """
    now = datetime.now(timezone.utc)

    # Attach derived fields to each row
    enriched = []
    for row in results:
        coords = _extract_coords(row)
        ts     = _extract_time(row)
        dist   = haversine_km(pilot_lat, pilot_lon, *coords) if coords else None
        days   = (now - ts).days if ts else None
        enriched.append({**row, "_coords": coords, "_dist_km": dist, "_days_ago": days, "_ts": ts})

    # ── Distances to pilot ────────────────────────────────────────────────────
    with_dist = [r for r in enriched if r["_dist_km"] is not None]
    with_dist.sort(key=lambda r: r["_dist_km"])

    distances_to_pilot = [
        {
            "label": _row_label(r),
            "distance_km": round(r["_dist_km"], 1),
            "coords": r["_coords"],
        }
        for r in with_dist
    ]

    # ── Recency ranking ───────────────────────────────────────────────────────
    with_time = [r for r in enriched if r["_days_ago"] is not None]
    with_time.sort(key=lambda r: r["_days_ago"])

    recency = [
        {
            "label": _row_label(r),
            "timestamp": str(r["_ts"].date()) if r["_ts"] else None,
            "days_ago": r["_days_ago"],
        }
        for r in with_time
    ]

    # ── Proximity groups ──────────────────────────────────────────────────────
    proximity_groups = _cluster(with_dist, proximity_threshold_km)

    # ── Summary text for LLM ─────────────────────────────────────────────────
    lines = []

    if distances_to_pilot:
        lines.append(f"=== Distance to {pilot_name} ({pilot_lat:.4f}°N, {pilot_lon:.4f}°E) ===")
        for d in distances_to_pilot:
            lat, lon = d["coords"]
            lines.append(f"  {d['label']:45s}  {d['distance_km']:7.1f} km  "
                         f"[{lat:.4f}°N, {lon:.4f}°E]")

    if proximity_groups:
        lines.append(f"\n=== Spatial proximity clusters (threshold: {proximity_threshold_km:.0f} km) ===")
        for i, group in enumerate(proximity_groups, 1):
            names = ", ".join(_row_label(r) for r in group)
            center_lat = sum(r["_coords"][0] for r in group) / len(group)
            center_lon = sum(r["_coords"][1] for r in group) / len(group)
            lines.append(f"  Cluster {i}: {names}")
            lines.append(f"    centroid: {center_lat:.4f}°N, {center_lon:.4f}°E")
            if len(group) > 1:
                max_d = max(
                    haversine_km(*group[a]["_coords"], *group[b]["_coords"])
                    for a in range(len(group)) for b in range(a + 1, len(group))
                )
                lines.append(f"    max internal distance: {max_d:.1f} km")

    if recency:
        lines.append("\n=== Temporal recency (most recent first) ===")
        for r in recency:
            lines.append(f"  {r['label']:45s}  {r['timestamp']}  ({r['days_ago']} days ago)")

    return {
        "distances_to_pilot": distances_to_pilot,
        "proximity_groups": [[_row_label(r) for r in g] for g in proximity_groups],
        "recency": recency,
        "summary_text": "\n".join(lines),
    }


# ── Helpers ───────────────────────────────────────────────────────────────────

def _row_label(row: dict) -> str:
    """Pick the most human-readable label from a result row."""
    for key in ("name", "asset_name", "measurement_name", "asset"):
        v = row.get(key)
        if v and not v.startswith("http"):
            return v[:44]
    # Fall back to the URI's local name
    for v in row.values():
        if isinstance(v, str) and v.startswith("http"):
            return v.rsplit("/", 1)[-1][:44]
    return str(list(row.values())[0])[:44]


def _cluster(rows: list[dict], threshold_km: float) -> list[list[dict]]:
    """Single-linkage clustering: group rows within threshold_km of any cluster member."""
    unassigned = list(rows)
    clusters: list[list[dict]] = []

    while unassigned:
        seed = unassigned.pop(0)
        group = [seed]
        changed = True
        while changed:
            changed = False
            remaining = []
            for r in unassigned:
                if any(haversine_km(*r["_coords"], *g["_coords"]) <= threshold_km for g in group):
                    group.append(r)
                    changed = True
                else:
                    remaining.append(r)
            unassigned = remaining
        if len(group) > 1:   # only report actual clusters (2+ points)
            clusters.append(group)

    return clusters
