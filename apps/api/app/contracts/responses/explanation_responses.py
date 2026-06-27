from pydantic import BaseModel

from app.domain.explanation import ExplanationProfile


class ExplanationResponse(BaseModel):
    candidate_id: str
    role_id: str
    explanation: ExplanationProfile
