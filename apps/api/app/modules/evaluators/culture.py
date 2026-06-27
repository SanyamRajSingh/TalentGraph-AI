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
        evidence = []
        missing_signals = []
        
        if ownership >= 75:
            strengths.append("Ownership signal aligns with the role expectation.")
            evidence.append(f"Ownership score is {candidate.ownership}/100.")
        if communication >= 75:
            strengths.append("Communication signal aligns with the role expectation.")
            evidence.append(f"Communication score is {candidate.communication}/100.")
        if collaboration >= 75:
            strengths.append("Collaboration signal aligns with the role expectation.")
            evidence.append(f"Collaboration score is {candidate.collaboration}/100.")
        if ambiguity < 65:
            risks.append("Ambiguity tolerance evidence may not match the role environment.")
            missing_signals.append("Experience navigating ambiguity")
        if communication < 65:
            risks.append("Communication evidence may need validation.")
            missing_signals.append("Clear communication examples")

        ramp_up_estimate = "Culturally aligned (fast integration)" if score >= 75 else "May require culture onboarding"

        return EvaluatorResult(
            score=score, 
            confidence=confidence, 
            strengths=strengths, 
            risks=risks,
            evidence=evidence,
            missing_signals=missing_signals,
            ramp_up_estimate=ramp_up_estimate
        )
