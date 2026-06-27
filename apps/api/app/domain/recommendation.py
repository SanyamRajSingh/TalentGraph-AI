from enum import StrEnum
from pydantic import BaseModel, Field


class RecommendationLabel(StrEnum):
    STRONG_HIRE = "STRONG_HIRE"
    HIRE = "HIRE"
    GROWTH_HIRE = "GROWTH_HIRE"
    BORDERLINE = "BORDERLINE"
    NO_HIRE = "NO_HIRE"


class RecommendationResult(BaseModel):
    """Final hiring recommendation for a candidate regarding a specific role."""

    candidate_id: str
    role_id: str
    label: RecommendationLabel
    reason: str
    supporting_evidence: list[str] = Field(default_factory=list)
