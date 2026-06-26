"""Repository interfaces for durable storage boundaries."""

from app.repositories.candidate_repository import CandidateRepository
from app.repositories.evaluation_repository import EvaluationRepository
from app.repositories.graph_repository import GraphRepository
from app.repositories.memory import (
    InMemoryCandidateRepository,
    InMemoryEvaluationRepository,
    InMemoryGraphRepository,
    InMemoryRankingRepository,
    InMemoryRoleDNARepository,
    InMemoryVectorRepository,
)
from app.repositories.ranking_repository import RankingRepository
from app.repositories.role_dna_repository import RoleDNARepository
from app.repositories.vector_repository import VectorRepository

__all__ = [
    "CandidateRepository",
    "EvaluationRepository",
    "GraphRepository",
    "InMemoryCandidateRepository",
    "InMemoryEvaluationRepository",
    "InMemoryGraphRepository",
    "InMemoryRankingRepository",
    "InMemoryRoleDNARepository",
    "InMemoryVectorRepository",
    "RankingRepository",
    "RoleDNARepository",
    "VectorRepository",
]
