from pydantic import BaseModel

from app.domain.role_dna import RoleDNAProfile, RoleJob


class UploadJobResponse(BaseModel):
    """API response for persisted job input."""

    job_id: str
    job: RoleJob


class RoleDNAResponse(BaseModel):
    """API response for Role DNA data."""

    role_id: str
    job_id: str | None = None
    role_dna: RoleDNAProfile


class RoleDNAListResponse(BaseModel):
    """API response for generated Role DNA profiles."""

    items: list[RoleDNAProfile]
