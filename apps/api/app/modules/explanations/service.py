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
            evidence=self._evidence(candidate, evaluation),
            estimations=self._estimations(role, candidate),
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

        # Intelligence index strengths
        if hasattr(candidate, 'leadership_readiness') and candidate.leadership_readiness >= 70:
            strengths.append(f"High leadership readiness score ({candidate.leadership_readiness}/100) signals management potential.")
        if hasattr(candidate, 'adaptability') and candidate.adaptability >= 70:
            strengths.append(f"Strong adaptability ({candidate.adaptability}/100) — broad skill set across multiple domains.")
        if hasattr(candidate, 'execution_speed') and candidate.execution_speed >= 70:
            strengths.append(f"High execution velocity ({candidate.execution_speed}/100) based on delivery language in resume.")
        if hasattr(candidate, 'business_acumen') and candidate.business_acumen >= 70:
            strengths.append(f"Business acumen score ({candidate.business_acumen}/100) shows awareness of commercial outcomes.")

        for result in self._results(evaluation):
            if result.score >= 75:
                strengths.extend(result.strengths[:2])

        return self._dedupe(strengths)[:7]

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

        # Intelligence index risks
        if hasattr(candidate, 'leadership_readiness') and candidate.leadership_readiness < 45:
            risks.append(f"Leadership readiness score ({candidate.leadership_readiness}/100) is low — may struggle with people responsibilities.")
        if hasattr(candidate, 'business_acumen') and candidate.business_acumen < 45:
            risks.append(f"Business acumen ({candidate.business_acumen}/100) signals may be insufficient for a customer-facing or strategy role.")
        if hasattr(candidate, 'adaptability') and candidate.adaptability < 40:
            risks.append(f"Low adaptability score ({candidate.adaptability}/100) — narrow domain profile detected.")

        for result in self._results(evaluation):
            if result.score < 70:
                risks.extend(result.risks[:2])

        return self._dedupe(risks)[:7]

    def _reasoning(
        self,
        role: RoleDNAProfile,
        candidate: CandidateDigitalTwin,
        evaluation: EvaluationBundle,
        ranking: RankingResult,
    ) -> list[str]:
        reasoning = [
            f"Ranked #{ranking.rank} for {role.role_title} under the '{ranking.persona.value}' hiring persona.",
            f"Overall match is {evaluation.overall_match}/100 with confidence {evaluation.overall_confidence}/100.",
        ]

        for label, result in [
            ("Technical", evaluation.technical),
            ("Growth", evaluation.growth),
            ("Domain", evaluation.domain),
            ("Culture", evaluation.culture),
        ]:
            if result is not None:
                reasoning.append(f"{label} evaluator score: {result.score}/100 — {result.explanation or 'deterministic evaluator output.'}")

        if candidate.projects:
            reasoning.append(f"Candidate evidence includes {len(candidate.projects)} project signal(s) and {len(candidate.timeline)} timeline event(s).")

        return reasoning

    def _evidence(
        self,
        candidate: CandidateDigitalTwin,
        evaluation: EvaluationBundle,
    ) -> list[str]:
        """Hard observable facts from the candidate's resume and evaluations."""
        evidence: list[str] = []
        if candidate.skills:
            evidence.append(f"Extracted {len(candidate.skills)} skills: {', '.join(candidate.skills[:6])}{'...' if len(candidate.skills) > 6 else ''}.")
        if candidate.projects:
            evidence.append(f"Identified {len(candidate.projects)} project(s): {', '.join(candidate.projects[:3])}{'...' if len(candidate.projects) > 3 else ''}.")
        if candidate.experiences:
            evidence.append(f"Resume contains {len(candidate.experiences)} experience record(s).")
        if candidate.certifications:
            evidence.append(f"Certifications found: {', '.join(candidate.certifications[:3])}.")
        if candidate.timeline:
            years = sorted({e.year for e in candidate.timeline})
            if years:
                evidence.append(f"Career timeline spans {years[0]}–{years[-1]} ({len(years)} year(s) recorded).")
        for result in self._results(evaluation):
            if result.score is not None:
                evidence.append(f"Evaluator '{result.dimension if hasattr(result, 'dimension') else 'unknown'}' returned a computed score of {result.score}/100.")
        return self._dedupe(evidence)[:6]

    def _estimations(
        self,
        role: RoleDNAProfile,
        candidate: CandidateDigitalTwin,
    ) -> list[str]:
        """Inferred predictions about future performance — clearly labelled as estimates."""
        estimations: list[str] = []
        lv = candidate.learning_velocity
        if lv >= 75:
            estimations.append(f"Estimated: Candidate likely to ramp into role within 1–2 months given high learning velocity ({lv}/100).")
        elif lv >= 50:
            estimations.append(f"Estimated: Candidate ramp-up expected within 2–4 months based on learning velocity ({lv}/100).")
        else:
            estimations.append(f"Estimated: Longer onboarding may be needed — learning velocity is {lv}/100.")

        if hasattr(candidate, 'leadership_readiness'):
            lr = candidate.leadership_readiness
            if lr >= 70:
                estimations.append(f"Estimated: High likelihood of succeeding in team-lead or mentoring responsibilities (readiness: {lr}/100).")
            elif lr >= 50:
                estimations.append(f"Estimated: Candidate shows potential for leadership, but may need 6–12 months of structured growth (readiness: {lr}/100).")

        if hasattr(candidate, 'execution_speed'):
            es = candidate.execution_speed
            if es >= 70:
                estimations.append(f"Estimated: Candidate likely to deliver quickly in a results-oriented environment (execution speed: {es}/100).")

        matched = [s for s in role.required_skills if s.lower() in {x.lower() for x in candidate.skills}]
        coverage = len(matched) / max(len(role.required_skills), 1) * 100
        estimations.append(f"Estimated: {coverage:.0f}% coverage of required role skills based on extracted resume data.")

        return self._dedupe(estimations)[:5]

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

