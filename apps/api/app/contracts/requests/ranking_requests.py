from pydantic import BaseModel

from app.domain.ranking import HiringPersona


class RankCandidatesRequest(BaseModel):
    """Request body for candidate ranking."""

    role_id: str
    candidate_ids: list[str]
    persona: HiringPersona = HiringPersona.STARTUP_FOUNDER
