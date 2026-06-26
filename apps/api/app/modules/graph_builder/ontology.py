import json
from functools import lru_cache
from pathlib import Path


ONTOLOGY_ROOT = Path(__file__).resolve().parents[5] / "data" / "ontology"


@lru_cache
def load_ontology() -> dict[str, dict[str, list[str]]]:
    """Load deterministic ontology seed files."""

    ontology: dict[str, dict[str, list[str]]] = {}
    for name in ("skills", "technologies", "domains"):
        path = ONTOLOGY_ROOT / f"{name}.json"
        with path.open("r", encoding="utf-8") as handle:
            ontology[name] = json.load(handle)
    return ontology
