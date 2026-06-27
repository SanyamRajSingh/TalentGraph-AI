"""Repository interfaces for durable storage boundaries."""

from app.repositories.candidate_repository import CandidateRepository
from app.repositories.evaluation_repository import EvaluationRepository
from app.repositories.explanation_repository import ExplanationRepository
from app.repositories.graph_repository import GraphRepository
from app.repositories.memory import (
    InMemoryCandidateRepository,
    InMemoryEvaluationRepository,
    InMemoryExplanationRepository,
    InMemoryGraphRepository,
    InMemoryRankingRepository,
    InMemoryRoleDNARepository,
    InMemoryVectorRepository,
)
from app.repositories.postgres import (
    PostgresCandidateRepository,
    PostgresEvaluationRepository,
    PostgresExplanationRepository,
    PostgresRankingRepository,
    PostgresRoleDNARepository,
)
from app.repositories.ranking_repository import RankingRepository
from app.repositories.role_dna_repository import RoleDNARepository
from app.repositories.vector_repository import VectorRepository

__all__ = [
    # Interfaces
    "CandidateRepository",
    "EvaluationRepository",
    "ExplanationRepository",
    "GraphRepository",
    "RankingRepository",
    "RoleDNARepository",
    "VectorRepository",
    # In-memory implementations (default / tests)
    "InMemoryCandidateRepository",
    "InMemoryEvaluationRepository",
    "InMemoryExplanationRepository",
    "InMemoryGraphRepository",
    "InMemoryRankingRepository",
    "InMemoryRoleDNARepository",
    "InMemoryVectorRepository",
    # PostgreSQL implementations (production)
    "PostgresCandidateRepository",
    "PostgresEvaluationRepository",
    "PostgresExplanationRepository",
    "PostgresRankingRepository",
    "PostgresRoleDNARepository",
]
