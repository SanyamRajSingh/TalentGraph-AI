from app.domain.candidate_twin import CandidateDigitalTwin
from app.domain.role_dna import RoleDNAProfile
from app.modules.embeddings import EmbeddingFoundationService, LocalEmbeddingProvider, SummaryService


def test_summary_service_generates_deterministic_summaries() -> None:
    role = _role()
    candidate = _candidate()
    service = SummaryService()

    role_summary = service.role_summary(role)
    candidate_summary = service.candidate_summary(candidate)

    assert role.role_title in role_summary.text
    assert candidate.name in candidate_summary.text
    assert role_summary.id == "summary:role:role_embed"
    assert candidate_summary.id == "summary:candidate:candidate_embed"


def test_local_embedding_provider_is_deterministic() -> None:
    provider = LocalEmbeddingProvider(dimensions=8)

    first = provider.embed("Python skill")
    second = provider.embed("Python skill")

    assert first == second
    assert len(first) == 8


def test_embedding_foundation_generates_summary_skill_and_project_vectors() -> None:
    collection = EmbeddingFoundationService(
        summary_service=SummaryService(),
        embedding_provider=LocalEmbeddingProvider(dimensions=8),
    ).generate(role_dna=_role(), candidate_twin=_candidate())

    kinds = {embedding.kind for embedding in collection.embeddings}
    assert "role_summary" in kinds
    assert "candidate_summary" in kinds
    assert "skill" in kinds
    assert "project" in kinds
    assert all(len(embedding.vector) == 8 for embedding in collection.embeddings)


def _role() -> RoleDNAProfile:
    return RoleDNAProfile(
        role_id="role_embed",
        role_title="ML Engineer",
        domain="Machine Learning",
        seniority="Senior",
        role_archetype="Analytical Builder",
        fingerprint="Builder-Researcher Hybrid",
        required_skills=["Python", "Machine Learning"],
        preferred_skills=["Statistics"],
        skill_importance={"Python": 40, "Machine Learning": 40, "Statistics": 20},
        technical_depth=92,
        problem_solving=86,
        communication=70,
        ownership=80,
        leadership=60,
        learning_agility=90,
        ambiguity_tolerance=75,
        collaboration=74,
        startup_vs_enterprise_environment=55,
    )


def _candidate() -> CandidateDigitalTwin:
    return CandidateDigitalTwin(
        candidate_id="candidate_embed",
        name="Nikhil Mehta",
        skills=["Python", "Machine Learning"],
        projects=["Built ML Pipeline"],
        domains=["Machine Learning"],
        technical_depth=88,
        learning_velocity=82,
        ownership=76,
        project_complexity=84,
    )
