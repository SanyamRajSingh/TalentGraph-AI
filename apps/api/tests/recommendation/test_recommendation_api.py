import pytest
from fastapi.testclient import TestClient

from app.main import app

def test_recommendation_api() -> None:
    client = TestClient(app)

    role_response = client.post(
        "/api/v1/generate-role-dna",
        json={"job_description": "Hiring backend engineer using Python FastAPI SQL with ownership."},
    )
    candidate_response = client.post(
        "/api/v1/build-digital-twins",
        json={
            "resume_text": "# Ada Backend\nEmail: ada@example.com\n## Skills\n- Python\n- FastAPI\n- SQL\n## Projects\n- 2024 Built API Platform",
        },
    )
    role_id = role_response.json()["role_id"]
    candidate_id = candidate_response.json()["candidate_id"]

    response = client.post(
        "/api/v1/recommend",
        json={"role_id": role_id, "candidate_id": candidate_id},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["recommendation"]["candidate_id"] == candidate_id
    assert data["recommendation"]["role_id"] == role_id
    assert data["recommendation"]["label"] in ["STRONG_HIRE", "HIRE", "GROWTH_HIRE", "BORDERLINE", "NO_HIRE"]
    assert "reason" in data["recommendation"]
