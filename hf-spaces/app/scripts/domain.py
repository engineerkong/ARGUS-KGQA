"""
Which knowledge graph HeriKGQA answers over.

HERIKGQA_DOMAIN=herikg (the default) is the HERIKG pipeline, unchanged. Any other value loads
domains/<name>/: its ontology (<name>.owl), its configuration (config.py: resource namespace,
store) and its prompt parts (prompt.py). Modules that differ per domain branch on IS_HERIKG.
"""
from __future__ import annotations

import importlib.util
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = os.environ.get("HERIKGQA_DOMAIN", "herikg").strip().lower() or "herikg"
IS_HERIKG = DOMAIN == "herikg"
DOMAIN_DIR = ROOT / "domains" / DOMAIN

_loaded: dict[str, object] = {}


def load(module: str):
    """domains/<DOMAIN>/<module>.py, imported once."""
    if module not in _loaded:
        path = DOMAIN_DIR / f"{module}.py"
        spec = importlib.util.spec_from_file_location(f"herikgqa_domain_{DOMAIN}_{module}", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _loaded[module] = mod
    return _loaded[module]
