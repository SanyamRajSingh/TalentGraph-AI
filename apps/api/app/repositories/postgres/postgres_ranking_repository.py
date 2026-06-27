"""PostgreSQL implementation of RankingRepository."""

from sqlalchemy.orm import Session

from app.db.models import RankingRow
from app.domain.ranking import RankingResult
from app.repositories.ranking_repository import RankingRepository


class PostgresRankingRepository(RankingRepository):
    """PostgreSQL-backed ranking repository using SQLAlchemy ORM."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def save_many(self, rankings: list[RankingResult]) -> list[RankingResult]:
        for ranking in rankings:
            # Delete existing ranking for same role/candidate/persona to avoid duplicates
            self.session.query(RankingRow).filter_by(
                candidate_id=ranking.candidate_id,
                role_id=ranking.role_id,
                persona=str(ranking.persona),
            ).delete()
            row = RankingRow(
                candidate_id=ranking.candidate_id,
                role_id=ranking.role_id,
                persona=str(ranking.persona),
                rank=ranking.rank,
                score=ranking.score,
                confidence=ranking.confidence,
                evaluation_id=ranking.evaluation_id,
                payload=ranking.model_dump(mode="json"),
            )
            self.session.add(row)
        self.session.commit()
        return rankings

    def list_by_role_id(self, role_id: str, persona: str | None = None) -> list[RankingResult]:
        query = self.session.query(RankingRow).filter_by(role_id=role_id)
        if persona is not None:
            query = query.filter_by(persona=persona)
        rows = query.order_by(RankingRow.rank).all()
        return [RankingResult.model_validate(r.payload) for r in rows]
