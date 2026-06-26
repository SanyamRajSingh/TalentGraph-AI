"""Embedding foundation module."""

from app.modules.embeddings.local_provider import LocalEmbeddingProvider
from app.modules.embeddings.service import EmbeddingFoundationService
from app.modules.embeddings.summary_service import SummaryService

__all__ = ["EmbeddingFoundationService", "LocalEmbeddingProvider", "SummaryService"]
