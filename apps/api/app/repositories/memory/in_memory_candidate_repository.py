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

    def search_candidates(self, filters) -> object:
        """Search and filter candidate digital twins (in-memory)."""
        from app.repositories.candidate_repository import PaginatedCandidateList
        
        results = list(self._twins.values())
        
        if filters.search:
            q = filters.search.lower()
            results = [r for r in results if q in r.name.lower() or (r.current_role and q in r.current_role.lower())]
            
        if filters.skills:
            req_skills = {s.lower() for s in filters.skills}
            results = [r for r in results if req_skills.issubset({s.lower() for s in r.skills})]
            
        if filters.growth_stage:
            results = [r for r in results if r.growth_stage.value.lower() == filters.growth_stage.lower() or str(r.growth_stage).lower() == filters.growth_stage.lower()]
            
        if filters.min_confidence is not None:
            results = [r for r in results if r.confidence >= filters.min_confidence]
            
        # Sorting
        if filters.sort_by == "name":
            results.sort(key=lambda x: x.name.lower())
        elif filters.sort_by == "confidence":
            results.sort(key=lambda x: x.confidence, reverse=True)
        else: # created_at or default
            # Since we don't have created_at on domain models, we just rely on insertion order reversed
            results.reverse()
            
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

