import json

from app.domain.role_dna import RoleDNAProfile
from app.modules.role_dna.normalizer import normalize_role_dna_payload
from app.modules.role_dna.prompts import ROLE_DNA_SYSTEM_PROMPT, build_role_dna_user_prompt
from app.providers.llm_provider import LLMProvider


class RoleDNAService:
    """Generates deterministic, normalized Role DNA profiles from job descriptions."""

    def __init__(self, llm_provider: LLMProvider) -> None:
        self.llm_provider = llm_provider

    def generate(self, job_description: str, job_id: str | None = None) -> RoleDNAProfile:
        response = self.llm_provider.complete_json(
            system_prompt=ROLE_DNA_SYSTEM_PROMPT,
            user_prompt=build_role_dna_user_prompt(job_description),
            schema_name="RoleDNAProfile",
        )
        payload = self._parse_json_response(response.text)
        return normalize_role_dna_payload(payload, job_id=job_id)

    @staticmethod
    def _parse_json_response(text: str) -> dict[str, object]:
        try:
            payload = json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("LLMProvider returned invalid JSON for Role DNA generation.") from exc

        if not isinstance(payload, dict):
            raise ValueError("LLMProvider returned a non-object JSON payload for Role DNA generation.")
        return payload
