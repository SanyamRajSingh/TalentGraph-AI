from uuid import uuid4

from pydantic import BaseModel, Field

Score = int


class EvaluatorResult(BaseModel):
    """Output contract for one evaluator module."""

    score: Score = Field(ge=0, le=100)
    confidence: Score = Field(ge=0, le=100)
    strengths: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    missing_signals: list[str] = Field(default_factory=list)
    ramp_up_estimate: str | None = None
    explanation: str = ""


class EvaluationBundle(BaseModel):
    """Grouped evaluator results for one candidate-role comparison."""

    evaluation_id: str = Field(default_factory=lambda: f"evaluation_{uuid4().hex[:12]}")
    candidate_id: str
    role_id: str
    technical: EvaluatorResult | None = None
    growth: EvaluatorResult | None = None
    domain: EvaluatorResult | None = None
    culture: EvaluatorResult | None = None
    overall_match: Score = Field(default=0, ge=0, le=100)
    overall_confidence: Score = Field(default=0, ge=0, le=100)
    narrative: str = ""
