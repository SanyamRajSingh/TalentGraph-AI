from app.domain.ranking import HiringPersona, RankingResult
from app.pipelines.ranking_pipeline import RankingPipeline


class MockRankingService:
    def rank(self, role_id: str, persona: HiringPersona) -> list[RankingResult]:
        return [
            RankingResult(
                candidate_id="candidate_pipeline",
                role_id=role_id,
                rank=1,
                persona=persona,
                score=91,
                confidence=82,
                evaluation_id="evaluation_pipeline",
            )
        ]


def test_ranking_pipeline_delegates_to_service() -> None:
    rankings = RankingPipeline(ranking_service=MockRankingService()).run(
        role_id="role_pipeline",
        persona=HiringPersona.ENTERPRISE_RECRUITER,
    )

    assert rankings[0].rank == 1
    assert rankings[0].persona == HiringPersona.ENTERPRISE_RECRUITER
