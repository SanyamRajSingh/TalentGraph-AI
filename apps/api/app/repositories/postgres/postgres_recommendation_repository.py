from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.models import RecommendationRow
from app.domain.recommendation import RecommendationResult
from app.repositories.recommendation_repository import RecommendationRepository


class PostgresRecommendationRepository(RecommendationRepository):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def save(self, recommendation: RecommendationResult) -> RecommendationResult:
        with self.session_factory() as session:
            row = session.execute(
                select(RecommendationRow)
                .where(RecommendationRow.candidate_id == recommendation.candidate_id)
                .where(RecommendationRow.role_id == recommendation.role_id)
            ).scalar_one_or_none()
            if row is None:
                row = RecommendationRow(
                    candidate_id=recommendation.candidate_id,
                    role_id=recommendation.role_id,
                    label=recommendation.label.value,
                    payload=recommendation.model_dump(mode="json"),
                )
                session.add(row)
            else:
                row.label = recommendation.label.value
                row.payload = recommendation.model_dump(mode="json")
            session.commit()
            return recommendation

    def get(self, candidate_id: str, role_id: str) -> RecommendationResult | None:
        with self.session_factory() as session:
            row = session.execute(
                select(RecommendationRow)
                .where(RecommendationRow.candidate_id == candidate_id)
                .where(RecommendationRow.role_id == role_id)
            ).scalar_one_or_none()
            if row is None:
                return None
            return RecommendationResult.model_validate(row.payload)
