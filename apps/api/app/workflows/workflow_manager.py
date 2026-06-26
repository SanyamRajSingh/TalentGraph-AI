from abc import ABC, abstractmethod

from app.workflows.processing_state import ProcessingStage, ProcessingState, WorkflowStatus


class WorkflowManager(ABC):
    """Abstract boundary for tracking workflow progress."""

    @abstractmethod
    def start(self, stage: ProcessingStage, correlation_id: str | None = None) -> ProcessingState:
        """Create a workflow state record."""

    @abstractmethod
    def transition(
        self,
        state: ProcessingState,
        status: WorkflowStatus,
        message: str | None = None,
    ) -> ProcessingState:
        """Transition workflow state."""
