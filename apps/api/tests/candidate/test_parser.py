from app.modules.candidates.local_parser_provider import LocalResumeParserProvider


def test_local_parser_extracts_candidate_fields() -> None:
    parser = LocalResumeParserProvider()

    parsed = parser.parse_resume_text(
        """# Maya Rao
Email: maya@example.com
Phone: +91 98765 43210
Location: Bengaluru

## Skills
- Python
- SQL
- Machine Learning

## Projects
- 2023 Built ML Project
"""
    )

    fields = parsed.structured_fields
    assert fields["name"] == "Maya Rao"
    assert fields["email"] == "maya@example.com"
    assert fields["phone"] == "+91 98765 43210"
    assert "Python" in fields["skills"]
    assert "Machine Learning" in fields["domains"]
    assert fields["years"] == [2023]
