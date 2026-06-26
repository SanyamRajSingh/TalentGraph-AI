from app.domain.candidate_twin import CandidateDigitalTwin, CandidateResume
from app.repositories.memory import InMemoryCandidateRepository


def test_memory_candidate_repository_persists_resumes_and_twins() -> None:
    repository = InMemoryCandidateRepository()

    resume = repository.save_resume(CandidateResume(resume_text="Python SQL resume"))
    twin = repository.save(CandidateDigitalTwin(resume_id=resume.resume_id, name="Test Candidate"))

    assert repository.get_resume(resume.resume_id) == resume
    assert repository.get_by_candidate_id(twin.candidate_id) == twin
    assert repository.list_candidates() == [twin]
