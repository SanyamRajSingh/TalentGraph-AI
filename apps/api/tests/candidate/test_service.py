from app.modules.candidates.service import CandidateDigitalTwinService
from app.providers.parser_provider import ParsedCandidateInput, ParserProvider


class MockParserProvider(ParserProvider):
    def parse_resume(self, content: bytes, filename: str) -> ParsedCandidateInput:
        return self.parse_resume_text(content.decode(), filename)

    def parse_resume_text(self, resume_text: str, source_name: str | None = None) -> ParsedCandidateInput:
        return ParsedCandidateInput(
            raw_text=resume_text,
            source_name=source_name,
            structured_fields={
                "name": "Sam Builder",
                "email": "sam@example.com",
                "phone": "+1 555 0100",
                "location": "Remote",
                "skills": ["Python", "FastAPI", "SQL"],
                "technologies": ["Python", "FastAPI", "PostgreSQL"],
                "projects": ["Built API platform"],
                "experiences": ["2024 Backend Engineer"],
                "certifications": ["Python course"],
                "achievements": ["Shipped production service"],
                "domains": ["Backend Systems"],
                "years": [2023, 2024],
            },
        )

    def parse_structured_profile(self, payload: dict[str, object]) -> ParsedCandidateInput:
        return ParsedCandidateInput(raw_text="", structured_fields=payload)


def test_candidate_service_builds_normalized_digital_twin() -> None:
    service = CandidateDigitalTwinService(parser_provider=MockParserProvider())

    twin = service.build_from_resume_text(
        "2023 learned Python. 2024 built and shipped API platform.",
        resume_id="resume_123",
    )

    assert twin.resume_id == "resume_123"
    assert twin.name == "Sam Builder"
    assert twin.email == "sam@example.com"
    assert twin.skills == ["Python", "FastAPI", "SQL"]
    assert len(twin.timeline) == 2
    assert 0 <= twin.technical_depth <= 100
    assert 0 <= twin.confidence <= 100
    assert twin.growth_stage
    assert twin.reasoning
