import dataclasses
from abc import ABC, abstractmethod

from app.domain.candidate_twin import CandidateDigitalTwin, CandidateResume


@dataclasses.dataclass
class CandidateFilter:
    search: str | None = None
    skills: list[str] | None = None
    growth_stage: str | None = None
    min_confidence: int | None = None
    sort_by: str = "created_at"  # 'created_at', 'confidence', 'name'
    page: int = 1
    page_size: int = 20


@dataclasses.dataclass
class PaginatedCandidateList:
    items: list[CandidateDigitalTwin]
    total: int
    page: int
    page_size: int


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

    @abstractmethod
    def get_by_email(self, email: str) -> CandidateDigitalTwin | None:
        """Fetch a candidate digital twin by email address."""

    @abstractmethod
    def search_candidates(self, filters: CandidateFilter) -> PaginatedCandidateList:
        """Search and filter candidate digital twins."""

