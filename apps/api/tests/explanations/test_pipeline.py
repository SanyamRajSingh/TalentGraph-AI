import pytest

from app.domain.evaluation import EvaluationBundle, EvaluatorResult
from app.domain.ranking import HiringPersona, RankingResult
from app.modules.explanations import CounterfactualService, ExplanationService
from app.pipelines.explanation_pipeline import ExplanationPipeline
from app.repositories.memory import (
    InMemoryCandidateRepository,
    InMemoryEvaluationRepository,
    InMemoryExplanationRepository,
    InMemoryRankingRepository,
    InMemoryRoleDNARepository,
)

from .test_helpers import candidate, role


def test_explanation_pipeline_loads_context_and_returns_profile() -> None:
    role_repository = InMemoryRoleDNARepository()
    candidate_repository = InMemoryCandidateRepository()
    evaluation_repository = InMemoryEvaluationRepository()
    ranking_repository = InMemoryRankingRepository()
    explanation_repository = InMemoryExplanationRepository()
    role_repository.save(role())
    candidate_repository.save(candidate())
    evaluation_repository.save(_evaluation())
    ranking_repository.save_many([_ranking()])

    pipeline = ExplanationPipeline(
        explanation_service=ExplanationService(CounterfactualService(), explanation_repository),
        role_repository=role_repository,
        candidate_repository=candidate_repository,
        evaluation_repository=evaluation_repository,
        ranking_repository=ranking_repository,
    )

    profile = pipeline.run(
        role_id="role_explain",
        candidate_id="candidate_explain",
        persona=HiringPersona.STARTUP_FOUNDER,
    )

    assert profile.candidate_id == "candidate_explain"
    assert profile.ranking_position == 1
    assert profile.counterfactuals


def test_explanation_pipeline_requires_existing_ranking() -> None:
    role_repository = InMemoryRoleDNARepository()
    candidate_repository = InMemoryCandidateRepository()
    evaluation_repository = InMemoryEvaluationRepository()
    ranking_repository = InMemoryRankingRepository()
    explanation_repository = InMemoryExplanationRepository()
    role_repository.save(role())
    candidate_repository.save(candidate())
    evaluation_repository.save(_evaluation())

    pipeline = ExplanationPipeline(
        explanation_service=ExplanationService(CounterfactualService(), explanation_repository),
        role_repository=role_repository,
        candidate_repository=candidate_repository,
        evaluation_repository=evaluation_repository,
        ranking_repository=ranking_repository,
    )

    with pytest.raises(ValueError, match="Ranking"):
        pipeline.run(role_id="role_explain", candidate_id="candidate_explain")


def _evaluation() -> EvaluationBundle:
    return EvaluationBundle(
        evaluation_id="evaluation_explain",
        candidate_id="candidate_explain",
        role_id="role_explain",
        technical=EvaluatorResult(score=80, confidence=80),
        growth=EvaluatorResult(score=74, confidence=80),
        domain=EvaluatorResult(score=48, confidence=80),
        culture=EvaluatorResult(score=62, confidence=80),
        overall_match=66,
        overall_confidence=80,
    )


def _ranking() -> RankingResult:
    return RankingResult(
        candidate_id="candidate_explain",
        role_id="role_explain",
        rank=1,
        persona=HiringPersona.STARTUP_FOUNDER,
        score=68,
        confidence=80,
        evaluation_id="evaluation_explain",
    )
