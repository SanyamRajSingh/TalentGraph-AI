"""Candidate Digital Twin Builder module."""

from app.modules.candidates.local_parser_provider import LocalResumeParserProvider
from app.modules.candidates.service import CandidateDigitalTwinService

__all__ = ["CandidateDigitalTwinService", "LocalResumeParserProvider"]
