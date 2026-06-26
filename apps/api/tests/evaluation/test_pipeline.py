from app.domain.candidate_twin import CandidateDigitalTwin
from app.domain.evaluation import EvaluationBundle
from app.domain.role_dna import RoleDNAProfile
from app.pipelines.evaluation_pipeline import EvaluationPipeline
from app.repositories.memory import (
    InMemoryCandidateRepository,
    InMemoryEvaluationRepository,
    InMemoryRoleDNARepository,
)


class MockEvaluationService:
    def evaluate(self, role: RoleDNAProfile, candidate: CandidateDigitalTwin) -> EvaluationBundle:
        return EvaluationBundle(
            candidate_id=candidate.candidate_id,
            role_id=role.role_id,
            overall_match=77,
            overall_confidence=70,
        )


def test_evaluation_pipeline_loads_inputs_runs_service_and_persists() -> None:
    role_repository = InMemoryRoleDNARepository()
    candidate_repository = InMemoryCandidateRepository()
    evaluation_repository = InMemoryEvaluationRepository()
    role_repository.save(_role())
    candidate_repository.save(CandidateDigitalTwin(candidate_id="candidate_pipe", name="Pipe Candidate"))

    bundle = EvaluationPipeline(
        evaluation_service=MockEvaluationService(),
        evaluation_repository=evaluation_repository,
        role_repository=role_repository,
        candidate_repository=candidate_repository,
    ).run(role_id="role_pipe", candidate_id="candidate_pipe")

    assert bundle.overall_match == 77
    assert evaluation_repository.get(bundle.evaluation_id) == bundle


def _role() -> RoleDNAProfile:
    return RoleDNAProfile(
        role_id="role_pipe",
        role_title="Backend Engineer",
        domain="Backend Systems",
        seniority="Senior",
        role_archetype="Systems Builder",
        fingerprint="Builder",
        required_skills=["Python"],
        technical_depth=80,
        problem_solving=80,
        communication=70,
        ownership=70,
        leadership=60,
        learning_agility=70,
        ambiguity_tolerance=70,
        collaboration=70,
        startup_vs_enterprise_environment=50,
    )
