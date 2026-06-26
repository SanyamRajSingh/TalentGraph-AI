from abc import ABC, abstractmethod

from app.domain.vector import EmbeddingCollection


class VectorRepository(ABC):
    """Persistence contract for summary embeddings."""

    @abstractmethod
    def save(self, collection: EmbeddingCollection) -> EmbeddingCollection:
        """Persist an embedding collection."""

    @abstractmethod
    def get(self, collection_id: str) -> EmbeddingCollection | None:
        """Fetch an embedding collection by id."""
