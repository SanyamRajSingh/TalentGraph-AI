from pydantic import BaseModel

from app.domain.knowledge_graph import KnowledgeGraph
from app.domain.vector import EmbeddingCollection


class GraphResponse(BaseModel):
    graph_id: str
    graph: KnowledgeGraph


class EmbeddingCollectionResponse(BaseModel):
    collection_id: str
    collection: EmbeddingCollection
