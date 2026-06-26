from fastapi.testclient import TestClient

from app.main import app


def test_role_dna_api_upload_generate_and_fetch() -> None:
    client = TestClient(app)

    upload_response = client.post(
        "/api/v1/upload-job",
        json={
            "job_description": "We are hiring a senior data scientist for fintech ML products.",
            "source_name": "demo",
        },
    )
    assert upload_response.status_code == 200
    job_id = upload_response.json()["job_id"]

    generate_response = client.post("/api/v1/generate-role-dna", json={"job_id": job_id})
    assert generate_response.status_code == 200
    body = generate_response.json()

    assert body["job_id"] == job_id
    assert body["role_dna"]["role_archetype"]
    assert body["role_dna"]["fingerprint"]
    assert body["role_dna"]["reasoning"]
    assert "Python" in body["role_dna"]["required_skills"] or body["role_dna"]["required_skills"]

    fetch_response = client.get(f"/api/v1/role-dna/{body['role_id']}")
    assert fetch_response.status_code == 200
    assert fetch_response.json()["role_id"] == body["role_id"]


def test_future_modules_remain_not_implemented() -> None:
    client = TestClient(app)

    response = client.post("/api/v1/rank-candidates")

    assert response.status_code == 501
