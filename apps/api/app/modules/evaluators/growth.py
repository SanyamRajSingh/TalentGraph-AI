from app.domain.candidate_twin import CandidateDigitalTwin, GrowthStage
from app.domain.evaluation import EvaluatorResult
from app.domain.role_dna import RoleDNAProfile
from app.modules.evaluators.utils import average, clamp_score


GROWTH_STAGE_SCORES = {
    GrowthStage.EXPLORER: 55,
    GrowthStage.BUILDER: 75,
    GrowthStage.EMERGING_LEADER: 88,
    GrowthStage.TECHNICAL_SPECIALIST: 82,
    GrowthStage.RESEARCHER: 80,
    GrowthStage.OPERATOR: 74,
    GrowthStage.HYBRID: 84,
}


class GrowthEvaluator:
    """Evaluates learning trajectory, consistency, and leadership signals."""

    def evaluate(self, role: RoleDNAProfile, candidate: CandidateDigitalTwin) -> EvaluatorResult:
        stage_score = GROWTH_STAGE_SCORES[candidate.growth_stage]
        leadership_alignment = 100 - abs(role.leadership - candidate.leadership)
        score = clamp_score(
            candidate.learning_velocity * 0.35
            + stage_score * 0.25
            + candidate.consistency * 0.25
            + leadership_alignment * 0.15
        )
        confidence = average([candidate.confidence, candidate.consistency, stage_score])

        strengths = [
            f"Growth stage is {candidate.growth_stage.value}.",
            f"Learning velocity is {candidate.learning_velocity}.",
        ]
        risks = []
        if candidate.consistency < 60:
            risks.append("Career/project consistency signal is still developing.")
        if leadership_alignment < 65:
            risks.append("Leadership evidence does not fully match the role expectation.")

        return EvaluatorResult(score=score, confidence=confidence, strengths=strengths, risks=risks)
