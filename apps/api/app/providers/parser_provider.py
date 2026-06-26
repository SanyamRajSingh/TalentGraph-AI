from abc import ABC, abstractmethod

from pydantic import BaseModel, Field


class ParsedCandidateInput(BaseModel):
    """Provider-neutral parsed candidate payload."""

    raw_text: str
    structured_fields: dict[str, object] = Field(default_factory=dict)
    source_name: str | None = None


class ParserProvider(ABC):
    """Abstract boundary for PDF and structured-profile parsing."""

    @abstractmethod
    def parse_resume(self, content: bytes, filename: str) -> ParsedCandidateInput:
        """Parse resume bytes into a normalized intermediate payload."""

    @abstractmethod
    def parse_resume_text(self, resume_text: str, source_name: str | None = None) -> ParsedCandidateInput:
        """Parse resume text into a normalized intermediate payload."""

    @abstractmethod
    def parse_structured_profile(self, payload: dict[str, object]) -> ParsedCandidateInput:
        """Normalize structured candidate input."""
