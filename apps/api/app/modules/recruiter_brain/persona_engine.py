from app.domain.evaluation import EvaluationBundle
from app.domain.ranking import HiringPersona


PERSONA_WEIGHTS: dict[HiringPersona, dict[str, int]] = {
    HiringPersona.STARTUP_FOUNDER: {
        "technical": 20,
        "growth": 35,
        "domain": 15,
        "culture": 30,
    },
    HiringPersona.ENTERPRISE_RECRUITER: {
        "technical": 40,
        "growth": 20,
        "domain": 25,
        "culture": 15,
    },
    HiringPersona.RESEARCH_TEAM: {
        "technical": 45,
        "growth": 20,
        "domain": 30,
        "culture": 5,
    },
}


class PersonaEngine:
    """Applies recruiter philosophy to evaluation scores."""

    def get_weights(self, persona: HiringPersona) -> dict[str, int]:
        return PERSONA_WEIGHTS[persona]

    def score(self, evaluation: EvaluationBundle, persona: HiringPersona) -> int:
        weights = self.get_weights(persona)
        total = sum(weights.values())
        if not all([evaluation.technical, evaluation.growth, evaluation.domain, evaluation.culture]):
            return 0
        weighted = (
            evaluation.technical.score * weights["technical"]
            + evaluation.growth.score * weights["growth"]
            + evaluation.domain.score * weights["domain"]
            + evaluation.culture.score * weights["culture"]
        )
        return max(0, min(100, int(round(weighted / total))))
