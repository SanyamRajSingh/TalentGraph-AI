from app.domain.evaluation import EvaluationBundle, EvaluatorResult
from app.domain.ranking import HiringPersona
from app.modules.recruiter_brain.persona_engine import PersonaEngine


def test_persona_weights_are_canonical() -> None:
    engine = PersonaEngine()

    assert engine.get_weights(HiringPersona.STARTUP_FOUNDER) == {
        "technical": 20,
        "growth": 35,
        "domain": 15,
        "culture": 30,
    }
    assert engine.get_weights(HiringPersona.ENTERPRISE_RECRUITER)["technical"] == 40
    assert engine.get_weights(HiringPersona.RESEARCH_TEAM)["domain"] == 30


def test_persona_engine_scores_weighted_dimensions() -> None:
    evaluation = EvaluationBundle(
        candidate_id="candidate_a",
        role_id="role_a",
        technical=EvaluatorResult(score=100, confidence=80),
        growth=EvaluatorResult(score=50, confidence=80),
        domain=EvaluatorResult(score=50, confidence=80),
        culture=EvaluatorResult(score=50, confidence=80),
    )

    assert PersonaEngine().score(evaluation, HiringPersona.ENTERPRISE_RECRUITER) == 70
