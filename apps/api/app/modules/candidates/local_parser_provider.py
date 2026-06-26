import re
from typing import Any

from app.providers.parser_provider import ParsedCandidateInput, ParserProvider

KNOWN_SKILLS = (
    "Python",
    "SQL",
    "JavaScript",
    "TypeScript",
    "React",
    "FastAPI",
    "Django",
    "Machine Learning",
    "Statistics",
    "NLP",
    "Docker",
    "Kubernetes",
    "AWS",
    "GCP",
    "Azure",
    "Pandas",
    "Spark",
    "PostgreSQL",
)

DOMAIN_KEYWORDS = {
    "FinTech": ("fintech", "payments", "banking", "fraud", "transaction"),
    "Machine Learning": ("machine learning", "ml", "model", "nlp"),
    "Backend Systems": ("backend", "api", "distributed", "microservice"),
    "Product Analytics": ("product analyst", "experimentation", "dashboard", "metrics"),
    "Data Engineering": ("pipeline", "etl", "spark", "warehouse"),
}


class LocalResumeParserProvider(ParserProvider):
    """Deterministic parser for plain text and markdown resumes."""

    def parse_resume(self, content: bytes, filename: str) -> ParsedCandidateInput:
        return self.parse_resume_text(content.decode("utf-8", errors="ignore"), source_name=filename)

    def parse_resume_text(self, resume_text: str, source_name: str | None = None) -> ParsedCandidateInput:
        fields: dict[str, Any] = {
            "name": self._extract_name(resume_text),
            "email": self._extract_email(resume_text),
            "phone": self._extract_phone(resume_text),
            "location": self._extract_location(resume_text),
            "skills": self._extract_skills(resume_text),
            "technologies": self._extract_skills(resume_text),
            "projects": self._extract_section_items(resume_text, "projects"),
            "experiences": self._extract_section_items(resume_text, "experience"),
            "certifications": self._extract_section_items(resume_text, "certifications"),
            "achievements": self._extract_section_items(resume_text, "achievements"),
            "domains": self._extract_domains(resume_text),
            "years": sorted({int(year) for year in re.findall(r"\b(20[0-3][0-9])\b", resume_text)}),
        }
        return ParsedCandidateInput(raw_text=resume_text, structured_fields=fields, source_name=source_name)

    def parse_structured_profile(self, payload: dict[str, object]) -> ParsedCandidateInput:
        raw_text = "\n".join(f"{key}: {value}" for key, value in sorted(payload.items()))
        return ParsedCandidateInput(raw_text=raw_text, structured_fields=payload, source_name=None)

    @staticmethod
    def _extract_name(text: str) -> str:
        for line in text.splitlines():
            cleaned = line.strip().strip("#").strip()
            if cleaned and "@" not in cleaned and len(cleaned.split()) <= 5:
                return cleaned
        return "Unknown Candidate"

    @staticmethod
    def _extract_email(text: str) -> str | None:
        match = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
        return match.group(0) if match else None

    @staticmethod
    def _extract_phone(text: str) -> str | None:
        match = re.search(r"(?:\+?\d[\d\s().-]{8,}\d)", text)
        return match.group(0).strip() if match else None

    @staticmethod
    def _extract_location(text: str) -> str | None:
        match = re.search(r"(?:Location|Based in):\s*([^\n]+)", text, re.I)
        return match.group(1).strip() if match else None

    @staticmethod
    def _extract_skills(text: str) -> list[str]:
        lowered = text.casefold()
        return [skill for skill in KNOWN_SKILLS if skill.casefold() in lowered]

    @staticmethod
    def _extract_section_items(text: str, section: str) -> list[str]:
        pattern = re.compile(rf"^#+\s*{section}\s*$([\s\S]*?)(?=^#+\s|\Z)", re.I | re.M)
        match = pattern.search(text)
        if not match:
            return []
        items: list[str] = []
        for line in match.group(1).splitlines():
            cleaned = line.strip().lstrip("-*").strip()
            if cleaned:
                items.append(cleaned)
        return items

    @staticmethod
    def _extract_domains(text: str) -> list[str]:
        lowered = text.casefold()
        domains = [
            domain
            for domain, keywords in DOMAIN_KEYWORDS.items()
            if any(keyword in lowered for keyword in keywords)
        ]
        return domains or ["General Technology"]
