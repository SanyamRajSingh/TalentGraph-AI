from app.domain.explanation import ExplanationProfile
from app.domain.ranking import HiringPersona, RankingResult
from app.modules.explanations import ExplanationService
from app.repositories import CandidateRepository, EvaluationRepository, RankingRepository, RoleDNARepository


class ExplanationPipeline:
    """Loads candidate context and orchestrates explanation generation."""

    def __init__(
        self,
        explanation_service: ExplanationService,
        role_repository: RoleDNARepository,
        candidate_repository: CandidateRepository,
        evaluation_repository: EvaluationRepository,
        ranking_repository: RankingRepository,
    ) -> None:
        self.explanation_service = explanation_service
        self.role_repository = role_repository
        self.candidate_repository = candidate_repository
        self.evaluation_repository = evaluation_repository
        self.ranking_repository = ranking_repository

    def run(
        self,
        role_id: str,
        candidate_id: str,
        persona: HiringPersona | None = None,
    ) -> ExplanationProfile:
        role = self.role_repository.get_by_role_id(role_id)
        if role is None:
            raise ValueError(f"Role DNA {role_id} not found.")

        candidate = self.candidate_repository.get_by_candidate_id(candidate_id)
        if candidate is None:
            raise ValueError(f"Candidate {candidate_id} not found.")

        evaluation = next(
            (
                item
                for item in self.evaluation_repository.list_by_role_id(role_id)
                if item.candidate_id == candidate_id
            ),
            None,
        )
        if evaluation is None:
            raise ValueError(f"Evaluation for candidate {candidate_id} and role {role_id} not found.")

        ranking = self._find_ranking(role_id=role_id, candidate_id=candidate_id, persona=persona)
        if ranking is None:
            raise ValueError(f"Ranking for candidate {candidate_id} and role {role_id} not found.")

        return self.explanation_service.generate(role, candidate, evaluation, ranking)

    def _find_ranking(
        self,
        role_id: str,
        candidate_id: str,
        persona: HiringPersona | None,
    ) -> RankingResult | None:
        rankings = self.ranking_repository.list_by_role_id(
            role_id,
            persona=persona.value if persona is not None else None,
        )
        return next((ranking for ranking in rankings if ranking.candidate_id == candidate_id), None)
