"""
Pre-computed analysis of a result set, so the answer LLM never does the maths:
recency, per-quantity numeric stats, and spatial metrics when rows carry
node coordinates. Sections are emitted only when the data supports them.
"""

from __future__ import annotations
from datetime import datetime, timezone
from math import radians, sin, cos, asin, sqrt
from typing import Any

_MAX_RECENCY_ROWS = 20
_EARTH_RADIUS_M = 6_371_000.0


# ── Time ─────────────────────────────────────────────────────────────────────

def _parse_dt(v: str) -> datetime | None:
    if not v:
        return None
    s = v.strip().replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(s)
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _extract_time(row: dict) -> datetime | None:
    for k in row:
        if "time" in k.lower() or "date" in k.lower():
            dt = _parse_dt(str(row.get(k) or ""))
            if dt:
                return dt
    return None


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


def _extract_points(results: list[dict]) -> list[dict]:
    # One point per distinct (label, lat, lon); altitude optional.
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
        key = (lat_f, lon_f)
        if key in seen:
            continue
        seen.add(key)
        points.append({"label": _row_label(row), "lat": lat_f, "lon": lon_f, "alt": alt_f})
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

    lines.append("  points (label: lat, lon, alt):")
    for p in points[:_MAX_RECENCY_ROWS]:
        alt = f", {p['alt']:.1f} m" if p["alt"] is not None else ""
        lines.append(f"    {p['label']:20s} {p['lat']:.6f}, {p['lon']:.6f}{alt}")
    if n > _MAX_RECENCY_ROWS:
        lines.append(f"    … and {n - _MAX_RECENCY_ROWS} more")
    return lines


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


# ── Entry point ──────────────────────────────────────────────────────────────

def analyze(results: list[dict[str, Any]]) -> dict[str, Any]:
    now = datetime.now(timezone.utc)

    timed = []
    for row in results:
        ts = _extract_time(row)
        timed.append((ts, row))
    with_time = sorted((t for t in timed if t[0] is not None),
                       key=lambda t: t[0], reverse=True)

    recency = [
        {"label": _row_label(r), "timestamp": ts.isoformat(),
         "days_ago": (now - ts).days}
        for ts, r in with_time
    ]

    lines = [f"Total results: {len(results)}"]

    if recency:
        span_new = with_time[0][0]
        span_old = with_time[-1][0]
        lines.append(f"\n=== Temporal ({len(recency)} timestamped rows) ===")
        lines.append(f"  newest: {span_new.isoformat()}")
        lines.append(f"  oldest: {span_old.isoformat()}")
        lines.append(f"  span:   {span_new - span_old}")
        lines.append("  most recent first:")
        for r in recency[:_MAX_RECENCY_ROWS]:
            lines.append(f"    {r['label']:40s}  {r['timestamp']}")
        if len(recency) > _MAX_RECENCY_ROWS:
            lines.append(f"    … and {len(recency) - _MAX_RECENCY_ROWS} more")

    points = _extract_points(results)
    if points:
        lines.extend(_spatial_lines(points))

    lines.extend(_numeric_lines(results))

    return {
        "recency": recency,
        "points": points,
        "summary_text": "\n".join(lines),
    }
