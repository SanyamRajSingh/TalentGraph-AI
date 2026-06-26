from sqlalchemy.orm import Session

from app.domain.candidate_twin import CandidateDigitalTwin, CandidateResume
from app.repositories.candidate_repository import CandidateRepository


class PostgresCandidateRepository(CandidateRepository):
    """PostgreSQL candidate repository skeleton.

    Concrete table mappings and migrations are intentionally deferred. Module 2
    uses the repository interface and in-memory implementation for testable demo
    behavior.
    """

    def __init__(self, session: Session) -> None:
        self.session = session

    def save_resume(self, resume: CandidateResume) -> CandidateResume:
        raise NotImplementedError("PostgreSQL resume persistence is not implemented in Module 2.")

    def get_resume(self, resume_id: str) -> CandidateResume | None:
        raise NotImplementedError("PostgreSQL resume lookup is not implemented in Module 2.")

    def save(self, twin: CandidateDigitalTwin) -> CandidateDigitalTwin:
        raise NotImplementedError("PostgreSQL candidate persistence is not implemented in Module 2.")

    def get_by_candidate_id(self, candidate_id: str) -> CandidateDigitalTwin | None:
        raise NotImplementedError("PostgreSQL candidate lookup is not implemented in Module 2.")

    def list_candidates(self) -> list[CandidateDigitalTwin]:
        raise NotImplementedError("PostgreSQL candidate listing is not implemented in Module 2.")
