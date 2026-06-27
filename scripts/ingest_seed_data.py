import os
import json
import urllib.request
import glob
import time

CANDIDATES_DIR = "data/demo/candidates"
JOBS_DIR = "data/demo/jobs"

API_BASE = "http://127.0.0.1:8000/api/v1"

def ingest_jobs():
    print("Ingesting jobs...")
    job_files = glob.glob(os.path.join(JOBS_DIR, "*.json"))
    for f in job_files:
        with open(f, "r") as file:
            payload = json.load(file)
            req = urllib.request.Request(
                f"{API_BASE}/roles",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            try:
                res = urllib.request.urlopen(req)
                if res.status not in (200, 201):
                    print(f"Failed to ingest job {payload.get('role_id')}")
                else:
                    print(f"Ingested job {payload.get('role_id')}")
            except Exception as e:
                print(f"Error ingesting job {payload.get('role_id')}: {e}")
                
def ingest_candidates():
    print("Ingesting candidates...")
    cand_files = glob.glob(os.path.join(CANDIDATES_DIR, "*.json"))
    for f in cand_files:
        with open(f, "r") as file:
            payload = json.load(file)
            req = urllib.request.Request(
                f"{API_BASE}/candidates/json",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            try:
                res = urllib.request.urlopen(req)
                if res.status not in (200, 201):
                    print(f"Failed to ingest candidate {payload.get('candidate_id')}")
                else:
                    print(f"Ingested candidate {payload.get('candidate_id')}")
            except Exception as e:
                print(f"Error ingesting candidate {payload.get('candidate_id')}: {e}")

if __name__ == "__main__":
    ingest_jobs()
    ingest_candidates()
    print("Ingestion complete.")
