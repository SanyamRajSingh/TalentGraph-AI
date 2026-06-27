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

    def upload_from_file(
        self,
        file_bytes: bytes,
        filename: str,
        content_type: str = "application/octet-stream",
    ) -> tuple[CandidateDigitalTwin, DigitalTwinBuilt]:
        """Parse an uploaded file (PDF, DOCX, or TXT) and build a Digital Twin.

        Dispatches to the correct parser based on file extension / content-type.
        Falls back to plain-text parsing for .txt and unknown types.
        """
        name_lower = filename.lower()
        is_pdf = name_lower.endswith(".pdf") or "pdf" in content_type
        is_docx = name_lower.endswith(".docx") or "wordprocessingml" in content_type

        if is_pdf:
            from app.providers.pdf_parser_provider import PdfParserProvider
            parsed = PdfParserProvider().parse_resume(file_bytes, filename)
        elif is_docx:
            from app.providers.docx_parser_provider import DocxParserProvider
            parsed = DocxParserProvider().parse_resume(file_bytes, filename)
        else:
            # TXT or unknown — decode bytes as UTF-8
            raw_text = file_bytes.decode("utf-8", errors="replace")
            from app.modules.candidates.local_parser_provider import LocalResumeParserProvider
            parsed = LocalResumeParserProvider().parse_resume_text(raw_text, source_name=filename)

        return self.run(resume_text=parsed.raw_text, source_name=filename)

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

        # Phase 1: Persistent Talent Memory - Merge with existing candidate by email
        if twin.email:
            existing = self.candidate_repository.get_by_email(twin.email)
            if existing:
                # Merge IDs and history
                twin.candidate_id = existing.candidate_id
                twin.resume_versions = existing.resume_versions.copy()
                twin.evaluations_history = existing.evaluations_history.copy()
                
                # Append new timeline entry
                from datetime import datetime
                from app.domain.candidate_twin import CandidateTimelineEntry
                year = datetime.now().year
                twin.timeline.append(CandidateTimelineEntry(year=year, event=f"Profile updated from {source_name or 'resume'}"))
        
        # Append this resume to history
        if resume:
            twin.resume_versions.append(resume)
            
        saved = self.candidate_repository.save(twin)
        return saved, DigitalTwinBuilt(candidate_id=saved.candidate_id)

