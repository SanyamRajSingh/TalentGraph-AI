from abc import ABC, abstractmethod

class CopilotConversationRepository(ABC):
    """Persistence contract for Copilot conversations."""

    @abstractmethod
    def save(self, conversation_id: str, payload: dict, role_id: str | None = None, candidate_id: str | None = None) -> dict:
        """Persist a conversation state."""

    @abstractmethod
    def get(self, conversation_id: str) -> dict | None:
        """Fetch a conversation state by id."""
