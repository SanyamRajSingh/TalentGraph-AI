from pydantic import BaseModel


class EvaluateRequest(BaseModel):
    role_id: str
    candidate_id: str
