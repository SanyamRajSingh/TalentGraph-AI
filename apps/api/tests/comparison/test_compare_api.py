from fastapi.testclient import TestClient

from app.main import app


def _setup_role_and_candidates(client: TestClient) -> tuple[str, str, str]:
    """Returns (role_id, candidate_a_id, candidate_b_id)."""
    role_resp = client.post("/api/v1/generate-role-dna", json={
        "job_description": "Senior Data Scientist — Python, ML, SQL, stakeholder management, ownership.",
        "role_title": "Senior Data Scientist",
    })
    assert role_resp.status_code == 200
    role_id = role_resp.json()["role_id"]

    twin_a = client.post("/api/v1/build-digital-twins", json={
        "resume_text": "Alice Chen. Skills: Python, SQL, ML, leadership, TensorFlow. Projects: fraud model, churn model. 8 years experience.",
    })
    assert twin_a.status_code == 200
    candidate_a_id = twin_a.json()["candidate_id"]

    twin_b = client.post("/api/v1/build-digital-twins", json={
        "resume_text": "Bob Patel. Skills: Python, R, statistics, communication. Projects: pricing model. 4 years experience.",
    })
    assert twin_b.status_code == 200
    candidate_b_id = twin_b.json()["candidate_id"]

    return role_id, candidate_a_id, candidate_b_id


def test_compare_returns_matrix() -> None:
    client = TestClient(app)
    role_id, cid_a, cid_b = _setup_role_and_candidates(client)

    resp = client.post("/api/v1/compare", json={
        "candidate_a_id": cid_a,
        "candidate_b_id": cid_b,
        "role_id": role_id,
    })
    assert resp.status_code == 200
    data = resp.json()

    assert data["candidate_a_id"] == cid_a
    assert data["candidate_b_id"] == cid_b
    assert data["role_id"] == role_id
    assert len(data["dimensions"]) > 0
    assert data["overall_winner"] in ("A", "B", "TIE")
    assert len(data["summary"]) > 10
    assert len(data["recommendation"]) > 10


def test_compare_404_for_missing_candidate() -> None:
    client = TestClient(app)
    role_resp = client.post("/api/v1/generate-role-dna", json={
        "job_description": "Engineer role.",
        "role_title": "Engineer",
    })
    role_id = role_resp.json()["role_dna"]["role_id"]

    resp = client.post("/api/v1/compare", json={
        "candidate_a_id": "nonexistent-a",
        "candidate_b_id": "nonexistent-b",
        "role_id": role_id,
    })
    assert resp.status_code == 404
