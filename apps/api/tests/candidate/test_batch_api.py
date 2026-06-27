import io
import zipfile

from fastapi.testclient import TestClient


from app.main import app

def test_batch_upload_zip() -> None:
    client = TestClient(app)
    # Create a dummy in-memory ZIP file
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zf:
        zf.writestr("resume1.txt", "Nikhil Mehta\nPython, SQL\n2020-2024 Engineer")
        zf.writestr("resume2.txt", "Sanya Singh\nReact, TypeScript\n2018-2024 Developer")
    
    zip_buffer.seek(0)
    
    # Upload the ZIP
    response = client.post(
        "/api/v1/batch/upload-zip",
        files={"file": ("resumes.zip", zip_buffer.read(), "application/zip")},
    )
    
    assert response.status_code == 200, response.text
    data = response.json()
    assert "job_id" in data
    
    job_id = data["job_id"]
    
    # Check status
    status_res = client.get(f"/api/v1/batch/status/{job_id}")
    assert status_res.status_code == 200, status_res.text
    status_data = status_res.json()
    
    assert status_data["job_id"] == job_id
    assert status_data["total_files"] == 2
