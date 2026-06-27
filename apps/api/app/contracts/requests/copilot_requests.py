from pydantic import BaseModel

class CopilotDraftRequest(BaseModel):
    candidate_id: str
    role_id: str
