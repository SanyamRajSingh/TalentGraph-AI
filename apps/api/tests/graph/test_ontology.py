from app.modules.graph_builder import load_ontology


def test_ontology_loads_seed_adjacencies() -> None:
    ontology = load_ontology()

    assert "Python" in ontology["skills"]
    assert "FastAPI" in ontology["skills"]["Python"]
    assert "Machine Learning" in ontology["skills"]
    assert "Statistics" in ontology["skills"]["Machine Learning"]
