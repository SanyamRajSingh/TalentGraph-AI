from app.domain.candidate_twin import CandidateDigitalTwin
from app.domain.role_dna import RoleDNAProfile


def role() -> RoleDNAProfile:
    return RoleDNAProfile(
        role_id="role_explain",
        role_title="Fintech ML Engineer",
        domain="fintech",
        seniority="senior",
        role_archetype="ML Product Builder",
        fingerprint="fintech-ml-product-builder",
        required_skills=["Python", "Machine Learning", "Distributed Systems"],
        preferred_skills=["SQL"],
        technical_depth=82,
        problem_solving=78,
        communication=76,
        ownership=74,
        leadership=70,
        learning_agility=72,
        ambiguity_tolerance=70,
        collaboration=72,
        startup_vs_enterprise_environment=64,
        reasoning=["Role needs applied ML and fintech context."],
        confidence=80,
    )


def candidate() -> CandidateDigitalTwin:
    return CandidateDigitalTwin(
        candidate_id="candidate_explain",
        name="Mira ML",
        skills=["Python", "Machine Learning"],
        projects=["Built churn model"],
        experiences=["ML Engineer"],
        domains=["analytics"],
        technical_depth=78,
        learning_velocity=76,
        leadership=58,
        ownership=75,
        communication=60,
        project_complexity=72,
        collaboration=68,
        consistency=70,
        reasoning=["Candidate has ML project evidence."],
        confidence=78,
    )
