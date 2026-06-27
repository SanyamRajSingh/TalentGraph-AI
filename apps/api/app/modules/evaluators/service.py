from app.domain.candidate_twin import CandidateDigitalTwin
from app.domain.evaluation import EvaluationBundle, EvaluatorResult
from app.domain.role_dna import RoleDNAProfile
from app.modules.evaluators.culture import CultureEvaluator
from app.modules.evaluators.domain import DomainEvaluator
from app.modules.evaluators.growth import GrowthEvaluator
from app.modules.evaluators.technical import TechnicalEvaluator
from app.modules.evaluators.utils import average, clamp_score


class EvaluationService:
    """Runs deterministic evaluator modules and computes match aggregates."""

    WEIGHTS = {
        "technical": 0.40,
        "growth": 0.25,
        "domain": 0.20,
        "culture": 0.15,
    }

    def __init__(
        self,
        technical_evaluator: TechnicalEvaluator | None = None,
        growth_evaluator: GrowthEvaluator | None = None,
        domain_evaluator: DomainEvaluator | None = None,
        culture_evaluator: CultureEvaluator | None = None,
    ) -> None:
        self.technical_evaluator = technical_evaluator or TechnicalEvaluator()
        self.growth_evaluator = growth_evaluator or GrowthEvaluator()
        self.domain_evaluator = domain_evaluator or DomainEvaluator()
        self.culture_evaluator = culture_evaluator or CultureEvaluator()

    def evaluate(self, role: RoleDNAProfile, candidate: CandidateDigitalTwin) -> EvaluationBundle:
        technical = self.technical_evaluator.evaluate(role, candidate)
        growth = self.growth_evaluator.evaluate(role, candidate)
        domain = self.domain_evaluator.evaluate(role, candidate)
        culture = self.culture_evaluator.evaluate(role, candidate)
        overall_match = self._overall_match(technical, growth, domain, culture)
        overall_confidence = average(
            [technical.confidence, growth.confidence, domain.confidence, culture.confidence]
        )
        narrative = self._generate_narrative(candidate, role, technical, growth, domain, culture, overall_match)

        return EvaluationBundle(
            candidate_id=candidate.candidate_id,
            role_id=role.role_id,
            technical=technical,
            growth=growth,
            domain=domain,
            culture=culture,
            overall_match=overall_match,
            overall_confidence=overall_confidence,
            narrative=narrative,
        )

    def _overall_match(
        self,
        technical: EvaluatorResult,
        growth: EvaluatorResult,
        domain: EvaluatorResult,
        culture: EvaluatorResult,
    ) -> int:
        return clamp_score(
            technical.score * self.WEIGHTS["technical"]
            + growth.score * self.WEIGHTS["growth"]
            + domain.score * self.WEIGHTS["domain"]
            + culture.score * self.WEIGHTS["culture"]
        )

    def _generate_narrative(
        self,
        candidate: CandidateDigitalTwin,
        role: RoleDNAProfile,
        technical: EvaluatorResult,
        growth: EvaluatorResult,
        domain: EvaluatorResult,
        culture: EvaluatorResult,
        overall_match: int
    ) -> str:
        if overall_match >= 80:
            fit = "an exceptionally strong fit"
        elif overall_match >= 65:
            fit = "a solid fit"
        elif overall_match >= 50:
            fit = "a borderline fit"
        else:
            fit = "a weak fit"

        parts = [f"{candidate.name} is {fit} for the {role.role_title} role ({overall_match}% overall match)."]
        
        if technical.score >= 75:
            parts.append(f"They demonstrate strong technical alignment, particularly in {', '.join(technical.strengths[:2]) if technical.strengths else 'core skills'}.")
        elif technical.risks:
            parts.append(f"There are some technical gaps: {technical.risks[0]}")
            
        if growth.score >= 75:
            parts.append("Their growth trajectory and learning velocity align well with the role's expectations.")
            
        if domain.score >= 70:
            parts.append("They possess relevant domain knowledge which should accelerate their ramp-up time.")
            
        return " ".join(parts)
