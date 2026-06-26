from app.domain.knowledge_graph import KnowledgeGraph
from app.domain.vector import EmbeddingCollection
from app.repositories.memory import InMemoryGraphRepository, InMemoryVectorRepository


def test_memory_graph_repository_persists_graphs() -> None:
    repository = InMemoryGraphRepository()
    graph = KnowledgeGraph(graph_id="graph_test")

    repository.save(graph)

    assert repository.get("graph_test") == graph


def test_memory_vector_repository_persists_collections() -> None:
    repository = InMemoryVectorRepository()
    collection = EmbeddingCollection(collection_id="embeddings_test")

    repository.save(collection)

    assert repository.get("embeddings_test") == collection
