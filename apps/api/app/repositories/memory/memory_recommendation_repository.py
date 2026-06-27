from app.domain.recommendation import RecommendationResult
from app.repositories.recommendation_repository import RecommendationRepository

class InMemoryRecommendationRepository(RecommendationRepository):
    def __init__(self):
        self._db: dict[str, RecommendationResult] = {}

    def _key(self, candidate_id: str, role_id: str) -> str:
        return f"{candidate_id}::{role_id}"

    def save(self, recommendation: RecommendationResult) -> RecommendationResult:
        self._db[self._key(recommendation.candidate_id, recommendation.role_id)] = recommendation
        return recommendation

    def get(self, candidate_id: str, role_id: str) -> RecommendationResult | None:
        return self._db.get(self._key(candidate_id, role_id))
