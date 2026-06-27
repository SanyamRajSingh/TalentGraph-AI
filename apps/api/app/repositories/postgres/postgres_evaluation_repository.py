"""PostgreSQL implementation of EvaluationRepository."""

from sqlalchemy.orm import Session

from app.db.models import EvaluationRow
from app.domain.evaluation import EvaluationBundle
from app.repositories.evaluation_repository import EvaluationRepository


class PostgresEvaluationRepository(EvaluationRepository):
    """PostgreSQL-backed evaluation repository using SQLAlchemy ORM."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, evaluation: EvaluationBundle) -> EvaluationBundle:
        existing = (
            self.session.query(EvaluationRow)
            .filter_by(evaluation_id=evaluation.evaluation_id)
            .first()
        )
        payload = evaluation.model_dump(mode="json")
        if existing:
            existing.overall_match = evaluation.overall_match
            existing.overall_confidence = evaluation.overall_confidence
            existing.payload = payload
        else:
            row = EvaluationRow(
                evaluation_id=evaluation.evaluation_id,
                candidate_id=evaluation.candidate_id,
                role_id=evaluation.role_id,
                overall_match=evaluation.overall_match,
                overall_confidence=evaluation.overall_confidence,
                payload=payload,
            )
            self.session.add(row)
        self.session.commit()
        return evaluation

    def get(self, evaluation_id: str) -> EvaluationBundle | None:
        row = (
            self.session.query(EvaluationRow)
            .filter_by(evaluation_id=evaluation_id)
            .first()
        )
        if row is None:
            return None
        return EvaluationBundle.model_validate(row.payload)

    def list_by_role_id(self, role_id: str) -> list[EvaluationBundle]:
        rows = (
            self.session.query(EvaluationRow)
            .filter_by(role_id=role_id)
            .order_by(EvaluationRow.created_at.desc())
            .all()
        )
        return [EvaluationBundle.model_validate(r.payload) for r in rows]
