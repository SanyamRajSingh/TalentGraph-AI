from app.domain.evaluation import EvaluationBundle, EvaluatorResult
from app.modules.explanations import CounterfactualService

from .test_helpers import candidate, role


def test_counterfactuals_are_derived_from_lowest_score_gaps() -> None:
    evaluation = EvaluationBundle(
        candidate_id="candidate_explain",
        role_id="role_explain",
        technical=EvaluatorResult(score=82, confidence=80),
        growth=EvaluatorResult(score=62, confidence=80),
        domain=EvaluatorResult(score=45, confidence=80),
        culture=EvaluatorResult(score=58, confidence=80),
        overall_match=60,
        overall_confidence=80,
    )

    suggestions = CounterfactualService().generate(role(), candidate(), evaluation)

    assert 1 <= len(suggestions) <= 3
    assert suggestions[0] == "Increase domain exposure to fintech through projects, products, or applied case work."
    assert any("communication evidence" in suggestion for suggestion in suggestions)
