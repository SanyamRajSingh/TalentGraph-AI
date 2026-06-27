import httpx
import os
import json

client = httpx.Client(base_url="http://127.0.0.1:8000/api/v1", timeout=30.0)
res = client.post("/generate-role-dna", json={"job_description": "Software engineer with 5 years experience in Python and PostgreSQL"})
role_id = res.json()["role_id"]

res = client.post("/build-digital-twins", json={"resume_text": "Bob is a software engineer with 5 years experience in Python and PostgreSQL"})
candidate_id = res.json()["candidate_id"]

res = client.post("/generate-embeddings", json={"role_id": role_id, "candidate_id": candidate_id})
print(res.status_code)
print(res.text)
