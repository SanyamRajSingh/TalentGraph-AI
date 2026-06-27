from app.domain.explanation import ExplanationProfile
from app.repositories.explanation_repository import ExplanationRepository


class InMemoryExplanationRepository(ExplanationRepository):
    """Process-local explanation repository for tests and demo runs."""

    def __init__(self) -> None:
        self._profiles: dict[str, ExplanationProfile] = {}

    def save(self, profile: ExplanationProfile) -> ExplanationProfile:
        self._profiles[profile.candidate_id] = profile
        return profile

    def get_by_candidate_id(self, candidate_id: str) -> ExplanationProfile | None:
        return self._profiles.get(candidate_id)
