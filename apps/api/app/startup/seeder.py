"""
Startup seeder — idempotent demo data loader.

Runs on every application startup. If repositories already contain data,
it exits immediately (no-op). Otherwise it seeds 50 candidates, 10 roles,
and runs the full pipeline (evaluations -> rankings -> explanations ->
embeddings -> graph) so the application is fully functional out of the box.

Compatible with both in-memory and PostgreSQL repositories.
"""

import logging
import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Static seed data definitions
# ---------------------------------------------------------------------------

_DOMAINS_MAP: dict[str, list[str]] = {
    "Fintech":       ["Payments", "Risk Management", "Blockchain"],
    "Healthcare":    ["EHR Integration", "Telehealth", "HIPAA Compliance"],
    "E-commerce":    ["Inventory Systems", "Cart Optimization", "Payments"],
    "EdTech":        ["LMS Platforms", "Video Streaming", "Gamification"],
    "SaaS":          ["Multi-tenancy", "Stripe Billing", "Microservices"],
    "Cybersecurity": ["Pen Testing", "IAM", "Cryptography"],
    "Cloud":         ["AWS", "Kubernetes", "Terraform"],
    "AI/ML":         ["LLMs", "PyTorch", "RAG Pipelines"],
    "Gaming":        ["Unity", "Unreal Engine", "Game Design"],
    "Automotive":    ["ADAS", "CAN Bus", "Embedded Systems"],
}

_ROLE_SKILL_MAP: dict[str, list[str]] = {
    "Backend Engineer":    ["Python", "FastAPI", "PostgreSQL", "Redis", "Docker"],
    "ML Engineer":         ["Python", "PyTorch", "MLflow", "Kubeflow", "SQL"],
    "Data Scientist":      ["Python", "Pandas", "Scikit-learn", "Spark", "SQL"],
    "Product Analyst":     ["SQL", "Tableau", "A/B Testing", "Excel", "Python"],
    "Full Stack Engineer": ["React", "TypeScript", "Node.js", "FastAPI", "Docker"],
}

_LEVELS = ["Junior", "Mid-Level", "Senior", "Lead", "Principal"]

_LEVEL_EXP: dict[str, tuple[int, int]] = {
    "Junior":    (1, 3),
    "Mid-Level": (3, 6),
    "Senior":    (6, 10),
    "Lead":      (8, 14),
    "Principal": (12, 20),
}

_LOCATIONS = [
    "San Francisco, CA", "New York, NY", "Austin, TX",
    "Seattle, WA", "Remote", "London, UK",
    "Berlin, Germany", "Toronto, Canada",
]

_COMPANIES = [
    "TechStartup", "MegaCorp", "ScaleAI",
    "DevHouse", "InnovateCo", "BuildFast", "DataLabs",
]


def _slug(text: str) -> str:
    return text.lower().replace(" ", "_").replace("/", "_")


# ---------------------------------------------------------------------------
# Domain object builders
# ---------------------------------------------------------------------------

def _build_candidates():
    from app.domain.candidate_twin import (
        CandidateDigitalTwin,
        CandidateTimelineEntry,
        GrowthStage,
    )

    candidates = []
    domain_list = list(_DOMAINS_MAP.keys())
    role_list = list(_ROLE_SKILL_MAP.keys())

    for role_idx, role in enumerate(role_list):
        for i in range(10):
            level = _LEVELS[i % len(_LEVELS)]
            domain = domain_list[(role_idx * 2 + i) % len(domain_list)]
            exp_min, exp_max = _LEVEL_EXP[level]
            years = random.randint(exp_min, exp_max)

            td     = min(100, 30 + years * 5 + random.randint(-5, 10))
            lv     = random.randint(55, 95)
            ldr    = min(100, 20 + years * 4 + random.randint(-5, 10))
            collab = random.randint(65, 95)
            comm   = random.randint(60, 95)
            proj   = min(100, 25 + years * 5 + random.randint(-10, 15))

            if level in ("Junior", "Mid-Level"):
                growth = GrowthStage.BUILDER
            elif level == "Senior":
                growth = GrowthStage.TECHNICAL_SPECIALIST
            elif level == "Lead":
                growth = GrowthStage.EMERGING_LEADER
            else:
                growth = GrowthStage.TECHNICAL_SPECIALIST

            skills = list(_ROLE_SKILL_MAP[role])[:4]
            skills.append(_DOMAINS_MAP[domain][0])

            timeline = []
            for y in range(min(years, 6)):
                company = _COMPANIES[y % len(_COMPANIES)]
                timeline.append(CandidateTimelineEntry(
                    year=2024 - y,
                    event=f"{level} {role} at {company}",
                ))

            candidates.append(CandidateDigitalTwin(
                candidate_id=f"seed_{_slug(role)}_{i:02d}",
                name=f"{level} {role} #{i + 1}",
                email=f"{_slug(level)}.{_slug(role).replace('_', '')}{i + 1}@talentgraph.dev",
                phone=f"+1-555-{100 + role_idx:03d}-{1000 + i:04d}",
                location=_LOCATIONS[i % len(_LOCATIONS)],
                skills=skills,
                projects=[
                    f"Led {domain} platform rebuild (25 pct perf gain)",
                    f"Shipped {role} tooling for distributed teams",
                ],
                domains=[domain],
                timeline=timeline,
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
            ))

    return candidates


def _build_jobs():
    from app.domain.role_dna import RoleDNAProfile, WorkEnvironmentAttributes

    jobs = []
    role_list = list(_ROLE_SKILL_MAP.keys())
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
                required_skills=list(_ROLE_SKILL_MAP[role])[:3],
                preferred_skills=list(_ROLE_SKILL_MAP[role])[3:],
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


# ---------------------------------------------------------------------------
# Main seeder
# ---------------------------------------------------------------------------

def seed(
    candidate_repository,
    role_repository,
    evaluation_pipeline,
    ranking_pipeline,
    explanation_pipeline,
    embedding_pipeline,
    graph_pipeline,
) -> None:
    """
    Idempotent seeder. No-ops if data already exists.
    Populates: candidates, roles, evaluations, rankings,
               explanations, embeddings, graph.
    """
    from app.domain.ranking import HiringPersona

    # ── Guard: skip if already seeded ────────────────────────────────────────
    existing = candidate_repository.list_candidates()
    if existing:
        logger.info("Startup seeder: %d candidates already loaded — skipping.", len(existing))
        return

    logger.info("Startup seeder: repository is empty — seeding demo data...")

    # ── 1. Save roles ─────────────────────────────────────────────────────────
    jobs = _build_jobs()
    for j in jobs:
        role_repository.save(j)
    logger.info("  Loaded %d jobs", len(jobs))

    # ── 2. Save candidates ────────────────────────────────────────────────────
    candidates = _build_candidates()
    for c in candidates:
        candidate_repository.save(c)
    logger.info("  Loaded %d candidates", len(candidates))

    # ── 3. Evaluations ────────────────────────────────────────────────────────
    eval_count = 0
    for j in jobs:
        for c in candidates:
            try:
                evaluation_pipeline.run(role_id=j.role_id, candidate_id=c.candidate_id)
                eval_count += 1
            except Exception as exc:
                logger.debug("  Eval skipped %s/%s: %s", c.candidate_id, j.role_id, exc)
    logger.info("  Loaded evaluations (%d)", eval_count)

    # ── 4. Rankings ───────────────────────────────────────────────────────────
    rank_count = 0
    for j in jobs:
        for persona in (HiringPersona.STARTUP_FOUNDER, HiringPersona.ENTERPRISE_RECRUITER):
            try:
                ranking_pipeline.run(role_id=j.role_id, persona=persona)
                rank_count += 1
            except Exception as exc:
                logger.debug("  Ranking skipped %s/%s: %s", j.role_id, persona, exc)
    logger.info("  Loaded rankings (%d runs)", rank_count)

    # ── 5. Explanations ───────────────────────────────────────────────────────
    exp_count = 0
    primary_job = jobs[0]  # generate explanations for first role only (performance)
    for c in candidates:
        for persona in (HiringPersona.STARTUP_FOUNDER,):
            try:
                explanation_pipeline.run(
                    role_id=primary_job.role_id,
                    candidate_id=c.candidate_id,
                    persona=persona,
                )
                exp_count += 1
            except Exception as exc:
                logger.debug("  Explanation skipped %s: %s", c.candidate_id, exc)
    logger.info("  Loaded explanations (%d)", exp_count)

    # ── 6. Embeddings ─────────────────────────────────────────────────────────
    emb_count = 0
    for c in candidates[:10]:  # first 10 candidates for speed on startup
        try:
            embedding_pipeline.run(
                role_id=primary_job.role_id,
                candidate_id=c.candidate_id,
            )
            emb_count += 1
        except Exception as exc:
            logger.debug("  Embedding skipped %s: %s", c.candidate_id, exc)
    logger.info("  Loaded embeddings (%d)", emb_count)

    # ── 7. Graph ──────────────────────────────────────────────────────────────
    graph_count = 0
    for c in candidates[:5]:  # first 5 for speed
        try:
            graph_pipeline.run(
                role_id=primary_job.role_id,
                candidate_id=c.candidate_id,
            )
            graph_count += 1
        except Exception as exc:
            logger.debug("  Graph skipped %s: %s", c.candidate_id, exc)
    logger.info("  Loaded graph data (%d snapshots)", graph_count)

    logger.info(
        "Startup seeder: DONE — %d candidates, %d jobs, %d evals, %d rankings, "
        "%d explanations, %d embeddings, %d graphs.",
        len(candidates), len(jobs), eval_count, rank_count,
        exp_count, emb_count, graph_count,
    )
