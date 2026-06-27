from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.models import CopilotConversationRow
from app.repositories.copilot_repository import CopilotConversationRepository


class PostgresCopilotRepository(CopilotConversationRepository):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def save(self, conversation_id: str, payload: dict, role_id: str | None = None, candidate_id: str | None = None) -> dict:
        with self.session_factory() as session:
            row = session.execute(
                select(CopilotConversationRow).where(CopilotConversationRow.conversation_id == conversation_id)
            ).scalar_one_or_none()
            if row is None:
                row = CopilotConversationRow(
                    conversation_id=conversation_id,
                    role_id=role_id,
                    candidate_id=candidate_id,
                    payload=payload,
                )
                session.add(row)
            else:
                row.payload = payload
            session.commit()
            return payload

    def get(self, conversation_id: str) -> dict | None:
        with self.session_factory() as session:
            row = session.execute(
                select(CopilotConversationRow).where(CopilotConversationRow.conversation_id == conversation_id)
            ).scalar_one_or_none()
            if row is None:
                return None
            return row.payload
