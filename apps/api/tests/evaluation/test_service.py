from app.domain.candidate_twin import CandidateDigitalTwin, GrowthStage
from app.domain.evaluation import EvaluatorResult
from app.domain.role_dna import RoleDNAProfile
from app.modules.evaluators import EvaluationService


class FixedEvaluator:
    def __init__(self, score: int, confidence: int) -> None:
        self.score = score
        self.confidence = confidence

    def evaluate(self, role: RoleDNAProfile, candidate: CandidateDigitalTwin) -> EvaluatorResult:
        return EvaluatorResult(score=self.score, confidence=self.confidence)


def test_evaluation_service_computes_weighted_overall_match_and_confidence() -> None:
    service = EvaluationService(
        technical_evaluator=FixedEvaluator(90, 80),
        growth_evaluator=FixedEvaluator(80, 70),
        domain_evaluator=FixedEvaluator(70, 60),
        culture_evaluator=FixedEvaluator(60, 50),
    )

    bundle = service.evaluate(_role(), _candidate())

    assert bundle.overall_match == 79
    assert bundle.overall_confidence == 65
    assert bundle.technical is not None
    assert bundle.growth is not None
    assert bundle.domain is not None
    assert bundle.culture is not None


def _role() -> RoleDNAProfile:
    return RoleDNAProfile(
        role_id="role_service",
        role_title="Data Scientist",
        domain="Machine Learning",
        seniority="Senior",
        role_archetype="Analytical Builder",
        fingerprint="Researcher",
        required_skills=["Python"],
        technical_depth=80,
        problem_solving=80,
        communication=70,
        ownership=70,
        leadership=60,
        learning_agility=80,
        ambiguity_tolerance=70,
        collaboration=70,
        startup_vs_enterprise_environment=60,
    )


def _candidate() -> CandidateDigitalTwin:
    return CandidateDigitalTwin(
        candidate_id="candidate_service",
        name="Service Candidate",
        skills=["Python"],
        growth_stage=GrowthStage.BUILDER,
    )
