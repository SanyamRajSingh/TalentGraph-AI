from app.domain.vector import EmbeddingCollection
from app.repositories.vector_repository import VectorRepository


class InMemoryVectorRepository(VectorRepository):
    """Process-local vector repository for tests and demo runs."""

    def __init__(self) -> None:
        self._collections: dict[str, EmbeddingCollection] = {}

    def save(self, collection: EmbeddingCollection) -> EmbeddingCollection:
        self._collections[collection.collection_id] = collection
        return collection

    def get(self, collection_id: str) -> EmbeddingCollection | None:
        return self._collections.get(collection_id)
