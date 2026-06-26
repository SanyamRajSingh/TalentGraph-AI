from app.domain.ranking import HiringPersona, RankingResult
from app.modules.ranking import RankingService


class RankingPipeline:
    """Orchestrates ranking candidates for a role/persona."""

    def __init__(self, ranking_service: RankingService) -> None:
        self.ranking_service = ranking_service

    def run(self, role_id: str, persona: HiringPersona) -> list[RankingResult]:
        return self.ranking_service.rank(role_id=role_id, persona=persona)
