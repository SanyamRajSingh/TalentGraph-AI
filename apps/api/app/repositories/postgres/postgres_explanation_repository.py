"""PostgreSQL implementation of ExplanationRepository."""

from sqlalchemy.orm import Session

from app.db.models import ExplanationRow
from app.domain.explanation import ExplanationProfile
from app.repositories.explanation_repository import ExplanationRepository


class PostgresExplanationRepository(ExplanationRepository):
    """PostgreSQL-backed explanation repository using SQLAlchemy ORM."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, profile: ExplanationProfile) -> ExplanationProfile:
        # Delete any previous explanation for this candidate to keep latest only
        self.session.query(ExplanationRow).filter_by(
            candidate_id=profile.candidate_id, role_id=profile.role_id
        ).delete()
        row = ExplanationRow(
            candidate_id=profile.candidate_id,
            role_id=profile.role_id,
            ranking_position=profile.ranking_position,
            payload=profile.model_dump(mode="json"),
        )
        self.session.add(row)
        self.session.commit()
        return profile

    def get_by_candidate_id(self, candidate_id: str) -> ExplanationProfile | None:
        row = (
            self.session.query(ExplanationRow)
            .filter_by(candidate_id=candidate_id)
            .order_by(ExplanationRow.created_at.desc())
            .first()
        )
        if row is None:
            return None
        return ExplanationProfile.model_validate(row.payload)
