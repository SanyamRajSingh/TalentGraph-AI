from typing import Protocol

from app.domain.knowledge_graph import KnowledgeGraph
from app.repositories.candidate_repository import CandidateRepository
from app.repositories.graph_repository import GraphRepository
from app.repositories.role_dna_repository import RoleDNARepository


class GraphBuilderServiceProtocol(Protocol):
    def build(self, role_dna: object | None = None, candidate_twin: object | None = None) -> KnowledgeGraph:
        """Build a deterministic graph snapshot."""


class GraphPipeline:
    """Orchestrates graph construction and persistence."""

    def __init__(
        self,
        graph_builder_service: GraphBuilderServiceProtocol,
        graph_repository: GraphRepository,
        role_repository: RoleDNARepository,
        candidate_repository: CandidateRepository,
    ) -> None:
        self.graph_builder_service = graph_builder_service
        self.graph_repository = graph_repository
        self.role_repository = role_repository
        self.candidate_repository = candidate_repository

    def run(self, role_id: str | None = None, candidate_id: str | None = None) -> KnowledgeGraph:
        role_dna = self.role_repository.get_by_role_id(role_id) if role_id else None
        candidate_twin = self.candidate_repository.get_by_candidate_id(candidate_id) if candidate_id else None
        if role_id and role_dna is None:
            raise ValueError(f"Role DNA {role_id} not found.")
        if candidate_id and candidate_twin is None:
            raise ValueError(f"Candidate {candidate_id} not found.")

        graph = self.graph_builder_service.build(role_dna=role_dna, candidate_twin=candidate_twin)
        return self.graph_repository.save(graph)
