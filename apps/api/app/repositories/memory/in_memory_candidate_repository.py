from app.domain.candidate_twin import CandidateDigitalTwin, CandidateResume
from app.repositories.candidate_repository import CandidateRepository


class InMemoryCandidateRepository(CandidateRepository):
    """Process-local candidate repository for tests and hackathon demo runs."""

    def __init__(self) -> None:
        self._resumes: dict[str, CandidateResume] = {}
        self._twins: dict[str, CandidateDigitalTwin] = {}

    def save_resume(self, resume: CandidateResume) -> CandidateResume:
        self._resumes[resume.resume_id] = resume
        return resume

    def get_resume(self, resume_id: str) -> CandidateResume | None:
        return self._resumes.get(resume_id)

    def save(self, twin: CandidateDigitalTwin) -> CandidateDigitalTwin:
        self._twins[twin.candidate_id] = twin
        return twin

    def get_by_candidate_id(self, candidate_id: str) -> CandidateDigitalTwin | None:
        return self._twins.get(candidate_id)

    def list_candidates(self) -> list[CandidateDigitalTwin]:
        return list(self._twins.values())
