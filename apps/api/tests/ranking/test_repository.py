from app.domain.ranking import HiringPersona, RankingResult
from app.repositories.memory import InMemoryRankingRepository


def test_memory_ranking_repository_persists_by_role_and_persona() -> None:
    repository = InMemoryRankingRepository()
    rankings = [
        RankingResult(
            candidate_id="candidate_1",
            role_id="role_1",
            rank=1,
            persona=HiringPersona.STARTUP_FOUNDER,
            score=88,
            confidence=80,
            evaluation_id="evaluation_1",
        )
    ]

    repository.save_many(rankings)

    assert repository.list_by_role_id("role_1", persona="startup_founder") == rankings
    assert repository.list_by_role_id("role_1") == rankings
