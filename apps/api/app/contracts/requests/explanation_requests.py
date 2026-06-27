from pydantic import BaseModel

from app.domain.ranking import HiringPersona


class GenerateExplanationRequest(BaseModel):
    role_id: str
    candidate_id: str
    persona: HiringPersona | None = None
