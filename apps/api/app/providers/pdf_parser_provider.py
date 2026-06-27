"""PDF resume parser provider.

Uses pypdf to extract text from PDF bytes.
Gracefully degrades to an empty-text stub if pypdf is not installed.
"""

from app.providers.parser_provider import ParsedCandidateInput, ParserProvider


class PdfParserProvider(ParserProvider):
    """Extract plain text from PDF resume bytes using pypdf."""

    def parse_resume(self, content: bytes, filename: str) -> ParsedCandidateInput:
        try:
            import io
            from pypdf import PdfReader

            reader = PdfReader(io.BytesIO(content))
            pages = [page.extract_text() or "" for page in reader.pages]
            raw_text = "\n".join(pages).strip()
        except ImportError:
            raw_text = f"[PDF parsing unavailable — pypdf not installed] filename={filename}"
        except Exception as exc:
            raw_text = f"[PDF parse error: {exc}] filename={filename}"

        source_name = filename
        return self.parse_resume_text(raw_text, source_name=source_name)

    def parse_resume_text(self, resume_text: str, source_name: str | None = None) -> ParsedCandidateInput:
        """Delegate text parsing to the local parser for field extraction."""
        from app.modules.candidates.local_parser_provider import LocalResumeParserProvider
        return LocalResumeParserProvider().parse_resume_text(resume_text, source_name=source_name)

    def parse_structured_profile(self, payload: dict[str, object]) -> ParsedCandidateInput:
        from app.modules.candidates.local_parser_provider import LocalResumeParserProvider
        return LocalResumeParserProvider().parse_structured_profile(payload)
