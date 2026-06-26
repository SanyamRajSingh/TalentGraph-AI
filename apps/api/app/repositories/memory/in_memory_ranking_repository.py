from app.domain.ranking import RankingResult
from app.repositories.ranking_repository import RankingRepository


class InMemoryRankingRepository(RankingRepository):
    """Process-local ranking repository for tests and demo runs."""

    def __init__(self) -> None:
        self._rankings: dict[tuple[str, str], list[RankingResult]] = {}

    def save_many(self, rankings: list[RankingResult]) -> list[RankingResult]:
        if not rankings:
            return []
        key = (rankings[0].role_id, rankings[0].persona.value)
        self._rankings[key] = rankings
        return rankings

    def list_by_role_id(self, role_id: str, persona: str | None = None) -> list[RankingResult]:
        if persona:
            return self._rankings.get((role_id, persona), [])
        results: list[RankingResult] = []
        for (stored_role_id, _persona), rankings in self._rankings.items():
            if stored_role_id == role_id:
                results.extend(rankings)
        return sorted(results, key=lambda ranking: (ranking.persona.value, ranking.rank))
