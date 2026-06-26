from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class WorkflowStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class ProcessingStage(StrEnum):
    JOB_UPLOAD = "job_upload"
    ROLE_DNA = "role_dna"
    CANDIDATE_UPLOAD = "candidate_upload"
    DIGITAL_TWIN = "digital_twin"
    RANKING = "ranking"
    EXPLANATION = "explanation"


class ProcessingState(BaseModel):
    """Workflow progress state for long-running or multi-step operations."""

    workflow_id: UUID = Field(default_factory=uuid4)
    status: WorkflowStatus = WorkflowStatus.PENDING
    stage: ProcessingStage
    correlation_id: str | None = None
    message: str | None = None
