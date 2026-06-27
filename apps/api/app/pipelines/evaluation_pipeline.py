from typing import Protocol

from app.domain.evaluation import EvaluationBundle
from app.repositories.candidate_repository import CandidateRepository
from app.repositories.evaluation_repository import EvaluationRepository
from app.repositories.role_dna_repository import RoleDNARepository


class EvaluationServiceProtocol(Protocol):
    def evaluate(self, role: object, candidate: object) -> EvaluationBundle:
        """Evaluate a candidate against a role."""


class EvaluationPipeline:
    """Orchestrates candidate-role evaluation and persistence."""

    def __init__(
        self,
        evaluation_service: EvaluationServiceProtocol,
        evaluation_repository: EvaluationRepository,
        role_repository: RoleDNARepository,
        candidate_repository: CandidateRepository,
    ) -> None:
        self.evaluation_service = evaluation_service
        self.evaluation_repository = evaluation_repository
        self.role_repository = role_repository
        self.candidate_repository = candidate_repository

    def run(self, role_id: str, candidate_id: str) -> EvaluationBundle:
        role = self.role_repository.get_by_role_id(role_id)
        if role is None:
            raise ValueError(f"Role DNA {role_id} not found.")
        candidate = self.candidate_repository.get_by_candidate_id(candidate_id)
        if candidate is None:
            raise ValueError(f"Candidate {candidate_id} not found.")

        bundle = self.evaluation_service.evaluate(role, candidate)
        saved_bundle = self.evaluation_repository.save(bundle)
        
        # Phase 1: Tracking evaluations
        candidate.evaluations_history.append(saved_bundle.evaluation_id)
        
        # Add a timeline entry for the evaluation
        from datetime import datetime
        from app.domain.candidate_twin import CandidateTimelineEntry
        candidate.timeline.append(CandidateTimelineEntry(
            year=datetime.now().year,
            event=f"Evaluated against role: {role.role_title}"
        ))
        
        self.candidate_repository.save(candidate)
        
        return saved_bundle
