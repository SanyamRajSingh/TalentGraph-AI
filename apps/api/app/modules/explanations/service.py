from app.domain.candidate_twin import CandidateDigitalTwin
from app.domain.evaluation import EvaluationBundle, EvaluatorResult
from app.domain.explanation import ExplanationProfile
from app.domain.ranking import RankingResult
from app.domain.role_dna import RoleDNAProfile
from app.modules.explanations.counterfactual_service import CounterfactualService
from app.repositories.explanation_repository import ExplanationRepository


class ExplanationService:
    """Generates and persists deterministic candidate explanations."""

    def __init__(
        self,
        counterfactual_service: CounterfactualService,
        explanation_repository: ExplanationRepository,
    ) -> None:
        self.counterfactual_service = counterfactual_service
        self.explanation_repository = explanation_repository

    def generate(
        self,
        role: RoleDNAProfile,
        candidate: CandidateDigitalTwin,
        evaluation: EvaluationBundle,
        ranking: RankingResult,
    ) -> ExplanationProfile:
        profile = ExplanationProfile(
            candidate_id=candidate.candidate_id,
            role_id=role.role_id,
            ranking_position=ranking.rank,
            strengths=self._strengths(role, candidate, evaluation),
            risks=self._risks(role, candidate, evaluation),
            reasoning=self._reasoning(role, candidate, evaluation, ranking),
            counterfactuals=self.counterfactual_service.generate(role, candidate, evaluation),
        )
        return self.explanation_repository.save(profile)

    def _strengths(
        self,
        role: RoleDNAProfile,
        candidate: CandidateDigitalTwin,
        evaluation: EvaluationBundle,
    ) -> list[str]:
        strengths: list[str] = []
        matched_required = [
            skill for skill in role.required_skills if skill.lower() in {item.lower() for item in candidate.skills}
        ]
        if matched_required:
            strengths.append(f"Strong alignment with required skills: {', '.join(matched_required[:3])}.")
        if candidate.learning_velocity >= role.learning_agility:
            strengths.append("Demonstrates high learning velocity relative to role expectations.")
        if candidate.ownership >= role.ownership:
            strengths.append("Good ownership signals from projects and experience.")

        for result in self._results(evaluation):
            if result.score >= 75:
                strengths.extend(result.strengths[:2])

        return self._dedupe(strengths)[:6]

    def _risks(
        self,
        role: RoleDNAProfile,
        candidate: CandidateDigitalTwin,
        evaluation: EvaluationBundle,
    ) -> list[str]:
        risks: list[str] = []
        if evaluation.domain and evaluation.domain.score < 70:
            risks.append(f"Limited domain exposure for {role.domain}.")
        if candidate.communication < role.communication:
            risks.append("Communication score is below role expectations.")
        if candidate.leadership < role.leadership and role.leadership >= 65:
            risks.append("Leadership evidence may be lighter than the role requires.")

        for result in self._results(evaluation):
            if result.score < 70:
                risks.extend(result.risks[:2])

        return self._dedupe(risks)[:6]

    def _reasoning(
        self,
        role: RoleDNAProfile,
        candidate: CandidateDigitalTwin,
        evaluation: EvaluationBundle,
        ranking: RankingResult,
    ) -> list[str]:
        reasoning = [
            f"Ranked #{ranking.rank} for {role.role_title} under {ranking.persona.value}.",
            f"Ranking score {ranking.score} is based on evaluation {evaluation.evaluation_id}.",
            f"Overall match is {evaluation.overall_match} with confidence {evaluation.overall_confidence}.",
        ]

        for label, result in [
            ("Technical", evaluation.technical),
            ("Growth", evaluation.growth),
            ("Domain", evaluation.domain),
            ("Culture", evaluation.culture),
        ]:
            if result is not None:
                reasoning.append(f"{label} score is {result.score}: {result.explanation or 'deterministic evaluator output.'}")

        if candidate.projects:
            reasoning.append(f"Candidate evidence includes {len(candidate.projects)} project signal(s).")

        return reasoning

    def _results(self, evaluation: EvaluationBundle) -> list[EvaluatorResult]:
        return [
            result
            for result in [evaluation.technical, evaluation.growth, evaluation.domain, evaluation.culture]
            if result is not None
        ]

    def _dedupe(self, items: list[str]) -> list[str]:
        seen: set[str] = set()
        deduped: list[str] = []
        for item in items:
            normalized = item.strip()
            if normalized and normalized not in seen:
                deduped.append(normalized)
                seen.add(normalized)
        return deduped
