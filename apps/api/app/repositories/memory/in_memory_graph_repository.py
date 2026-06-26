from app.domain.knowledge_graph import KnowledgeGraph
from app.repositories.graph_repository import GraphRepository


class InMemoryGraphRepository(GraphRepository):
    """Process-local graph repository for tests and demo runs."""

    def __init__(self) -> None:
        self._graphs: dict[str, KnowledgeGraph] = {}

    def save(self, graph: KnowledgeGraph) -> KnowledgeGraph:
        self._graphs[graph.graph_id] = graph
        return graph

    def get(self, graph_id: str) -> KnowledgeGraph | None:
        return self._graphs.get(graph_id)
