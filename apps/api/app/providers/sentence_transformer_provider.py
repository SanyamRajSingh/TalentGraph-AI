from fastapi import HTTPException
from app.providers.embedding_provider import EmbeddingProvider

class SentenceTransformerEmbeddingProvider(EmbeddingProvider):
    """Real embedding provider using sentence-transformers."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        self.model_name = model_name
        self._model = None

    @property
    def model(self):
        if self._model is None:
            # Lazy load so it doesn't block startup or memory unless requested
            try:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer(self.model_name)
            except ModuleNotFoundError:
                raise HTTPException(
                    status_code=501, 
                    detail="ML dependencies (sentence-transformers) are not installed in this environment."
                )
        return self._model

    def embed(self, text: str) -> list[float]:
        # Encode returns a numpy array, we convert to float list
        return self.model.encode(text).tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts).tolist()
