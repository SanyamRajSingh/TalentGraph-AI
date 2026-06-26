from pydantic import BaseModel

from app.domain.ranking import HiringPersona


class RankRequest(BaseModel):
    role_id: str
    persona: HiringPersona = HiringPersona.STARTUP_FOUNDER
