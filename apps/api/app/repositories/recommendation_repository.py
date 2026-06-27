from abc import ABC, abstractmethod
from app.domain.recommendation import RecommendationResult

class RecommendationRepository(ABC):
    """Persistence contract for candidate recommendations."""

    @abstractmethod
    def save(self, recommendation: RecommendationResult) -> RecommendationResult:
        """Persist a recommendation."""

    @abstractmethod
    def get(self, candidate_id: str, role_id: str) -> RecommendationResult | None:
        """Fetch a recommendation by candidate and role."""
