from pydantic import BaseModel, Field


class UploadJobRequest(BaseModel):
    """Request body for creating a job input."""

    job_description: str = Field(min_length=1)
    source_name: str | None = None


class GenerateRoleDNARequest(BaseModel):
    """Request body for Role DNA generation."""

    job_id: str | None = None
    job_description: str | None = Field(default=None, min_length=1)
