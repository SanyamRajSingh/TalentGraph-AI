from fastapi.testclient import TestClient
from app.main import app

def test_copilot_api() -> None:
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

    # First we must evaluate so copilot has a bundle
    client.post(
        "/api/v1/evaluate",
        json={"role_id": role_id, "candidate_id": candidate_id},
    )

    response = client.post(
        "/api/v1/copilot/draft-email",
        json={"role_id": role_id, "candidate_id": candidate_id},
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "subject" in data
    assert "body" in data
    assert "Ada Backend" in data["body"]
    assert "backend engineer" in data["subject"].lower()
