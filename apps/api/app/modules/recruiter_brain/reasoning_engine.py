from app.domain.evaluation import EvaluationBundle
from app.domain.explanation import CandidateExplanation


class ReasoningEngine:
    """Generates recruiter-readable explanations from evaluator results.

    TODO: Implement explanation synthesis after evaluator outputs exist.
    """

    def explain(self, evaluation: EvaluationBundle) -> CandidateExplanation:
        raise NotImplementedError("Reasoning generation is not implemented in the architecture pass.")
