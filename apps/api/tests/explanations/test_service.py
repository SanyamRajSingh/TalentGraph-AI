from app.domain.evaluation import EvaluationBundle, EvaluatorResult
from app.domain.ranking import HiringPersona, RankingResult
from app.modules.explanations import CounterfactualService, ExplanationService
from app.repositories.memory import InMemoryExplanationRepository

from .test_helpers import candidate, role


def test_explanation_service_generates_and_persists_profile() -> None:
    repository = InMemoryExplanationRepository()
    service = ExplanationService(
        counterfactual_service=CounterfactualService(),
        explanation_repository=repository,
    )
    evaluation = EvaluationBundle(
        evaluation_id="evaluation_explain",
        candidate_id="candidate_explain",
        role_id="role_explain",
        technical=EvaluatorResult(
            score=86,
            confidence=82,
            strengths=["Strong Python and ML alignment."],
            risks=[],
            explanation="Strong technical overlap.",
        ),
        growth=EvaluatorResult(score=78, confidence=80, strengths=["High learning velocity."]),
        domain=EvaluatorResult(score=52, confidence=78, risks=["Limited domain exposure."]),
        culture=EvaluatorResult(score=64, confidence=76, risks=["Communication evidence is thin."]),
        overall_match=71,
        overall_confidence=79,
    )
    ranking = RankingResult(
        candidate_id="candidate_explain",
        role_id="role_explain",
        rank=2,
        persona=HiringPersona.STARTUP_FOUNDER,
        score=73,
        confidence=79,
        evaluation_id="evaluation_explain",
    )

    profile = service.generate(role(), candidate(), evaluation, ranking)

    assert profile.ranking_position == 2
    assert "Strong Python and ML alignment." in profile.strengths
    assert any("Limited domain exposure" in risk for risk in profile.risks)
    assert profile.counterfactuals
    assert repository.get_by_candidate_id("candidate_explain") == profile
