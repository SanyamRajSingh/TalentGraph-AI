import json
import re

from app.providers.llm_provider import LLMProvider, LLMResponse

TECH_SKILLS = {
    "Python": ("python",),
    "Machine Learning": ("machine learning", "ml "),
    "SQL": ("sql",),
    "Data Engineering": ("data engineering", "etl", "pipeline"),
    "Distributed Systems": ("distributed", "scalable systems"),
    "React": ("react", "frontend"),
    "FastAPI": ("fastapi", "api"),
    "Statistics": ("statistics", "statistical"),
    "NLP": ("nlp", "language model"),
    "Cloud": ("aws", "gcp", "azure", "cloud"),
}


class LocalRoleDNALLMProvider(LLMProvider):
    """Deterministic local provider for demos when no external LLM is configured."""

    def complete_json(self, system_prompt: str, user_prompt: str, schema_name: str) -> LLMResponse:
        job_description = user_prompt.split("Job description:", maxsplit=1)[-1].strip()
        text = job_description.casefold()

        required_skills = [
            skill for skill, needles in TECH_SKILLS.items() if any(needle in text for needle in needles)
        ]
        if not required_skills:
            required_skills = ["Problem Solving", "Communication"]

        preferred_skills = []
        for skill in ("Leadership", "Experimentation", "Product Thinking", "Stakeholder Management"):
            if skill.casefold().split()[0] in text:
                preferred_skills.append(skill)

        role_title = self._infer_title(job_description)
        domain = self._infer_domain(text)
        seniority = self._infer_seniority(text)
        archetype = self._infer_archetype(text, required_skills)
        startup_score = 82 if any(word in text for word in ("startup", "0 to 1", "founding")) else 45

        payload = {
            "role_title": role_title,
            "domain": domain,
            "seniority": seniority,
            "role_archetype": archetype,
            "fingerprint": self._infer_fingerprint(text, archetype),
            "required_skills": required_skills,
            "preferred_skills": preferred_skills,
            "skill_importance": self._skill_weights(required_skills, preferred_skills),
            "technical_depth": 88 if required_skills else 60,
            "problem_solving": 84,
            "communication": 72 if "stakeholder" in text else 62,
            "ownership": 86 if any(word in text for word in ("own", "lead", "drive")) else 68,
            "leadership": 78 if any(word in text for word in ("lead", "mentor", "manager")) else 45,
            "learning_agility": 82 if any(word in text for word in ("learn", "ambiguous", "new")) else 68,
            "ambiguity_tolerance": 84 if any(word in text for word in ("ambiguous", "0 to 1", "startup")) else 55,
            "collaboration": 76 if any(word in text for word in ("cross-functional", "team", "stakeholder")) else 58,
            "startup_vs_enterprise_environment": startup_score,
            "work_environment": {
                "startup_vs_enterprise": startup_score,
                "ambiguity_tolerance": 84 if "ambiguous" in text else 55,
                "collaboration": 76 if "team" in text else 58,
                "ownership": 86 if "own" in text else 68,
                "communication": 72 if "stakeholder" in text else 62,
            },
            "weight_distribution": {
                "technical_depth": 25,
                "problem_solving": 20,
                "communication": 10,
                "ownership": 15,
                "leadership": 10,
                "learning_agility": 10,
                "ambiguity_tolerance": 5,
                "collaboration": 5,
            },
            "reasoning": [
                f"The role reads as {archetype} because the description emphasizes {', '.join(required_skills[:3])}.",
                f"{seniority} expectations are inferred from ownership, leadership, and execution language.",
                "Weights prioritize the strongest repeated requirements while keeping soft-skill signals visible.",
            ],
            "confidence": 78,
        }
        return LLMResponse(text=json.dumps(payload), model="local-role-dna", metadata={"schema": schema_name})

    @staticmethod
    def _infer_title(job_description: str) -> str:
        match = re.search(r"(?:hiring|seeking|looking for|role[:\s]+)\s+(?:an?\s+)?([^.\n]+)", job_description, re.I)
        if match:
            return match.group(1).strip(" :-")[:80]
        if "data scientist" in job_description.casefold():
            return "Data Scientist"
        if "engineer" in job_description.casefold():
            return "Software Engineer"
        return "Unspecified Role"

    @staticmethod
    def _infer_domain(text: str) -> str:
        if any(word in text for word in ("fintech", "financial", "payments", "banking")):
            return "FinTech"
        if any(word in text for word in ("health", "clinical", "patient")):
            return "HealthTech"
        if any(word in text for word in ("hiring", "talent", "recruiting")):
            return "HRTech"
        return "General Technology"

    @staticmethod
    def _infer_seniority(text: str) -> str:
        if any(word in text for word in ("principal", "staff", "architect")):
            return "Staff+"
        if any(word in text for word in ("senior", "lead", "mentor")):
            return "Senior"
        if any(word in text for word in ("junior", "entry", "graduate")):
            return "Junior"
        return "Mid-level"

    @staticmethod
    def _infer_archetype(text: str, skills: list[str]) -> str:
        if "Machine Learning" in skills or "Statistics" in skills:
            return "Analytical Builder"
        if any(word in text for word in ("platform", "distributed", "infrastructure")):
            return "Systems Builder"
        if any(word in text for word in ("product", "customer", "experiment")):
            return "Product-Minded Operator"
        return "Generalist Builder"

    @staticmethod
    def _infer_fingerprint(text: str, archetype: str) -> str:
        if any(word in text for word in ("ambiguous", "0 to 1", "startup")) and any(
            word in text for word in ("technical", "ml", "python", "distributed")
        ):
            return "High-Ambiguity Technical Specialist"
        if "Analytical" in archetype and any(word in text for word in ("build", "production", "engineer")):
            return "Builder-Researcher Hybrid"
        if "Analytical" in archetype:
            return "Researcher"
        if any(word in text for word in ("operate", "stakeholder", "business")):
            return "Operator"
        return "Builder"

    @staticmethod
    def _skill_weights(required_skills: list[str], preferred_skills: list[str]) -> dict[str, int]:
        weights = {skill: 15 for skill in required_skills}
        weights.update({skill: 7 for skill in preferred_skills})
        return weights
