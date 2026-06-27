from fastapi.testclient import TestClient

from app.main import app


def test_explanation_api_generates_and_fetches_profile() -> None:
    client = TestClient(app)

    role_id = client.post(
        "/api/v1/generate-role-dna",
        json={
            "job_description": "Hiring fintech data scientist using Python SQL machine learning with strong communication.",
        },
    ).json()["role_id"]
    candidate_id = client.post(
        "/api/v1/build-digital-twins",
        json={
            "resume_text": "# Mira ML\nEmail: mira@example.com\n## Skills\n- Python\n- SQL\n- Machine Learning\n## Projects\n- 2024 Built churn model",
        },
    ).json()["candidate_id"]

    client.post("/api/v1/evaluate", json={"role_id": role_id, "candidate_id": candidate_id})
    client.post("/api/v1/rank", json={"role_id": role_id, "persona": "startup_founder"})

    response = client.post(
        "/api/v1/generate-explanations",
        json={"role_id": role_id, "candidate_id": candidate_id, "persona": "startup_founder"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["candidate_id"] == candidate_id
    assert body["explanation"]["ranking_position"] == 1
    assert body["explanation"]["strengths"]
    assert body["explanation"]["reasoning"]
    assert body["explanation"]["counterfactuals"]

    fetch_response = client.get(f"/api/v1/explanations/{candidate_id}")
    assert fetch_response.status_code == 200
    assert fetch_response.json()["candidate_id"] == candidate_id
