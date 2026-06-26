from abc import ABC, abstractmethod

from app.domain.candidate_twin import CandidateDigitalTwin, CandidateResume


class CandidateRepository(ABC):
    """Persistence contract for candidate records and digital twins."""

    @abstractmethod
    def save_resume(self, resume: CandidateResume) -> CandidateResume:
        """Persist resume text input."""

    @abstractmethod
    def get_resume(self, resume_id: str) -> CandidateResume | None:
        """Fetch resume text input."""

    @abstractmethod
    def save(self, twin: CandidateDigitalTwin) -> CandidateDigitalTwin:
        """Persist a candidate digital twin."""

    @abstractmethod
    def get_by_candidate_id(self, candidate_id: str) -> CandidateDigitalTwin | None:
        """Fetch a candidate digital twin by candidate identifier."""

    @abstractmethod
    def list_candidates(self) -> list[CandidateDigitalTwin]:
        """List persisted candidate digital twins."""
