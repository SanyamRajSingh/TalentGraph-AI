from sqlalchemy.orm import Session

from app.domain.explanation import ExplanationProfile
from app.repositories.explanation_repository import ExplanationRepository


class PostgresExplanationRepository(ExplanationRepository):
    """Future PostgreSQL-backed explanation repository boundary."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, profile: ExplanationProfile) -> ExplanationProfile:
        raise NotImplementedError("PostgreSQL explanation persistence is not implemented in Module 6.")

    def get_by_candidate_id(self, candidate_id: str) -> ExplanationProfile | None:
        raise NotImplementedError("PostgreSQL explanation lookup is not implemented in Module 6.")
