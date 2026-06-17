"""
Spatial and temporal analysis helpers.

Pre-computes recency ranking and basic statistics from SPARQL results
so the answer generator receives structured analysis rather than raw rows.
"""

from __future__ import annotations
from datetime import datetime, timezone
from typing import Any


def _extract_time(row: dict) -> datetime | None:
    time_keys = [k for k in row if "time" in k.lower() or "date" in k.lower()]
    for k in time_keys:
        v = row.get(k)
        if not v:
            continue
        for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d"):
            try:
                return datetime.strptime(v[:19], fmt[:len(v[:19])]).replace(tzinfo=timezone.utc)
            except ValueError:
                continue
    return None


def _row_label(row: dict) -> str:
    for key in ("Site_label", "site_label", "label", "Sensor_label",
                "sensor_label", "name", "ObservedProperty_label"):
        v = row.get(key)
        if v and not v.startswith("http"):
            return v[:50]
    for v in row.values():
        if isinstance(v, str) and not v.startswith("http") and len(v) < 60:
            return v[:50]
    for v in row.values():
        if isinstance(v, str) and v.startswith("http"):
            return v.rsplit("/", 1)[-1][:50]
    return str(list(row.values())[0])[:50]


def analyze(results: list[dict[str, Any]]) -> dict[str, Any]:
    now = datetime.now(timezone.utc)

    enriched = []
    for row in results:
        ts = _extract_time(row)
        days = (now - ts).days if ts else None
        enriched.append({**row, "_days_ago": days, "_ts": ts})

    # ── Recency ranking ──────────────────────────────────────────────
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

    # ── Summary text for LLM ────────────────────────────────────────
    lines = []
    lines.append(f"Total results: {len(results)}")

    if recency:
        lines.append(f"\n=== Temporal recency (most recent first, showing up to 20) ===")
        for r in recency[:20]:
            lines.append(f"  {r['label']:50s}  {r['timestamp']}  ({r['days_ago']} days ago)")
        if len(recency) > 20:
            lines.append(f"  … and {len(recency) - 20} more.")

    # ── Numeric value summary ────────────────────────────────────────
    for key in ("hasSimpleResult", "count", "avg", "min", "max", "n"):
        vals = []
        for row in results:
            for k, v in row.items():
                if key.lower() in k.lower() and v is not None:
                    try:
                        vals.append(float(v))
                    except (ValueError, TypeError):
                        pass
        if vals:
            lines.append(f"\n=== Numeric summary for '{key}' ===")
            lines.append(f"  count: {len(vals)}, min: {min(vals):.4f}, max: {max(vals):.4f}, "
                         f"avg: {sum(vals)/len(vals):.4f}")

    return {
        "recency": recency,
        "summary_text": "\n".join(lines),
    }
