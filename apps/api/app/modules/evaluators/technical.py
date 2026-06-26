from app.domain.candidate_twin import CandidateDigitalTwin
from app.domain.evaluation import EvaluatorResult
from app.domain.role_dna import RoleDNAProfile
from app.modules.evaluators.utils import average, clamp_score, overlap, percent


class TechnicalEvaluator:
    """Evaluates required/preferred skills and technical signal alignment."""

    def evaluate(self, role: RoleDNAProfile, candidate: CandidateDigitalTwin) -> EvaluatorResult:
        candidate_skills = [*candidate.skills, *candidate.technologies]
        required_matches = overlap(role.required_skills, candidate_skills)
        preferred_matches = overlap(role.preferred_skills, candidate_skills)

        required_score = percent(len(required_matches), len(role.required_skills), default=80)
        preferred_score = percent(len(preferred_matches), len(role.preferred_skills), default=70)
        depth_alignment = 100 - abs(role.technical_depth - candidate.technical_depth)
        complexity_alignment = 100 - abs(role.problem_solving - candidate.project_complexity)

        score = clamp_score(
            required_score * 0.45
            + preferred_score * 0.15
            + depth_alignment * 0.25
            + complexity_alignment * 0.15
        )
        confidence = average([required_score, preferred_score, candidate.confidence])

        strengths = []
        risks = []
        if required_matches:
            strengths.append(f"Matches required skills: {', '.join(sorted(required_matches))}.")
        if preferred_matches:
            strengths.append(f"Matches preferred skills: {', '.join(sorted(preferred_matches))}.")
        missing_required = [skill for skill in role.required_skills if skill.casefold() not in {m.casefold() for m in required_matches}]
        if missing_required:
            risks.append(f"Missing required skills: {', '.join(missing_required)}.")
        if candidate.project_complexity < role.problem_solving:
            risks.append("Project complexity is below the role's problem-solving demand.")

        return EvaluatorResult(score=score, confidence=confidence, strengths=strengths, risks=risks)
