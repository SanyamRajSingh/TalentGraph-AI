from datetime import UTC, datetime

from pydantic import BaseModel, Field


class ExplanationProfile(BaseModel):
    """Human-readable explanation for one ranked candidate."""

    candidate_id: str
    role_id: str
    ranking_position: int = Field(ge=1)
    strengths: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    reasoning: list[str] = Field(default_factory=list)
    counterfactuals: list[str] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
