from pydantic import BaseModel, Field


class UploadCandidateRequest(BaseModel):
    """Request body for uploading resume text."""

    resume_text: str = Field(min_length=1)
    source_name: str | None = None


class BuildDigitalTwinRequest(BaseModel):
    """Request body for building a Candidate Digital Twin."""

    resume_id: str | None = None
    resume_text: str | None = Field(default=None, min_length=1)
    source_name: str | None = None


class StructuredCandidateRequest(BaseModel):
    """Request body for structured candidate input."""

    source_name: str | None = None
    profile: dict[str, object] = Field(default_factory=dict)
