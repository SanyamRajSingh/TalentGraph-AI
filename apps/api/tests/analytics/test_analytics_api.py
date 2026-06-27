from fastapi.testclient import TestClient

from app.main import app

def test_get_analytics_overview() -> None:
    client = TestClient(app)
    
    # Generate some data to ensure non-zero counts
    role_resp = client.post("/api/v1/generate-role-dna", json={
        "job_description": "Senior Data Scientist",
        "role_title": "Data Scientist",
    })
    
    twin_resp = client.post("/api/v1/build-digital-twins", json={
        "resume_text": "Alice Chen. Skills: Python, SQL. 8 years experience.",
    })
    
    # Get analytics
    resp = client.get("/api/v1/analytics/overview")
    assert resp.status_code == 200
    data = resp.json()
    
    assert data["total_candidates"] >= 1
    assert data["total_roles"] >= 1
    assert "total_evaluations" in data
    assert "average_confidence" in data
    assert "growth_stage_distribution" in data
    assert "top_skills" in data
