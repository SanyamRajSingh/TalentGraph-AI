from __future__ import annotations

from pydantic import BaseModel, Field


class DimensionComparison(BaseModel):
    """Per-dimension score comparison between two candidates."""
    dimension: str
    candidate_a_score: int
    candidate_b_score: int
    winner: str  # "A", "B", or "TIE"
    delta: int   # candidate_a - candidate_b


class ComparisonMatrix(BaseModel):
    """Side-by-side comparison matrix of two candidates against a role."""
    candidate_a_id: str
    candidate_b_id: str
    candidate_a_name: str
    candidate_b_name: str
    role_id: str
    role_title: str
    dimensions: list[DimensionComparison] = Field(default_factory=list)
    overall_winner: str  # "A", "B", or "TIE"
    summary: str
    recommendation: str
    skill_overlap: list[str] = Field(default_factory=list)
    a_unique_skills: list[str] = Field(default_factory=list)
    b_unique_skills: list[str] = Field(default_factory=list)
