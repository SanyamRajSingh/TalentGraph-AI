from app.domain.evaluation import EvaluationBundle
from app.repositories.evaluation_repository import EvaluationRepository


class InMemoryEvaluationRepository(EvaluationRepository):
    """Process-local evaluation repository for tests and demo runs."""

    def __init__(self) -> None:
        self._evaluations: dict[str, EvaluationBundle] = {}

    def save(self, evaluation: EvaluationBundle) -> EvaluationBundle:
        self._evaluations[evaluation.evaluation_id] = evaluation
        return evaluation

    def get(self, evaluation_id: str) -> EvaluationBundle | None:
        return self._evaluations.get(evaluation_id)

    def list_by_role_id(self, role_id: str) -> list[EvaluationBundle]:
        return [
            evaluation
            for evaluation in self._evaluations.values()
            if evaluation.role_id == role_id
        ]
