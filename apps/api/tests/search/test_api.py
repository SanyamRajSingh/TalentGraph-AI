import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.api.v1.dependencies import get_candidate_repository
from app.domain.candidate_twin import CandidateDigitalTwin

def test_search_candidates_match_type() -> None:
    pytest.importorskip("sentence_transformers", reason="sentence_transformers not installed")
    client = TestClient(app)
    
    # Pre-populate candidate repository with some mock twins
    repo = get_candidate_repository()
    
    # Twin 1: The anchor
    twin1 = CandidateDigitalTwin(
        name="Alice Backend",
        skills=["Python", "Django", "SQL", "Postgres", "Redis"],
        domains=["E-commerce", "Fintech"]
    )
    repo.save(twin1)
    
    # Twin 2: Very similar to anchor
    twin2 = CandidateDigitalTwin(
        name="Bob Backend",
        skills=["Python", "FastAPI", "SQL", "Postgres", "Redis", "Docker"],
        domains=["Fintech"]
    )
    repo.save(twin2)
    
    # Twin 3: Transferable (some overlap but not a clone)
    twin3 = CandidateDigitalTwin(
        name="Charlie Frontend",
        skills=["JavaScript", "React", "Python", "SQL"],
        domains=["E-commerce"]
    )
    repo.save(twin3)

    # Search for similar candidates to twin1
    response = client.get(f"/api/v1/search/candidates?candidate_id={twin1.candidate_id}&match_type=similar")
    assert response.status_code == 200
    similar_results = response.json()
    
    # Bob should be here because he's a very close match
    similar_names = [r["name"] for r in similar_results]
    assert "Bob Backend" in similar_names
    # Charlie might not be if his score is < 0.75
    # (Actually depends on the mock embedding provider, which returns deterministic vectors)
    
    # Search for transferable candidates
    response2 = client.get(f"/api/v1/search/candidates?candidate_id={twin1.candidate_id}&match_type=transferable")
    assert response2.status_code == 200
    transfer_results = response2.json()
    
    # Charlie should ideally be here if his score is 0.40 <= score < 0.75
    # (This test just proves the endpoint accepts the parameter and runs without error)
    assert isinstance(transfer_results, list)
