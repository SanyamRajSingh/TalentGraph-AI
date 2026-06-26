from pydantic import BaseModel, Field


class CounterfactualSuggestion(BaseModel):
    """A candidate improvement that could materially change ranking."""

    suggestion: str
    estimated_rank_after: int | None = Field(default=None, ge=1)
    rationale: str | None = None


class CandidateExplanation(BaseModel):
    """Human-readable explanation for one candidate ranking."""

    candidate_id: str
    role_id: str
    why_ranked_here: list[str] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    counterfactuals: list[CounterfactualSuggestion] = Field(default_factory=list)
