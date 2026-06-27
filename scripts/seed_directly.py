import os
import sys
# Add apps/api to path so it can import app modules
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "apps", "api"))

import json
import glob
from app.db.session import create_tables
from app.api.v1.dependencies import get_role_pipeline, get_candidate_pipeline

CANDIDATES_DIR = "data/demo/candidates"
JOBS_DIR = "data/demo/jobs"

def main():
    try:
        create_tables()
    except Exception as e:
        print("Tables already exist or failed:", e)

    role_pipeline = get_role_pipeline()
    cand_pipeline = get_candidate_pipeline()

    print("Ingesting jobs...")
    for f in glob.glob(os.path.join(JOBS_DIR, "*.json")):
        with open(f, "r") as file:
            payload = json.load(file)
            desc = payload.get("description", "A great job")
            job, _ = role_pipeline.upload_job(job_description=desc, source_name=payload.get("role_id"))
            # Bypass to just save role_dna directly
            from app.domain.role_dna import RoleDNAProfile
            dna = RoleDNAProfile(
                role_id=payload.get("role_id"),
                job_id=job.job_id,
                role_title=payload.get("role_title"),
                domain=payload.get("domain"),
                seniority=payload.get("seniority"),
                role_archetype="builder",
                fingerprint="abc-123",
                required_skills=payload.get("required_skills"),
                technical_depth=payload.get("technical_bar", 75),
                problem_solving=75,
                communication=payload.get("communication_bar", 70),
                ownership=payload.get("ownership_bar", 75),
                leadership=60,
                learning_agility=payload.get("velocity_bar", 75),
                ambiguity_tolerance=70,
                collaboration=80,
                startup_vs_enterprise_environment=80,
            )
            role_pipeline.role_repository.save(dna)

    print("Ingesting candidates...")
    from app.domain.candidate_twin import CandidateDigitalTwin
    for f in glob.glob(os.path.join(CANDIDATES_DIR, "*.json")):
        with open(f, "r") as file:
            payload = json.load(file)
            twin = CandidateDigitalTwin(**payload)
            cand_pipeline.candidate_repository.save(twin)

    print("Seed complete.")

if __name__ == "__main__":
    main()
