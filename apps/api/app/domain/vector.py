from pydantic import BaseModel, Field


class SummaryDocument(BaseModel):
    id: str
    kind: str
    owner_id: str
    text: str
    metadata: dict[str, str | int | float | bool | None] = Field(default_factory=dict)


class EmbeddingRecord(BaseModel):
    id: str
    source_id: str
    kind: str
    text: str
    vector: list[float]
    metadata: dict[str, str | int | float | bool | None] = Field(default_factory=dict)


class EmbeddingCollection(BaseModel):
    collection_id: str
    summaries: list[SummaryDocument] = Field(default_factory=list)
    embeddings: list[EmbeddingRecord] = Field(default_factory=list)
