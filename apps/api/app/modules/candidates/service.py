from time import perf_counter

from app.domain.candidate_twin import CandidateDigitalTwin
from app.modules.candidates.normalizer import (
    build_timeline,
    clamp_score,
    infer_growth_stage,
    normalize_list,
    infer_strengths,
    infer_weaknesses,
    infer_risk_profile,
    recommend_roles,
)
from app.providers.parser_provider import ParserProvider


class CandidateDigitalTwinService:
    """Builds deterministic Candidate Digital Twins from parsed resume text."""

    def __init__(self, parser_provider: ParserProvider) -> None:
        self.parser_provider = parser_provider

    def build_from_resume_text(
        self,
        resume_text: str,
        resume_id: str | None = None,
        source_name: str | None = None,
    ) -> CandidateDigitalTwin:
        started = perf_counter()
        parsed = self.parser_provider.parse_resume_text(resume_text, source_name=source_name)
        fields = parsed.structured_fields

        skills = normalize_list(fields.get("skills"))
        technologies = normalize_list(fields.get("technologies")) or skills
        projects = normalize_list(fields.get("projects"))
        experiences = normalize_list(fields.get("experiences"))
        certifications = normalize_list(fields.get("certifications"))
        achievements = normalize_list(fields.get("achievements"))
        domains = normalize_list(fields.get("domains"))
        timeline = build_timeline(parsed.raw_text, fields)
        metrics = self._derive_metrics(parsed.raw_text, skills, projects, experiences, achievements, domains, timeline)
        growth_stage = infer_growth_stage(metrics, skills, projects, domains)

        strengths = infer_strengths(metrics)
        weaknesses = infer_weaknesses(metrics)
        risk_profile = infer_risk_profile(metrics)
        recommended_roles = recommend_roles(growth_stage)
        
        growth_signals = [f"Learning velocity score is {metrics['learning_velocity']}/100."]
        leadership_signals = [f"Leadership score is {metrics['leadership']}/100.", f"Ownership score is {metrics['ownership']}/100."]
        success_environments = ["Fast-paced startups", "Agile teams"] if metrics['ownership'] >= 60 else ["Structured enterprise environments"]
        career_progression_score = clamp_score(50 + len(timeline) * 5 + int(metrics['leadership'] * 0.2))

        processing_time_ms = int((perf_counter() - started) * 1000)
        return CandidateDigitalTwin(
            resume_id=resume_id,
            name=self._text_field(fields.get("name"), "Unknown Candidate"),
            email=self._optional_text(fields.get("email")),
            phone=self._optional_text(fields.get("phone")),
            location=self._optional_text(fields.get("location")),
            skills=skills,
            technologies=technologies,
            projects=projects,
            experiences=experiences,
            certifications=certifications,
            achievements=achievements,
            domains=domains or ["General Technology"],
            timeline=timeline,
            growth_stage=growth_stage,
            strengths=strengths,
            weaknesses=weaknesses,
            growth_signals=growth_signals,
            leadership_signals=leadership_signals,
            career_progression_score=career_progression_score,
            risk_profile=risk_profile,
            recommended_roles=recommended_roles,
            success_environments=success_environments,
            reasoning=self._build_reasoning(metrics, growth_stage.value, skills, projects, timeline),
            processing_time_ms=processing_time_ms,
            **metrics,
        )

    @staticmethod
    def _derive_metrics(
        raw_text: str,
        skills: list[str],
        projects: list[str],
        experiences: list[str],
        achievements: list[str],
        domains: list[str],
        timeline: list[object],
    ) -> dict[str, int]:
        text = raw_text.casefold()
        technical_depth = clamp_score(35 + len(skills) * 6 + len(projects) * 4)
        learning_velocity = clamp_score(40 + len(timeline) * 8 + len(certified_terms(text)) * 6)
        leadership = clamp_score(35 + keyword_count(text, ("lead", "mentor", "managed", "owned")) * 12)
        ownership = clamp_score(40 + keyword_count(text, ("owned", "built", "shipped", "launched")) * 10)
        communication = clamp_score(45 + keyword_count(text, ("presented", "stakeholder", "documented", "communicated")) * 10)
        project_complexity = clamp_score(35 + len(projects) * 10 + keyword_count(text, ("distributed", "ml", "scale", "pipeline")) * 8)
        collaboration = clamp_score(45 + keyword_count(text, ("team", "cross-functional", "partnered", "collaborated")) * 9)
        consistency = clamp_score(45 + len(experiences) * 8 + len(achievements) * 5 + min(len(timeline), 5) * 5)
        
        # New Intelligence Indices
        leadership_readiness = clamp_score(30 + leadership * 0.4 + communication * 0.3 + project_complexity * 0.3)
        adaptability = clamp_score(40 + len(set(skills)) * 2 + len(domains) * 10)
        execution_speed = clamp_score(45 + keyword_count(text, ("shipped", "delivered", "accelerated", "reduced", "faster")) * 12)
        business_acumen = clamp_score(35 + keyword_count(text, ("revenue", "cost", "conversion", "stakeholder", "strategy", "roi")) * 12)
        
        confidence = clamp_score(50 + min(len(raw_text) // 250, 20) + len(skills) * 3 + min(len(timeline), 4) * 5)

        return {
            "technical_depth": technical_depth,
            "learning_velocity": learning_velocity,
            "leadership": leadership,
            "ownership": ownership,
            "communication": communication,
            "project_complexity": project_complexity,
            "collaboration": collaboration,
            "consistency": consistency,
            "leadership_readiness": leadership_readiness,
            "adaptability": adaptability,
            "execution_speed": execution_speed,
            "business_acumen": business_acumen,
            "confidence": confidence,
        }

    @staticmethod
    def _build_reasoning(
        metrics: dict[str, int],
        growth_stage: str,
        skills: list[str],
        projects: list[str],
        timeline: list[object],
    ) -> list[str]:
        top_skills = ", ".join(skills[:4]) if skills else "general problem-solving signals"
        return [
            f"Growth stage is {growth_stage} based on technical signals, ownership language, and project evidence.",
            f"Technical depth is supported by {top_skills}.",
            f"Project complexity reflects {len(projects)} project signal(s) and {len(timeline)} timeline event(s).",
            "Scores are deterministic and normalized to a 0-100 scale.",
        ]

    @staticmethod
    def _text_field(value: object, default: str) -> str:
        return value.strip() if isinstance(value, str) and value.strip() else default

    @staticmethod
    def _optional_text(value: object) -> str | None:
        return value.strip() if isinstance(value, str) and value.strip() else None


def keyword_count(text: str, keywords: tuple[str, ...]) -> int:
    return sum(1 for keyword in keywords if keyword in text)


def certified_terms(text: str) -> list[str]:
    return [term for term in ("certified", "course", "learned", "trained") if term in text]
