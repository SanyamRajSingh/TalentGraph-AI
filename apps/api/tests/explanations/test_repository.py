from app.domain.explanation import ExplanationProfile
from app.repositories.memory import InMemoryExplanationRepository


def test_in_memory_explanation_repository_persists_by_candidate_id() -> None:
    repository = InMemoryExplanationRepository()
    profile = ExplanationProfile(
        candidate_id="candidate_explain",
        role_id="role_explain",
        ranking_position=1,
        strengths=["Strong Python alignment."],
    )

    repository.save(profile)

    assert repository.get_by_candidate_id("candidate_explain") == profile
    assert repository.get_by_candidate_id("missing") is None
