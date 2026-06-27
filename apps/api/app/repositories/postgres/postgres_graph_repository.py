from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.models import GraphRow
from app.domain.knowledge_graph import KnowledgeGraph
from app.repositories.graph_repository import GraphRepository


class PostgresGraphRepository(GraphRepository):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def save(self, graph: KnowledgeGraph) -> KnowledgeGraph:
        with self.session_factory() as session:
            row = session.execute(
                select(GraphRow).where(GraphRow.graph_id == graph.graph_id)
            ).scalar_one_or_none()
            if row is None:
                row = GraphRow(
                    graph_id=graph.graph_id,
                    role_id=graph.role_id,
                    candidate_id=graph.candidate_id,
                    node_count=len(graph.nodes),
                    payload=graph.model_dump(mode="json"),
                )
                session.add(row)
            else:
                row.node_count = len(graph.nodes)
                row.payload = graph.model_dump(mode="json")
            session.commit()
            return graph

    def get(self, graph_id: str) -> KnowledgeGraph | None:
        with self.session_factory() as session:
            row = session.execute(
                select(GraphRow).where(GraphRow.graph_id == graph_id)
            ).scalar_one_or_none()
            if row is None:
                return None
            return KnowledgeGraph.model_validate(row.payload)
