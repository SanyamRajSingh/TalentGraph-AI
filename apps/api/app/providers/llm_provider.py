from abc import ABC, abstractmethod

from pydantic import BaseModel, Field


class LLMResponse(BaseModel):
    """Provider-neutral LLM response envelope."""

    text: str
    model: str
    metadata: dict[str, object] = Field(default_factory=dict)


class LLMProvider(ABC):
    """Abstract boundary for OpenAI or demo/mock LLM calls."""

    @abstractmethod
    def complete_json(
        self,
        system_prompt: str,
        user_prompt: str,
        schema_name: str,
    ) -> LLMResponse:
        """Return a JSON-oriented LLM response without binding callers to a vendor."""
