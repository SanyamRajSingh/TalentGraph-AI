from fastapi.testclient import TestClient

from app.main import app


def test_evaluation_api_round_trip() -> None:
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

    evaluation_response = client.post(
        "/api/v1/evaluate",
        json={"role_id": role_id, "candidate_id": candidate_id},
    )

    assert evaluation_response.status_code == 200
    body = evaluation_response.json()
    assert body["evaluation"]["overall_match"] >= 0
    assert body["evaluation"]["overall_confidence"] >= 0
    assert body["evaluation"]["technical"]["score"] >= 0

    fetch_response = client.get(f"/api/v1/evaluations/{body['evaluation_id']}")
    assert fetch_response.status_code == 200
    assert fetch_response.json()["evaluation_id"] == body["evaluation_id"]


def test_ranking_endpoint_still_501_after_evaluation_module() -> None:
    client = TestClient(app)

    response = client.post("/api/v1/rank-candidates")

    assert response.status_code == 501
