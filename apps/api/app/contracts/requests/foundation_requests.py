from pydantic import BaseModel


class BuildGraphRequest(BaseModel):
    role_id: str | None = None
    candidate_id: str | None = None


class GenerateEmbeddingsRequest(BaseModel):
    role_id: str | None = None
    candidate_id: str | None = None
