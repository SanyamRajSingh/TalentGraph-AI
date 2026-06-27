from app.domain.candidate_twin import CandidateDigitalTwin
from app.domain.evaluation import EvaluationBundle, EvaluatorResult
from app.domain.role_dna import RoleDNAProfile


class CounterfactualService:
    """Generates deterministic improvement suggestions from evaluator score gaps."""

    def generate(
        self,
        role: RoleDNAProfile,
        candidate: CandidateDigitalTwin,
        evaluation: EvaluationBundle,
    ) -> list[str]:
        gaps = [
            ("technical", evaluation.technical),
            ("growth", evaluation.growth),
            ("domain", evaluation.domain),
            ("culture", evaluation.culture),
        ]
        ordered_gaps = sorted(
            [(name, result) for name, result in gaps if result is not None],
            key=lambda item: item[1].score,
        )

        suggestions: list[str] = []
        for name, result in ordered_gaps:
            if len(suggestions) == 3:
                break
            if result.score >= 78 and suggestions:
                continue
            suggestion = self._suggestion_for_gap(name, role, candidate, result)
            if suggestion not in suggestions:
                suggestions.append(suggestion)

        return suggestions[:3]

    def _suggestion_for_gap(
        self,
        gap_name: str,
        role: RoleDNAProfile,
        candidate: CandidateDigitalTwin,
        result: EvaluatorResult,
    ) -> str:
        if gap_name == "technical":
            missing_skills = [
                skill
                for skill in role.required_skills[:4]
                if skill.lower() not in {candidate_skill.lower() for candidate_skill in candidate.skills}
            ]
            if missing_skills:
                return f"Gain stronger hands-on evidence in {', '.join(missing_skills[:2])}."
            return "Show deeper technical ownership on larger or more complex projects."

        if gap_name == "growth":
            if candidate.leadership < 65:
                return "Demonstrate leadership on larger projects with clear scope and outcomes."
            return "Add recent examples that show faster learning velocity and increasing responsibility."

        if gap_name == "domain":
            domain = role.domain or "the target domain"
            return f"Increase domain exposure to {domain} through projects, products, or applied case work."

        if gap_name == "culture":
            if candidate.communication < role.communication:
                return "Improve communication evidence with clearer stakeholder, documentation, or presentation examples."
            if candidate.ownership < role.ownership:
                return "Add stronger ownership evidence showing decisions made under ambiguity."
            return "Provide more collaboration evidence across product, engineering, or business partners."

        return result.risks[0] if result.risks else "Add clearer evidence for the weakest match dimension."
