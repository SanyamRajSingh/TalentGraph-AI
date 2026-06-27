from pydantic import BaseModel


class RecommendRequest(BaseModel):
    role_id: str
    candidate_id: str
