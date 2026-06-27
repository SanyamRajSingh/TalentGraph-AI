from pydantic import BaseModel


class CopilotDraftRequest(BaseModel):
    candidate_id: str
    role_id: str


class CopilotDraftResponse(BaseModel):
    subject: str
    body: str


class CopilotChatRequest(BaseModel):
    message: str
    candidate_id: str | None = None
    role_id: str | None = None


class CopilotChatResponse(BaseModel):
    intent: str
    answer: str
    follow_up_questions: list[str]
