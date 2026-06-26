from pydantic import BaseModel

from app.domain.ranking import RankingResult


class RankingResponse(BaseModel):
    role_id: str
    persona: str
    rankings: list[RankingResult]
