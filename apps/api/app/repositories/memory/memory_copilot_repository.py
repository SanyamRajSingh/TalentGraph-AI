from app.repositories.copilot_repository import CopilotConversationRepository

class InMemoryCopilotRepository(CopilotConversationRepository):
    def __init__(self):
        self._db: dict[str, dict] = {}

    def save(self, conversation_id: str, payload: dict, role_id: str | None = None, candidate_id: str | None = None) -> dict:
        self._db[conversation_id] = payload
        return payload

    def get(self, conversation_id: str) -> dict | None:
        return self._db.get(conversation_id)
