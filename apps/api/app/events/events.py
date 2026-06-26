from datetime import UTC, datetime
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class DomainEvent(BaseModel):
    """Base event envelope for pipeline observability and future async hooks."""

    event_id: UUID = Field(default_factory=uuid4)
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    correlation_id: str | None = None


class JobUploaded(DomainEvent):
    event_type: Literal["job_uploaded"] = "job_uploaded"
    job_id: str


class RoleDNAGenerated(DomainEvent):
    event_type: Literal["role_dna_generated"] = "role_dna_generated"
    role_id: str


class CandidateUploaded(DomainEvent):
    event_type: Literal["candidate_uploaded"] = "candidate_uploaded"
    candidate_id: str


class DigitalTwinBuilt(DomainEvent):
    event_type: Literal["digital_twin_built"] = "digital_twin_built"
    candidate_id: str


class RankingGenerated(DomainEvent):
    event_type: Literal["ranking_generated"] = "ranking_generated"
    role_id: str
    persona: str


class ExplanationGenerated(DomainEvent):
    event_type: Literal["explanation_generated"] = "explanation_generated"
    candidate_id: str
    role_id: str
