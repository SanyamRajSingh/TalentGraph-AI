import json

import pytest

from app.modules.role_dna.service import RoleDNAService
from app.providers.llm_provider import LLMProvider, LLMResponse


class MockLLMProvider(LLMProvider):
    def __init__(self, payload: dict[str, object] | None = None, text: str | None = None) -> None:
        self.payload = payload
        self.text = text

    def complete_json(self, system_prompt: str, user_prompt: str, schema_name: str) -> LLMResponse:
        text = self.text if self.text is not None else json.dumps(self.payload)
        return LLMResponse(text=text, model="mock")


def test_service_uses_injected_provider_and_returns_normalized_profile() -> None:
    service = RoleDNAService(
        llm_provider=MockLLMProvider(
            payload={
                "role_title": "ML Engineer",
                "domain": "FinTech",
                "seniority": "Senior",
                "role_archetype": "Analytical Builder",
                "fingerprint": "Builder-Researcher Hybrid",
                "required_skills": ["Python", "Machine Learning"],
                "preferred_skills": ["MLOps"],
                "technical_depth": 92,
                "problem_solving": 88,
                "communication": 65,
                "ownership": 80,
                "leadership": 55,
                "learning_agility": 90,
                "ambiguity_tolerance": 75,
                "collaboration": 70,
                "startup_vs_enterprise_environment": 85,
                "reasoning": ["Strong ML execution signals."],
            }
        )
    )

    profile = service.generate("We need a senior ML engineer.", job_id="job_abc")

    assert profile.job_id == "job_abc"
    assert profile.role_title == "ML Engineer"
    assert profile.technical_depth == 92
    assert profile.fingerprint == "Builder-Researcher Hybrid"
    assert "Strong ML execution signals." in profile.reasoning


def test_service_rejects_invalid_provider_json() -> None:
    service = RoleDNAService(llm_provider=MockLLMProvider(text="not-json"))

    with pytest.raises(ValueError, match="invalid JSON"):
        service.generate("bad provider output")
