from app.domain.evaluation import EvaluationBundle
from app.domain.recommendation import RecommendationLabel, RecommendationResult


class RecommendationService:
    """Derives a final hiring recommendation deterministically from an EvaluationBundle."""

    def recommend(self, bundle: EvaluationBundle) -> RecommendationResult:
        score = bundle.overall_match
        
        # Determine the base label from the overall match score
        if score >= 85:
            label = RecommendationLabel.STRONG_HIRE
            reason = f"Candidate is a very strong match for the role ({score}% overall match)."
        elif score >= 70:
            label = RecommendationLabel.HIRE
            reason = f"Candidate meets the core requirements for the role ({score}% overall match)."
        elif score >= 60:
            label = RecommendationLabel.GROWTH_HIRE
            reason = f"Candidate has high potential but requires ramp-up ({score}% overall match)."
        elif score >= 50:
            label = RecommendationLabel.BORDERLINE
            reason = f"Candidate is a borderline fit and may require significant upskilling ({score}% overall match)."
        else:
            label = RecommendationLabel.NO_HIRE
            reason = f"Candidate does not meet the minimum requirements for the role ({score}% overall match)."
            
        evidence = []
        if bundle.technical and bundle.technical.strengths:
            evidence.append(bundle.technical.strengths[0])
        if bundle.growth and bundle.growth.strengths:
            evidence.append(bundle.growth.strengths[0])
        if bundle.culture and bundle.culture.strengths:
            evidence.append(bundle.culture.strengths[0])
            
        if bundle.technical and bundle.technical.risks:
            evidence.append(f"Risk: {bundle.technical.risks[0]}")
            
        return RecommendationResult(
            candidate_id=bundle.candidate_id,
            role_id=bundle.role_id,
            label=label,
            reason=reason,
            supporting_evidence=evidence
        )
