from pydantic import BaseModel

from app.domain.ranking import RankingResult


class RankingListResponse(BaseModel):
    """API response for generated rankings."""

    role_id: str
    rankings: list[RankingResult]
