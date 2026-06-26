from app.domain.candidate_twin import CandidateDigitalTwin
from app.domain.evaluation import EvaluatorResult
from app.domain.role_dna import RoleDNAProfile
from app.modules.evaluators.utils import average, clamp_score


class CultureEvaluator:
    """Evaluates communication, ownership, collaboration, and ambiguity fit."""

    def evaluate(self, role: RoleDNAProfile, candidate: CandidateDigitalTwin) -> EvaluatorResult:
        communication = 100 - abs(role.communication - candidate.communication)
        ownership = 100 - abs(role.ownership - candidate.ownership)
        collaboration = 100 - abs(role.collaboration - candidate.collaboration)
        ambiguity = 100 - abs(role.ambiguity_tolerance - candidate.ownership)
        score = clamp_score(communication * 0.25 + ownership * 0.30 + collaboration * 0.25 + ambiguity * 0.20)
        confidence = average([candidate.confidence, communication, ownership, collaboration])

        strengths = []
        risks = []
        if ownership >= 75:
            strengths.append("Ownership signal aligns with the role expectation.")
        if communication >= 75:
            strengths.append("Communication signal aligns with the role expectation.")
        if collaboration >= 75:
            strengths.append("Collaboration signal aligns with the role expectation.")
        if ambiguity < 65:
            risks.append("Ambiguity tolerance evidence may not match the role environment.")
        if communication < 65:
            risks.append("Communication evidence may need validation.")

        return EvaluatorResult(score=score, confidence=confidence, strengths=strengths, risks=risks)
