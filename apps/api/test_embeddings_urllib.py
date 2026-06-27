import urllib.request
import json

def req(url, payload):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as f:
            return json.loads(f.read().decode())
    except Exception as e:
        print(f"Failed {url}: {e}")
        return None

role = req("http://127.0.0.1:8000/api/v1/generate-role-dna", {"job_description": "Software engineer Python"})
if not role:
    exit(1)
role_id = role["role_id"]

cand = req("http://127.0.0.1:8000/api/v1/build-digital-twins", {"resume_text": "Bob is a software engineer with Python"})
candidate_id = cand["candidate_id"]

emb = req("http://127.0.0.1:8000/api/v1/generate-embeddings", {"role_id": role_id, "candidate_id": candidate_id})
print("Embeddings:", emb)
