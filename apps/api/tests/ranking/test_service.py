from app.domain.evaluation import EvaluationBundle, EvaluatorResult
from app.domain.ranking import HiringPersona
from app.modules.ranking import RankingService
from app.repositories.memory import InMemoryEvaluationRepository, InMemoryRankingRepository


def test_ranking_service_sorts_descending_and_assigns_rank() -> None:
    evaluation_repository = InMemoryEvaluationRepository()
    ranking_repository = InMemoryRankingRepository()
    evaluation_repository.save(_evaluation("candidate_low", technical=50, growth=50, domain=50, culture=50))
    evaluation_repository.save(_evaluation("candidate_high", technical=90, growth=90, domain=80, culture=85))

    rankings = RankingService(evaluation_repository, ranking_repository).rank(
        role_id="role_rank",
        persona=HiringPersona.STARTUP_FOUNDER,
    )

    assert [ranking.candidate_id for ranking in rankings] == ["candidate_high", "candidate_low"]
    assert [ranking.rank for ranking in rankings] == [1, 2]
    assert ranking_repository.list_by_role_id("role_rank", persona="startup_founder") == rankings


def test_ranking_service_tie_breaks_by_confidence_then_candidate_id() -> None:
    evaluation_repository = InMemoryEvaluationRepository()
    ranking_repository = InMemoryRankingRepository()
    evaluation_repository.save(_evaluation("candidate_b", 80, 80, 80, 80, confidence=70))
    evaluation_repository.save(_evaluation("candidate_a", 80, 80, 80, 80, confidence=90))
    evaluation_repository.save(_evaluation("candidate_c", 80, 80, 80, 80, confidence=90))

    rankings = RankingService(evaluation_repository, ranking_repository).rank(
        role_id="role_rank",
        persona=HiringPersona.RESEARCH_TEAM,
    )

    assert [ranking.candidate_id for ranking in rankings] == ["candidate_a", "candidate_c", "candidate_b"]


def _evaluation(
    candidate_id: str,
    technical: int,
    growth: int,
    domain: int,
    culture: int,
    confidence: int = 80,
) -> EvaluationBundle:
    return EvaluationBundle(
        candidate_id=candidate_id,
        role_id="role_rank",
        technical=EvaluatorResult(score=technical, confidence=confidence),
        growth=EvaluatorResult(score=growth, confidence=confidence),
        domain=EvaluatorResult(score=domain, confidence=confidence),
        culture=EvaluatorResult(score=culture, confidence=confidence),
        overall_confidence=confidence,
    )
