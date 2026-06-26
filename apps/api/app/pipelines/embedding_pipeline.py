from typing import Protocol

from app.domain.vector import EmbeddingCollection
from app.repositories.candidate_repository import CandidateRepository
from app.repositories.role_dna_repository import RoleDNARepository
from app.repositories.vector_repository import VectorRepository


class EmbeddingFoundationServiceProtocol(Protocol):
    def generate(
        self,
        role_dna: object | None = None,
        candidate_twin: object | None = None,
    ) -> EmbeddingCollection:
        """Generate summaries and embeddings."""


class EmbeddingPipeline:
    """Orchestrates summary generation, embedding generation, and persistence."""

    def __init__(
        self,
        embedding_service: EmbeddingFoundationServiceProtocol,
        vector_repository: VectorRepository,
        role_repository: RoleDNARepository,
        candidate_repository: CandidateRepository,
    ) -> None:
        self.embedding_service = embedding_service
        self.vector_repository = vector_repository
        self.role_repository = role_repository
        self.candidate_repository = candidate_repository

    def run(self, role_id: str | None = None, candidate_id: str | None = None) -> EmbeddingCollection:
        role_dna = self.role_repository.get_by_role_id(role_id) if role_id else None
        candidate_twin = self.candidate_repository.get_by_candidate_id(candidate_id) if candidate_id else None
        if role_id and role_dna is None:
            raise ValueError(f"Role DNA {role_id} not found.")
        if candidate_id and candidate_twin is None:
            raise ValueError(f"Candidate {candidate_id} not found.")

        collection = self.embedding_service.generate(role_dna=role_dna, candidate_twin=candidate_twin)
        return self.vector_repository.save(collection)
