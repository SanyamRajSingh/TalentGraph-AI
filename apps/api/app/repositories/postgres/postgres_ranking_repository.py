from sqlalchemy.orm import Session

from app.domain.ranking import RankingResult
from app.repositories.ranking_repository import RankingRepository


class PostgresRankingRepository(RankingRepository):
    """PostgreSQL ranking repository skeleton for future persistence hardening."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def save_many(self, rankings: list[RankingResult]) -> list[RankingResult]:
        raise NotImplementedError("PostgreSQL ranking persistence is not implemented in Module 5.")

    def list_by_role_id(self, role_id: str, persona: str | None = None) -> list[RankingResult]:
        raise NotImplementedError("PostgreSQL ranking lookup is not implemented in Module 5.")
