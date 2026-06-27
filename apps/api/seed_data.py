"""
Seed script - inserts 50 realistic candidates and 10 job roles.
Run from apps/api directory using:
  $env:PYTHONPATH="."; C:/Users/sanya/anaconda3/python.exe seed_data.py

Supports both Memory and PostgreSQL repositories (auto-detected via DATABASE_URL).
Idempotent: skips seed if >10 candidates already exist.
"""

import os
import random

from app.domain.candidate_twin import (
    CandidateDigitalTwin,
    CandidateTimelineEntry,
    GrowthStage,
)
from app.domain.role_dna import RoleDNAProfile, WorkEnvironmentAttributes
from app.domain.ranking import HiringPersona
from app.api.v1.dependencies import (
    get_candidate_repository,
    get_role_dna_repository,
    get_evaluation_pipeline,
    get_ranking_pipeline,
)

# ── Data definitions ──────────────────────────────────────────────────────────

DOMAINS_MAP = {
    "Fintech":       ["Payments", "Risk Management", "Blockchain"],
    "Healthcare":    ["EHR Integration", "Telehealth", "HIPAA"],
    "E-commerce":    ["Inventory Systems", "Cart Optimization", "Payments"],
    "EdTech":        ["LMS", "Video Streaming", "Gamification"],
    "SaaS":          ["Multi-tenancy", "Stripe Billing", "Microservices"],
    "Cybersecurity": ["Pen Testing", "IAM", "Cryptography"],
    "Cloud":         ["AWS", "Kubernetes", "Terraform"],
    "AI/ML":         ["LLMs", "PyTorch", "RAG"],
    "Gaming":        ["Unity", "Unreal", "Game Design"],
    "Automotive":    ["ADAS", "CAN Bus", "Embedded Systems"],
}

ROLE_SKILL_MAP = {
    "Backend Engineer":    ["Python", "FastAPI", "PostgreSQL", "Redis", "Docker"],
    "ML Engineer":         ["Python", "PyTorch", "MLflow", "Kubeflow", "SQL"],
    "Data Scientist":      ["Python", "Pandas", "Scikit-learn", "Spark", "SQL"],
    "Product Analyst":     ["SQL", "Tableau", "A/B Testing", "Excel", "Python"],
    "Full Stack Engineer": ["React", "TypeScript", "Node.js", "FastAPI", "Docker"],
}

LEVELS = ["Junior", "Mid-Level", "Senior", "Lead", "Principal"]

LEVEL_EXP = {
    "Junior":    (1, 3),
    "Mid-Level": (3, 6),
    "Senior":    (6, 10),
    "Lead":      (8, 14),
    "Principal": (12, 20),
}

LOCATIONS = [
    "San Francisco, CA", "New York, NY", "Austin, TX",
    "Seattle, WA", "Remote", "London, UK",
    "Berlin, Germany", "Toronto, Canada",
]

COMPANIES = ["TechStartup", "MegaCorp", "ScaleAI", "DevHouse", "InnovateCo", "BuildFast", "DataLabs"]


def _slug(text: str) -> str:
    return text.lower().replace(" ", "_").replace("/", "_")


def _generate_timeline(level: str, role: str, years: int) -> list[CandidateTimelineEntry]:
    events = []
    for y in range(min(years, 6)):
        company = COMPANIES[y % len(COMPANIES)]
        events.append(CandidateTimelineEntry(
            year=2024 - y,
            event=f"{level} {role} at {company}"
        ))
    return events


def generate_candidates() -> list[CandidateDigitalTwin]:
    candidates = []
    domain_list = list(DOMAINS_MAP.keys())
    role_list = list(ROLE_SKILL_MAP.keys())

    for role_idx, role in enumerate(role_list):  # 5 roles × 10 = 50 candidates
        for i in range(10):
            level = LEVELS[i % len(LEVELS)]
            domain = domain_list[(role_idx * 2 + i) % len(domain_list)]
            exp_range = LEVEL_EXP[level]
            years = random.randint(*exp_range)

            td  = min(100, 30 + years * 5 + random.randint(-5, 10))
            lv  = random.randint(55, 95)
            ldr = min(100, 20 + years * 4 + random.randint(-5, 10))
            collab = random.randint(65, 95)
            comm   = random.randint(60, 95)
            proj   = min(100, 25 + years * 5 + random.randint(-10, 15))

            if level in ["Junior", "Mid-Level"]:
                growth = GrowthStage.BUILDER
            elif level == "Senior":
                growth = GrowthStage.TECHNICAL_SPECIALIST
            elif level == "Lead":
                growth = GrowthStage.EMERGING_LEADER
            else:
                growth = GrowthStage.ARCHITECT if hasattr(GrowthStage, "ARCHITECT") else GrowthStage.TECHNICAL_SPECIALIST

            skills = list(ROLE_SKILL_MAP[role])[:4]
            skills.append(DOMAINS_MAP[domain][0])

            cand = CandidateDigitalTwin(
                candidate_id=f"seed_{_slug(role)}_{i:02d}",
                name=f"{level} {role} #{i + 1}",
                email=f"{_slug(level)}.{_slug(role).replace('_', '')}{i + 1}@talentgraph.dev",
                phone=f"+1-555-{100 + role_idx:03d}-{1000 + i:04d}",
                location=LOCATIONS[i % len(LOCATIONS)],
                skills=skills,
                projects=[
                    f"Led {domain} platform rebuild (25% perf gain)",
                    f"Shipped {role} tooling for distributed teams",
                ],
                domains=[domain],
                timeline=_generate_timeline(level, role, years),
                technical_depth=td,
                learning_velocity=lv,
                leadership=ldr,
                leadership_readiness=min(100, ldr + 5),
                ownership=min(100, lv + random.randint(5, 15)),
                communication=comm,
                project_complexity=proj,
                collaboration=collab,
                adaptability=random.randint(60, 95),
                execution_speed=random.randint(60, 95),
                business_acumen=random.randint(50, 90),
                growth_stage=growth,
                strengths=[f"Strong {skills[0]} skills", f"{domain} domain expertise"],
                weaknesses=["Limited public-speaking experience"],
                confidence=min(100, (td + lv + ldr) // 3),
                risk_profile="Low" if lv >= 80 else "Medium" if lv >= 60 else "High",
            )
            candidates.append(cand)

    return candidates


def generate_jobs() -> list[RoleDNAProfile]:
    jobs = []
    role_list = list(ROLE_SKILL_MAP.keys())
    seniorities = ["Senior", "Lead"]

    idx = 0
    for role in role_list:
        for seniority in seniorities:
            td = 75 if seniority == "Senior" else 85
            jobs.append(RoleDNAProfile(
                role_id=f"seed_role_{idx:02d}",
                role_title=f"{seniority} {role}",
                domain="Technology",
                seniority=seniority,
                role_archetype="Individual Contributor" if seniority == "Senior" else "Team Lead",
                fingerprint=f"{_slug(seniority)}_{_slug(role)}_{idx}",
                required_skills=list(ROLE_SKILL_MAP[role])[:3],
                preferred_skills=list(ROLE_SKILL_MAP[role])[3:],
                technical_depth=td,
                problem_solving=td,
                communication=70,
                ownership=80,
                leadership=70 if seniority == "Lead" else 50,
                learning_agility=75,
                ambiguity_tolerance=65,
                collaboration=75,
                startup_vs_enterprise_environment=60,
                work_environment=WorkEnvironmentAttributes(
                    ownership=80,
                    collaboration=75,
                    communication=70,
                ),
                confidence=80,
            ))
            idx += 1

    return jobs


def run() -> None:
    print("[seed] Checking existing data...")
    cand_repo = get_candidate_repository()
    role_repo = get_role_dna_repository()

    existing = cand_repo.list_candidates()
    if len(existing) > 10:
        print(f"[seed] Already have {len(existing)} candidates -- skipping seed.")
        return

    print("[seed] Generating seed data...")
    candidates = generate_candidates()
    jobs = generate_jobs()

    for j in jobs:
        role_repo.save(j)
    print(f"  [OK] Saved {len(jobs)} job roles")

    for c in candidates:
        cand_repo.save(c)
    print(f"  [OK] Saved {len(candidates)} candidates")

    # Write JSON snapshots to disk
    os.makedirs(os.path.join("data", "demo", "candidates"), exist_ok=True)
    os.makedirs(os.path.join("data", "demo", "jobs"), exist_ok=True)

    for c in candidates:
        path = os.path.join("data", "demo", "candidates", f"{c.candidate_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            f.write(c.model_dump_json(indent=2))

    for j in jobs:
        path = os.path.join("data", "demo", "jobs", f"{j.role_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            f.write(j.model_dump_json(indent=2))

    print("  [OK] Wrote JSON snapshots to data/demo/")

    print("[seed] Running evaluations and rankings...")
    eval_pipe = get_evaluation_pipeline()
    rank_pipe = get_ranking_pipeline()

    for j in jobs:
        for c in candidates:
            try:
                eval_pipe.run(role_id=j.role_id, candidate_id=c.candidate_id)
            except Exception as e:
                print(f"  [WARN] Eval failed {c.candidate_id}/{j.role_id}: {e}")

        try:
            rank_pipe.run(role_id=j.role_id, persona=HiringPersona.STARTUP_FOUNDER)
            print(f"  [OK] Ranked candidates for {j.role_title}")
        except Exception as e:
            print(f"  [WARN] Ranking failed {j.role_id}: {e}")

    print(f"\n[seed] DONE -- {len(candidates)} candidates, {len(jobs)} roles.")


if __name__ == "__main__":
    run()
