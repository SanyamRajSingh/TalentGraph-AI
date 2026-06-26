from sqlalchemy.orm import Session

from app.domain.evaluation import EvaluationBundle
from app.repositories.evaluation_repository import EvaluationRepository


class PostgresEvaluationRepository(EvaluationRepository):
    """PostgreSQL evaluation repository skeleton for future persistence hardening."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, evaluation: EvaluationBundle) -> EvaluationBundle:
        raise NotImplementedError("PostgreSQL evaluation persistence is not implemented in Module 4.")

    def get(self, evaluation_id: str) -> EvaluationBundle | None:
        raise NotImplementedError("PostgreSQL evaluation lookup is not implemented in Module 4.")

    def list_by_role_id(self, role_id: str) -> list[EvaluationBundle]:
        raise NotImplementedError("PostgreSQL evaluation listing is not implemented in Module 4.")
