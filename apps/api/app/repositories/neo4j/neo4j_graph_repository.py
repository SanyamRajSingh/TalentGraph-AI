from app.domain.knowledge_graph import KnowledgeGraph
from app.repositories.graph_repository import GraphRepository


class Neo4jGraphRepository(GraphRepository):
    """Neo4j graph repository skeleton for future persistence hardening."""

    def __init__(self, driver: object) -> None:
        self.driver = driver

    def save(self, graph: KnowledgeGraph) -> KnowledgeGraph:
        raise NotImplementedError("Neo4j graph persistence is not implemented in Module 3.")

    def get(self, graph_id: str) -> KnowledgeGraph | None:
        raise NotImplementedError("Neo4j graph lookup is not implemented in Module 3.")
