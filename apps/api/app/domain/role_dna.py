from uuid import uuid4

from pydantic import BaseModel, Field

Score = int


class RoleJob(BaseModel):
    """Persisted job description input."""

    job_id: str = Field(default_factory=lambda: f"job_{uuid4().hex[:12]}")
    job_description: str = Field(min_length=1)
    source_name: str | None = None


class WorkEnvironmentAttributes(BaseModel):
    """Normalized environmental signals inferred from a job description."""

    startup_vs_enterprise: Score = Field(default=50, ge=0, le=100)
    ambiguity_tolerance: Score = Field(default=50, ge=0, le=100)
    collaboration: Score = Field(default=50, ge=0, le=100)
    ownership: Score = Field(default=50, ge=0, le=100)
    communication: Score = Field(default=50, ge=0, le=100)


class RoleDNAProfile(BaseModel):
    """Canonical representation of what a role needs."""

    role_id: str = Field(default_factory=lambda: f"role_{uuid4().hex[:12]}")
    job_id: str | None = None
    role_title: str
    domain: str
    seniority: str
    role_archetype: str
    fingerprint: str
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    skill_importance: dict[str, Score] = Field(default_factory=dict)
    technical_depth: Score = Field(ge=0, le=100)
    problem_solving: Score = Field(ge=0, le=100)
    communication: Score = Field(ge=0, le=100)
    ownership: Score = Field(ge=0, le=100)
    leadership: Score = Field(ge=0, le=100)
    learning_agility: Score = Field(ge=0, le=100)
    ambiguity_tolerance: Score = Field(ge=0, le=100)
    collaboration: Score = Field(ge=0, le=100)
    startup_vs_enterprise_environment: Score = Field(ge=0, le=100)
    work_environment: WorkEnvironmentAttributes = Field(default_factory=WorkEnvironmentAttributes)
    weight_distribution: dict[str, Score] = Field(default_factory=dict)
    reasoning: list[str] = Field(default_factory=list)
    confidence: Score = Field(default=75, ge=0, le=100)
