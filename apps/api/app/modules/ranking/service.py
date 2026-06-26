from app.domain.evaluation import EvaluationBundle
from app.domain.ranking import HiringPersona, RankingResult
from app.modules.recruiter_brain.persona_engine import PersonaEngine
from app.repositories.evaluation_repository import EvaluationRepository
from app.repositories.ranking_repository import RankingRepository


class RankingService:
    """Ranks candidates from existing EvaluationBundles using persona weights."""

    def __init__(
        self,
        evaluation_repository: EvaluationRepository,
        ranking_repository: RankingRepository,
        persona_engine: PersonaEngine | None = None,
    ) -> None:
        self.evaluation_repository = evaluation_repository
        self.ranking_repository = ranking_repository
        self.persona_engine = persona_engine or PersonaEngine()

    def rank(self, role_id: str, persona: HiringPersona) -> list[RankingResult]:
        evaluations = self.evaluation_repository.list_by_role_id(role_id)
        rankings = self._rank_evaluations(role_id=role_id, evaluations=evaluations, persona=persona)
        return self.ranking_repository.save_many(rankings)

    def _rank_evaluations(
        self,
        role_id: str,
        evaluations: list[EvaluationBundle],
        persona: HiringPersona,
    ) -> list[RankingResult]:
        scored = [
            RankingResult(
                candidate_id=evaluation.candidate_id,
                role_id=role_id,
                rank=1,
                persona=persona,
                score=self.persona_engine.score(evaluation, persona),
                confidence=evaluation.overall_confidence,
                evaluation_id=evaluation.evaluation_id,
            )
            for evaluation in evaluations
        ]
        scored.sort(key=lambda ranking: (-ranking.score, -ranking.confidence, ranking.candidate_id))
        return [
            ranking.model_copy(update={"rank": index + 1})
            for index, ranking in enumerate(scored)
        ]
