"""MultiTQ domain configuration (see scripts/domain.py)."""
from pathlib import Path

NAME = "MultiTQ (ICEWS05-15 political events)"
ONTOLOGY_NS = "http://herikgqa.org/multitq/ontology#"
RESOURCE_NS = "http://herikgqa.org/multitq/resource/"
PREFIX = "mtq:"
STORE = Path(__file__).resolve().parents[2] / "data_multitq" / "oxigraph"
