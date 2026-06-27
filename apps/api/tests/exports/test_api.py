from io import BytesIO

from fastapi.testclient import TestClient
from openpyxl import load_workbook

from app.main import app


def test_export_rankings_api_returns_xlsx() -> None:
    client = TestClient(app)

    role_id = client.post(
        "/api/v1/generate-role-dna",
        json={"job_description": "Hiring fintech data scientist using Python SQL machine learning."},
    ).json()["role_id"]
    candidate_id = client.post(
        "/api/v1/build-digital-twins",
        json={
            "resume_text": "# Ada Analyst\nEmail: ada@example.com\n## Skills\n- Python\n- SQL\n- Machine Learning\n## Projects\n- 2024 Built fraud model",
        },
    ).json()["candidate_id"]
    client.post("/api/v1/evaluate", json={"role_id": role_id, "candidate_id": candidate_id})
    client.post("/api/v1/rank", json={"role_id": role_id, "persona": "startup_founder"})
    client.post(
        "/api/v1/generate-explanations",
        json={"role_id": role_id, "candidate_id": candidate_id, "persona": "startup_founder"},
    )

    response = client.post(
        "/api/v1/export-rankings",
        json={"role_id": role_id, "persona": "startup_founder"},
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    workbook = load_workbook(BytesIO(response.content))
    sheet = workbook["Rankings"]
    assert sheet["A1"].value == "Rank"
    assert sheet["B2"].value == "Ada Analyst"
    assert sheet["E2"].value
