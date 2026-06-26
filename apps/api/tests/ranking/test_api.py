from fastapi.testclient import TestClient

from app.main import app


def test_ranking_api_ranks_existing_evaluations_by_persona() -> None:
    client = TestClient(app)

    role_response = client.post(
        "/api/v1/generate-role-dna",
        json={"job_description": "Hiring backend engineer using Python FastAPI SQL with ownership."},
    )
    role_id = role_response.json()["role_id"]

    candidate_one = client.post(
        "/api/v1/build-digital-twins",
        json={
            "resume_text": "# Ada Backend\nEmail: ada@example.com\n## Skills\n- Python\n- FastAPI\n- SQL\n## Projects\n- 2024 Built API Platform",
        },
    ).json()["candidate_id"]
    candidate_two = client.post(
        "/api/v1/build-digital-twins",
        json={
            "resume_text": "# Ben Analyst\nEmail: ben@example.com\n## Skills\n- SQL\n## Projects\n- 2024 Built dashboard",
        },
    ).json()["candidate_id"]

    client.post("/api/v1/evaluate", json={"role_id": role_id, "candidate_id": candidate_one})
    client.post("/api/v1/evaluate", json={"role_id": role_id, "candidate_id": candidate_two})

    rank_response = client.post("/api/v1/rank", json={"role_id": role_id, "persona": "startup_founder"})

    assert rank_response.status_code == 200
    body = rank_response.json()
    assert body["role_id"] == role_id
    assert body["persona"] == "startup_founder"
    assert len(body["rankings"]) >= 2
    assert body["rankings"][0]["rank"] == 1

    fetch_response = client.get(f"/api/v1/rankings/{role_id}?persona=startup_founder")
    assert fetch_response.status_code == 200
    assert fetch_response.json()["rankings"]


def test_future_explanation_endpoint_still_501_after_ranking_module() -> None:
    client = TestClient(app)

    response = client.post("/api/v1/generate-explanations")

    assert response.status_code == 501
