from abc import ABC, abstractmethod

from app.domain.explanation import ExplanationProfile


class ExplanationRepository(ABC):
    """Persistence contract for generated explanation profiles."""

    @abstractmethod
    def save(self, profile: ExplanationProfile) -> ExplanationProfile:
        """Persist an explanation profile."""

    @abstractmethod
    def get_by_candidate_id(self, candidate_id: str) -> ExplanationProfile | None:
        """Fetch the latest explanation profile for a candidate."""
