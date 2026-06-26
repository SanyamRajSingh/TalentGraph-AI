from app.domain.candidate_twin import CandidateDigitalTwin
from app.domain.role_dna import RoleDNAProfile
from app.domain.vector import SummaryDocument


class SummaryService:
    """Generates deterministic role and candidate summaries."""

    def role_summary(self, role: RoleDNAProfile) -> SummaryDocument:
        skills = ", ".join(role.required_skills[:6]) or "no explicit skills"
        text = (
            f"{role.role_title} in {role.domain}. Archetype: {role.role_archetype}. "
            f"Fingerprint: {role.fingerprint}. Required skills: {skills}. "
            f"Key scores: technical depth {role.technical_depth}, problem solving {role.problem_solving}, "
            f"ownership {role.ownership}, learning agility {role.learning_agility}."
        )
        return SummaryDocument(
            id=f"summary:role:{role.role_id}",
            kind="role_summary",
            owner_id=role.role_id,
            text=text,
            metadata={"role_title": role.role_title, "domain": role.domain},
        )

    def candidate_summary(self, candidate: CandidateDigitalTwin) -> SummaryDocument:
        skills = ", ".join(candidate.skills[:6]) or "no explicit skills"
        domains = ", ".join(candidate.domains[:4]) or "General"
        text = (
            f"{candidate.name}. Growth stage: {candidate.growth_stage.value}. "
            f"Domains: {domains}. Skills: {skills}. "
            f"Key scores: technical depth {candidate.technical_depth}, learning velocity {candidate.learning_velocity}, "
            f"ownership {candidate.ownership}, project complexity {candidate.project_complexity}."
        )
        return SummaryDocument(
            id=f"summary:candidate:{candidate.candidate_id}",
            kind="candidate_summary",
            owner_id=candidate.candidate_id,
            text=text,
            metadata={"name": candidate.name, "growth_stage": candidate.growth_stage.value},
        )
