from abc import ABC, abstractmethod

from app.domain.ranking import RankingResult


class RankingRepository(ABC):
    """Persistence contract for generated rankings."""

    @abstractmethod
    def save_many(self, rankings: list[RankingResult]) -> list[RankingResult]:
        """Persist ranking results for a role/persona run."""

    @abstractmethod
    def list_by_role_id(self, role_id: str, persona: str | None = None) -> list[RankingResult]:
        """List rankings for a role, optionally filtered by persona."""
