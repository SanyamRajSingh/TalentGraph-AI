from abc import ABC, abstractmethod

from app.domain.evaluation import EvaluationBundle


class EvaluationRepository(ABC):
    """Persistence contract for evaluator outputs."""

    @abstractmethod
    def save(self, evaluation: EvaluationBundle) -> EvaluationBundle:
        """Persist evaluator outputs for one candidate-role comparison."""

    @abstractmethod
    def get(self, evaluation_id: str) -> EvaluationBundle | None:
        """Fetch evaluator outputs by id."""

    @abstractmethod
    def list_by_role_id(self, role_id: str) -> list[EvaluationBundle]:
        """List evaluator outputs for a role."""
