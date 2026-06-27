"""DOCX resume parser provider.

Uses python-docx to extract text from DOCX bytes.
Gracefully degrades to an empty-text stub if python-docx is not installed.
"""

from app.providers.parser_provider import ParsedCandidateInput, ParserProvider


class DocxParserProvider(ParserProvider):
    """Extract plain text from DOCX resume bytes using python-docx."""

    def parse_resume(self, content: bytes, filename: str) -> ParsedCandidateInput:
        try:
            import io
            from docx import Document

            doc = Document(io.BytesIO(content))
            paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
            raw_text = "\n".join(paragraphs).strip()
        except ImportError:
            raw_text = f"[DOCX parsing unavailable — python-docx not installed] filename={filename}"
        except Exception as exc:
            raw_text = f"[DOCX parse error: {exc}] filename={filename}"

        source_name = filename
        return self.parse_resume_text(raw_text, source_name=source_name)

    def parse_resume_text(self, resume_text: str, source_name: str | None = None) -> ParsedCandidateInput:
        """Delegate text parsing to the local parser for field extraction."""
        from app.modules.candidates.local_parser_provider import LocalResumeParserProvider
        return LocalResumeParserProvider().parse_resume_text(resume_text, source_name=source_name)

    def parse_structured_profile(self, payload: dict[str, object]) -> ParsedCandidateInput:
        from app.modules.candidates.local_parser_provider import LocalResumeParserProvider
        return LocalResumeParserProvider().parse_structured_profile(payload)
