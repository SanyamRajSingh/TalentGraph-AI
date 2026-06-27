from app.domain.candidate_twin import CandidateDigitalTwin
from app.domain.evaluation import EvaluatorResult
from app.domain.role_dna import RoleDNAProfile
from app.modules.evaluators.utils import clamp_score, overlap, percent
from app.modules.graph_builder.ontology import load_ontology


class DomainEvaluator:
    """Evaluates domain overlap and ontology-adjacent transferable skill signals."""

    def evaluate(self, role: RoleDNAProfile, candidate: CandidateDigitalTwin) -> EvaluatorResult:
        domain_matches = overlap([role.domain], candidate.domains)
        transferable_skills = overlap(role.required_skills, candidate.skills)
        adjacent = self._adjacent_matches(role.required_skills, candidate.skills + candidate.technologies)

        domain_score = 100 if domain_matches else 55
        transfer_score = percent(len(transferable_skills), len(role.required_skills), default=70)
        adjacent_score = min(100, len(adjacent) * 35)
        score = clamp_score(domain_score * 0.45 + transfer_score * 0.35 + adjacent_score * 0.20)
        confidence = clamp_score(55 + len(candidate.domains) * 8 + len(transferable_skills) * 6 + len(adjacent) * 4)

        strengths = []
        risks = []
        evidence = []
        missing_signals = []
        if domain_matches:
            strengths.append(f"Direct domain overlap: {', '.join(sorted(domain_matches))}.")
            evidence.append(f"Matched domains: {', '.join(sorted(domain_matches))}.")
        if adjacent:
            strengths.append(f"Ontology-adjacent skills/technologies: {', '.join(sorted(adjacent))}.")
            evidence.append(f"Found {len(adjacent)} transferable skills from related domains.")
        if not domain_matches:
            risks.append(f"No direct candidate domain match for {role.domain}.")
            missing_signals.append("Direct industry/domain experience")
        if not transferable_skills:
            risks.append("Limited direct transferable required-skill evidence.")
            missing_signals.append("Transferable required skills")

        ramp_up_estimate = "1-2 months" if score >= 80 else "3-5 months"

        return EvaluatorResult(
            score=score, 
            confidence=confidence, 
            strengths=strengths, 
            risks=risks,
            evidence=evidence,
            missing_signals=missing_signals,
            ramp_up_estimate=ramp_up_estimate
        )

    @staticmethod
    def _adjacent_matches(role_skills: list[str], candidate_terms: list[str]) -> set[str]:
        ontology = load_ontology()["skills"]
        candidate_keys = {term.casefold() for term in candidate_terms}
        matches: set[str] = set()
        for skill in role_skills:
            for adjacent in ontology.get(skill, []):
                if adjacent.casefold() in candidate_keys:
                    matches.add(adjacent)
        return matches
