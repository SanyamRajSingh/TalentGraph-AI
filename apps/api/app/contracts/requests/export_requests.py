from pydantic import BaseModel

from app.domain.ranking import HiringPersona


class ExportRankingsRequest(BaseModel):
    role_id: str
    persona: HiringPersona | None = None
