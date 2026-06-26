from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4

from pydantic import BaseModel, Field

Score = int


class GrowthStage(StrEnum):
    EXPLORER = "Explorer"
    BUILDER = "Builder"
    EMERGING_LEADER = "Emerging Leader"
    TECHNICAL_SPECIALIST = "Technical Specialist"
    RESEARCHER = "Researcher"
    OPERATOR = "Operator"
    HYBRID = "Hybrid"


class CandidateResume(BaseModel):
    """Persisted resume text input."""

    resume_id: str = Field(default_factory=lambda: f"resume_{uuid4().hex[:12]}")
    resume_text: str = Field(min_length=1)
    source_name: str | None = None


class CandidateTimelineEntry(BaseModel):
    """One deterministic candidate timeline point."""

    year: int
    event: str


class CandidateDigitalTwin(BaseModel):
    """Canonical rich candidate profile derived from resume text."""

    candidate_id: str = Field(default_factory=lambda: f"candidate_{uuid4().hex[:12]}")
    resume_id: str | None = None
    name: str = "Unknown Candidate"
    email: str | None = None
    phone: str | None = None
    location: str | None = None
    skills: list[str] = Field(default_factory=list)
    technologies: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    experiences: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    achievements: list[str] = Field(default_factory=list)
    domains: list[str] = Field(default_factory=list)
    timeline: list[CandidateTimelineEntry] = Field(default_factory=list)
    technical_depth: Score = Field(default=50, ge=0, le=100)
    learning_velocity: Score = Field(default=50, ge=0, le=100)
    leadership: Score = Field(default=50, ge=0, le=100)
    ownership: Score = Field(default=50, ge=0, le=100)
    communication: Score = Field(default=50, ge=0, le=100)
    project_complexity: Score = Field(default=50, ge=0, le=100)
    collaboration: Score = Field(default=50, ge=0, le=100)
    consistency: Score = Field(default=50, ge=0, le=100)
    growth_stage: GrowthStage = GrowthStage.EXPLORER
    confidence: Score = Field(default=70, ge=0, le=100)
    reasoning: list[str] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    processing_time_ms: int = Field(default=0, ge=0)
    version: str = "candidate-twin-v1"
