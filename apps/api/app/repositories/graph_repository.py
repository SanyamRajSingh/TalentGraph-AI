from abc import ABC, abstractmethod

from app.domain.knowledge_graph import KnowledgeGraph


class GraphRepository(ABC):
    """Persistence contract for Talent Knowledge Graph snapshots."""

    @abstractmethod
    def save(self, graph: KnowledgeGraph) -> KnowledgeGraph:
        """Persist a graph snapshot."""

    @abstractmethod
    def get(self, graph_id: str) -> KnowledgeGraph | None:
        """Fetch a graph snapshot by id."""
