from app.domain.evaluation import EvaluationBundle
from app.domain.ranking import RankingResult


class ScoreCalculator:
    """Calculates match and success-potential scores.

    TODO: Implement deterministic formulas after ranking logic is approved.
    """

    def calculate_success_score(self, evaluation: EvaluationBundle) -> int:
        raise NotImplementedError("Success scoring is not implemented in the architecture pass.")

    def calculate_ranking_score(self, evaluation: EvaluationBundle) -> RankingResult:
        raise NotImplementedError("Ranking scoring is not implemented in the architecture pass.")
