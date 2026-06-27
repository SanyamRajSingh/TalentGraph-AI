from pydantic import BaseModel
from app.domain.recommendation import RecommendationResult


class RecommendResponse(BaseModel):
    recommendation: RecommendationResult
