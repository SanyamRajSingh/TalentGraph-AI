"""PostgreSQL implementation of CandidateRepository."""

from sqlalchemy.orm import Session

from app.db.models import CandidateResumeRow, CandidateRow
from app.domain.candidate_twin import CandidateDigitalTwin, CandidateResume
from app.repositories.candidate_repository import CandidateRepository


class PostgresCandidateRepository(CandidateRepository):
    """PostgreSQL-backed candidate repository using SQLAlchemy ORM."""

    def __init__(self, session: Session) -> None:
        self.session = session

    # ------------------------------------------------------------------ resumes

    def save_resume(self, resume: CandidateResume) -> CandidateResume:
        existing = (
            self.session.query(CandidateResumeRow)
            .filter_by(resume_id=resume.resume_id)
            .first()
        )
        if existing:
            existing.resume_text = resume.resume_text
            existing.source_name = resume.source_name
        else:
            row = CandidateResumeRow(
                resume_id=resume.resume_id,
                resume_text=resume.resume_text,
                source_name=resume.source_name,
            )
            self.session.add(row)
        self.session.commit()
        return resume

    def get_resume(self, resume_id: str) -> CandidateResume | None:
        row = self.session.query(CandidateResumeRow).filter_by(resume_id=resume_id).first()
        if row is None:
            return None
        return CandidateResume(
            resume_id=row.resume_id,
            resume_text=row.resume_text,
            source_name=row.source_name,
        )

    # ------------------------------------------------------------------ twins

    def save(self, twin: CandidateDigitalTwin) -> CandidateDigitalTwin:
        existing = (
            self.session.query(CandidateRow)
            .filter_by(candidate_id=twin.candidate_id)
            .first()
        )
        payload = twin.model_dump(mode="json")
        if existing:
            existing.name = twin.name
            existing.growth_stage = twin.growth_stage.value if hasattr(twin.growth_stage, "value") else str(twin.growth_stage)
            existing.confidence = twin.confidence
            existing.payload = payload
        else:
            row = CandidateRow(
                candidate_id=twin.candidate_id,
                resume_id=twin.resume_id,
                name=twin.name,
                growth_stage=twin.growth_stage.value if hasattr(twin.growth_stage, "value") else str(twin.growth_stage),
                confidence=twin.confidence,
                payload=payload,
            )
            self.session.add(row)
        self.session.commit()
        return twin

    def get_by_candidate_id(self, candidate_id: str) -> CandidateDigitalTwin | None:
        row = self.session.query(CandidateRow).filter_by(candidate_id=candidate_id).first()
        if row is None:
            return None
        return CandidateDigitalTwin.model_validate(row.payload)

    def list_candidates(self) -> list[CandidateDigitalTwin]:
        rows = self.session.query(CandidateRow).order_by(CandidateRow.created_at.desc()).all()
        return [CandidateDigitalTwin.model_validate(r.payload) for r in rows]

    def search_candidates(self, filters) -> object:
        """Search and filter candidate digital twins (PostgreSQL)."""
        from app.repositories.candidate_repository import PaginatedCandidateList
        
        query = self.session.query(CandidateRow)
        
        # SQL filters for native columns
        if filters.growth_stage:
            query = query.filter(CandidateRow.growth_stage.ilike(filters.growth_stage))
            
        if filters.min_confidence is not None:
            query = query.filter(CandidateRow.confidence >= filters.min_confidence)
            
        # SQL sorting
        if filters.sort_by == "name":
            query = query.order_by(CandidateRow.name.asc())
        elif filters.sort_by == "confidence":
            query = query.order_by(CandidateRow.confidence.desc())
        else: # created_at or default
            query = query.order_by(CandidateRow.created_at.desc())
            
        # Execute query
        rows = query.all()
        results = [CandidateDigitalTwin.model_validate(r.payload) for r in rows]
        
        # In-memory filters for complex logic and JSON payload data (to keep it cross-dialect compatible with SQLite tests)
        if filters.search:
            q = filters.search.lower()
            results = [r for r in results if q in r.name.lower() or (r.current_role and q in r.current_role.lower())]
            
        if filters.skills:
            req_skills = {s.lower() for s in filters.skills}
            results = [r for r in results if req_skills.issubset({s.lower() for s in r.skills})]
            
        # Pagination
        total = len(results)
        start = (filters.page - 1) * filters.page_size
        end = start + filters.page_size
        
        return PaginatedCandidateList(
            items=results[start:end],
            total=total,
            page=filters.page,
            page_size=filters.page_size,
        )

