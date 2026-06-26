from app.domain.explanation import CounterfactualSuggestion
from app.domain.ranking import RankingResult


class CounterfactualEngine:
    """Suggests candidate improvements that could change ranking outcomes.

    TODO: Implement counterfactual generation in the explanations increment.
    """

    def generate(self, ranking: RankingResult) -> list[CounterfactualSuggestion]:
        raise NotImplementedError("Counterfactuals are not implemented in the architecture pass.")
