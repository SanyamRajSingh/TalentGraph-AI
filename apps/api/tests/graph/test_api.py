import pytest
from fastapi.testclient import TestClient

from app.main import app


def test_graph_and_embedding_api_round_trip() -> None:
    client = TestClient(app)

    role_response = client.post(
        "/api/v1/generate-role-dna",
        json={"job_description": "Hiring backend engineer using Python FastAPI SQL."},
    )
    candidate_response = client.post(
        "/api/v1/build-digital-twins",
        json={
            "resume_text": "# Ada Backend\nEmail: ada@example.com\n## Skills\n- Python\n- FastAPI\n## Projects\n- 2024 Built API Platform",
        },
    )
    role_id = role_response.json()["role_id"]
    candidate_id = candidate_response.json()["candidate_id"]

    graph_response = client.post("/api/v1/build-graph", json={"role_id": role_id, "candidate_id": candidate_id})
    assert graph_response.status_code == 200
    graph_id = graph_response.json()["graph_id"]
    assert graph_response.json()["graph"]["nodes"]
    assert graph_response.json()["graph"]["relationships"]

    fetch_graph_response = client.get(f"/api/v1/graph/{graph_id}")
    assert fetch_graph_response.status_code == 200
    assert fetch_graph_response.json()["graph_id"] == graph_id

    # Embeddings require sentence_transformers — skip gracefully if not installed
    pytest.importorskip("sentence_transformers", reason="sentence_transformers not installed")
    embeddings_response = client.post(
        "/api/v1/generate-embeddings",
        json={"role_id": role_id, "candidate_id": candidate_id},
    )
    assert embeddings_response.status_code == 200
    collection_id = embeddings_response.json()["collection_id"]
    assert embeddings_response.json()["collection"]["summaries"]
    assert embeddings_response.json()["collection"]["embeddings"]

    fetch_embeddings_response = client.get(f"/api/v1/embeddings/{collection_id}")
    assert fetch_embeddings_response.status_code == 200
    assert fetch_embeddings_response.json()["collection_id"] == collection_id


def test_future_recommendation_endpoint_remains_501() -> None:
    client = TestClient(app)

    response = client.post("/api/v1/rank-candidates")

    assert response.status_code == 501
