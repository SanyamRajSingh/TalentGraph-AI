from enum import StrEnum

from pydantic import BaseModel, Field

Score = int


class HiringPersona(StrEnum):
    STARTUP_FOUNDER = "startup_founder"
    ENTERPRISE_RECRUITER = "enterprise_recruiter"
    RESEARCH_TEAM = "research_team"


class RankingResult(BaseModel):
    """Canonical ranking output for a role/persona run."""

    candidate_id: str
    role_id: str
    rank: int = Field(ge=1)
    persona: HiringPersona
    score: Score = Field(ge=0, le=100)
    confidence: Score = Field(ge=0, le=100)
    evaluation_id: str
