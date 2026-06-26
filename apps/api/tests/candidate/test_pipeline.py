from app.domain.candidate_twin import CandidateDigitalTwin
from app.pipelines.candidate_pipeline import CandidatePipeline
from app.repositories.memory import InMemoryCandidateRepository


class MockTwinService:
    def build_from_resume_text(
        self,
        resume_text: str,
        resume_id: str | None = None,
        source_name: str | None = None,
    ) -> CandidateDigitalTwin:
        return CandidateDigitalTwin(
            resume_id=resume_id,
            name="Pipeline Candidate",
            skills=["Python"],
            reasoning=["Built by mock service."],
        )


def test_candidate_pipeline_uploads_builds_and_persists() -> None:
    repository = InMemoryCandidateRepository()
    pipeline = CandidatePipeline(twin_service=MockTwinService(), candidate_repository=repository)

    resume, upload_event = pipeline.upload_resume("Python resume")
    twin, built_event = pipeline.run(resume_id=resume.resume_id)

    assert upload_event.candidate_id == resume.resume_id
    assert built_event.candidate_id == twin.candidate_id
    assert repository.get_resume(resume.resume_id) == resume
    assert repository.get_by_candidate_id(twin.candidate_id) == twin
