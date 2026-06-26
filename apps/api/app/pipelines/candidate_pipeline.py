from typing import Protocol

from app.domain.candidate_twin import CandidateDigitalTwin, CandidateResume
from app.events import CandidateUploaded, DigitalTwinBuilt
from app.repositories.candidate_repository import CandidateRepository


class CandidateTwinService(Protocol):
    """Dependency boundary for building digital twins."""

    def build_from_resume_text(
        self,
        resume_text: str,
        resume_id: str | None = None,
        source_name: str | None = None,
    ) -> CandidateDigitalTwin:
        """Build a normalized candidate digital twin."""


class CandidatePipeline:
    """Orchestrates resume upload through Digital Twin construction."""

    def __init__(
        self,
        twin_service: CandidateTwinService,
        candidate_repository: CandidateRepository,
    ) -> None:
        self.twin_service = twin_service
        self.candidate_repository = candidate_repository

    def upload_resume(
        self,
        resume_text: str,
        source_name: str | None = None,
    ) -> tuple[CandidateResume, CandidateUploaded]:
        resume = self.candidate_repository.save_resume(
            CandidateResume(resume_text=resume_text, source_name=source_name)
        )
        return resume, CandidateUploaded(candidate_id=resume.resume_id)

    def run(
        self,
        resume_text: str | None = None,
        resume_id: str | None = None,
        source_name: str | None = None,
    ) -> tuple[CandidateDigitalTwin, DigitalTwinBuilt]:
        if resume_id:
            resume = self.candidate_repository.get_resume(resume_id)
            if resume is None:
                raise ValueError(f"Resume {resume_id} was not found.")
            resume_text = resume.resume_text
            source_name = resume.source_name
        elif resume_text:
            resume, _ = self.upload_resume(resume_text=resume_text, source_name=source_name)
            resume_id = resume.resume_id
        else:
            raise ValueError("Either resume_id or resume_text is required.")

        twin = self.twin_service.build_from_resume_text(
            resume_text=resume_text,
            resume_id=resume_id,
            source_name=source_name,
        )
        saved = self.candidate_repository.save(twin)
        return saved, DigitalTwinBuilt(candidate_id=saved.candidate_id)
