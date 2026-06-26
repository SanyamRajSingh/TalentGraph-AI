from app.domain.candidate_twin import CandidateDigitalTwin, GrowthStage
from app.domain.role_dna import RoleDNAProfile
from app.modules.evaluators import (
    CultureEvaluator,
    DomainEvaluator,
    GrowthEvaluator,
    TechnicalEvaluator,
)


def test_technical_evaluator_scores_skill_and_depth_alignment() -> None:
    result = TechnicalEvaluator().evaluate(_role(), _candidate())

    assert 0 <= result.score <= 100
    assert result.score >= 70
    assert result.strengths


def test_growth_evaluator_scores_stage_and_trajectory() -> None:
    result = GrowthEvaluator().evaluate(_role(), _candidate())

    assert 0 <= result.score <= 100
    assert "Growth stage" in result.strengths[0]


def test_domain_evaluator_uses_ontology_adjacency() -> None:
    candidate = _candidate()
    candidate.skills = ["FastAPI"]
    candidate.technologies = ["FastAPI"]
    candidate.domains = ["Backend Systems"]
    role = _role()
    role.required_skills = ["Python"]

    result = DomainEvaluator().evaluate(role, candidate)

    assert result.score > 50
    assert any("Ontology-adjacent" in strength for strength in result.strengths)


def test_culture_evaluator_scores_work_style_alignment() -> None:
    result = CultureEvaluator().evaluate(_role(), _candidate())

    assert 0 <= result.score <= 100
    assert result.confidence > 0


def _role() -> RoleDNAProfile:
    return RoleDNAProfile(
        role_id="role_eval",
        role_title="Backend Engineer",
        domain="Backend Systems",
        seniority="Senior",
        role_archetype="Systems Builder",
        fingerprint="Builder",
        required_skills=["Python", "FastAPI"],
        preferred_skills=["SQL"],
        skill_importance={"Python": 40, "FastAPI": 40, "SQL": 20},
        technical_depth=85,
        problem_solving=82,
        communication=70,
        ownership=80,
        leadership=65,
        learning_agility=75,
        ambiguity_tolerance=70,
        collaboration=72,
        startup_vs_enterprise_environment=55,
    )


def _candidate() -> CandidateDigitalTwin:
    return CandidateDigitalTwin(
        candidate_id="candidate_eval",
        name="Ada Backend",
        skills=["Python", "FastAPI", "SQL"],
        technologies=["Python", "PostgreSQL"],
        projects=["Built API Platform"],
        domains=["Backend Systems"],
        technical_depth=82,
        learning_velocity=78,
        leadership=62,
        ownership=82,
        communication=72,
        project_complexity=80,
        collaboration=74,
        consistency=76,
        growth_stage=GrowthStage.BUILDER,
        confidence=84,
    )
