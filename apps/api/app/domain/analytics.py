from pydantic import BaseModel, Field

class TalentDistribution(BaseModel):
    """Distribution of candidates by growth stage."""
    growth_stage: str
    count: int

class SkillFrequency(BaseModel):
    """Frequency of extracted skills across candidates."""
    skill: str
    count: int

class AnalyticsOverview(BaseModel):
    """High-level analytics overview for the recruiter dashboard."""
    total_candidates: int
    total_roles: int
    total_evaluations: int
    average_confidence: float
    growth_stage_distribution: list[TalentDistribution] = Field(default_factory=list)
    top_skills: list[SkillFrequency] = Field(default_factory=list)
