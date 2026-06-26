from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Consistent API error payload."""

    detail: str
    correlation_id: str | None = None


class WorkflowAcceptedResponse(BaseModel):
    """Response envelope for workflow-triggering endpoints."""

    workflow_id: str
    state: str
    correlation_id: str | None = None
