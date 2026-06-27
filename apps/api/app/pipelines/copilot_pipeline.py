from app.domain.copilot import CopilotDraftResponse
from app.modules.copilot.service import CopilotService
from app.repositories import CandidateRepository, EvaluationRepository, RoleDNARepository


class CopilotPipeline:
    def __init__(
        self,
        copilot_service: CopilotService,
        candidate_repository: CandidateRepository,
        role_repository: RoleDNARepository,
        evaluation_repository: EvaluationRepository,
    ):
        self.copilot_service = copilot_service
        self.candidate_repository = candidate_repository
        self.role_repository = role_repository
        self.evaluation_repository = evaluation_repository

    def draft_email(self, candidate_id: str, role_id: str) -> CopilotDraftResponse:
        candidate = self.candidate_repository.get_by_candidate_id(candidate_id)
        if not candidate:
            raise ValueError(f"Candidate {candidate_id} not found.")

        role = self.role_repository.get_by_role_id(role_id)
        if not role:
            raise ValueError(f"Role {role_id} not found.")

        # In a real app we'd query by candidate_id and role_id, but here we can just re-evaluate or use the latest.
        # Let's get all evaluations for candidate and find the one for the role.
        # For simplicity in this demo, let's assume the evaluation_repository can find by candidate_id and role_id.
        evaluations = self.evaluation_repository.list_by_role_id(role_id)
        evaluation = next((e for e in evaluations if e.candidate_id == candidate_id), None)
        
        if not evaluation:
            raise ValueError(f"Evaluation for candidate {candidate_id} and role {role_id} not found.")
            
        return self.copilot_service.draft_email(candidate.name, role.role_title, evaluation)
