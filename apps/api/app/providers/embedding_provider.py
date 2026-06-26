from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    """Abstract boundary for sentence-transformer or hosted embedding models."""

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """Generate one embedding vector."""

    @abstractmethod
    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embedding vectors for a batch."""

    def embed_text(self, text: str) -> list[float]:
        """Backward-compatible alias for one embedding vector."""

        return self.embed(text)
