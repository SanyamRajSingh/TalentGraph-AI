from pydantic import BaseModel

from app.domain.candidate_twin import CandidateDigitalTwin, CandidateResume


class UploadCandidateResponse(BaseModel):
    """API response for uploaded resume text."""

    resume_id: str
    resume: CandidateResume


class CandidateTwinResponse(BaseModel):
    """API response for candidate digital twin data."""

    candidate_id: str
    twin: CandidateDigitalTwin


class CandidateListResponse(BaseModel):
    """API response for generated candidate digital twins."""

    items: list[CandidateDigitalTwin]


class PaginatedCandidateListResponse(BaseModel):
    """API response for paginated candidate digital twins."""

    items: list[CandidateDigitalTwin]
    total: int
    page: int
    page_size: int

