import json

from app.modules.role_dna.service import RoleDNAService
from app.pipelines.role_pipeline import RolePipeline
from app.providers.llm_provider import LLMProvider, LLMResponse
from app.repositories.memory import InMemoryRoleDNARepository


class PipelineMockProvider(LLMProvider):
    def complete_json(self, system_prompt: str, user_prompt: str, schema_name: str) -> LLMResponse:
        return LLMResponse(
            text=json.dumps(
                {
                    "role_title": "Data Scientist",
                    "domain": "FinTech",
                    "seniority": "Senior",
                    "role_archetype": "Analytical Builder",
                    "required_skills": ["Python", "SQL"],
                    "preferred_skills": ["Machine Learning"],
                    "technical_depth": 90,
                    "problem_solving": 88,
                    "communication": 70,
                    "ownership": 80,
                    "leadership": 60,
                    "learning_agility": 92,
                    "ambiguity_tolerance": 75,
                    "collaboration": 72,
                    "startup_vs_enterprise_environment": 68,
                    "reasoning": ["Data-heavy role with strong analytical requirements."],
                }
            ),
            model="mock",
        )


def test_role_pipeline_persists_job_and_role_dna() -> None:
    repository = InMemoryRoleDNARepository()
    pipeline = RolePipeline(
        role_dna_service=RoleDNAService(PipelineMockProvider()),
        role_repository=repository,
    )

    job, upload_event = pipeline.upload_job("Hiring a senior data scientist for fintech.")
    profile, generated_event = pipeline.run("", job_id=job.job_id)

    assert upload_event.job_id == job.job_id
    assert generated_event.role_id == profile.role_id
    assert repository.get_job(job.job_id) == job
    assert repository.get_by_role_id(profile.role_id) == profile
    assert profile.job_id == job.job_id
