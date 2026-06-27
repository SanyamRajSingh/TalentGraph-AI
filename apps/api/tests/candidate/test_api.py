from fastapi.testclient import TestClient

from app.main import app


def test_candidate_api_upload_build_list_and_fetch() -> None:
    client = TestClient(app)

    upload_response = client.post(
        "/api/v1/upload-candidates",
        json={
            "resume_text": "# Ada Smith\nEmail: ada@example.com\n## Skills\n- Python\n- SQL\n## Projects\n- 2024 Built API",
            "source_name": "ada.md",
        },
    )
    assert upload_response.status_code == 200
    resume_id = upload_response.json()["resume_id"]

    build_response = client.post("/api/v1/build-digital-twins", json={"resume_id": resume_id})
    assert build_response.status_code == 200
    body = build_response.json()

    assert body["twin"]["resume_id"] == resume_id
    assert body["twin"]["name"] == "Ada Smith"
    assert body["twin"]["growth_stage"]
    assert body["twin"]["reasoning"]

    list_response = client.get("/api/v1/candidates")
    assert list_response.status_code == 200
    assert list_response.json()["items"]

    fetch_response = client.get(f"/api/v1/candidate/{body['candidate_id']}")
    assert fetch_response.status_code == 200
    assert fetch_response.json()["candidate_id"] == body["candidate_id"]


def test_future_modules_still_return_501() -> None:
    client = TestClient(app)

    response = client.post("/api/v1/rank-candidates")

    assert response.status_code == 501


def test_upload_file_txt() -> None:
    client = TestClient(app)
    
    # Text file upload
    response = client.post(
        "/api/v1/upload-file",
        files={"file": ("test_resume.txt", b"# Bob Smith\nEmail: bob@example.com\n## Skills\n- Python", "text/plain")},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["twin"]["name"] == "Bob Smith"


def test_upload_file_pdf_fallback() -> None:
    # If pypdf is installed, it will try to parse this dummy byte string and fail gracefully, returning a string indicating error.
    # We just want to ensure it doesn't 500.
    client = TestClient(app)
    response = client.post(
        "/api/v1/upload-file",
        files={"file": ("test.pdf", b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\n", "application/pdf")},
    )
    assert response.status_code == 200
    assert "twin" in response.json()

