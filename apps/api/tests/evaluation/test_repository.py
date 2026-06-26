from app.domain.evaluation import EvaluationBundle
from app.repositories.memory import InMemoryEvaluationRepository


def test_memory_evaluation_repository_persists_and_lists() -> None:
    repository = InMemoryEvaluationRepository()
    bundle = EvaluationBundle(candidate_id="candidate_1", role_id="role_1", overall_match=80)

    repository.save(bundle)

    assert repository.get(bundle.evaluation_id) == bundle
    assert repository.list_by_role_id("role_1") == [bundle]
