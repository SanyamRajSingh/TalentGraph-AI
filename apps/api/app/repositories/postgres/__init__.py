"""PostgreSQL repository skeletons."""

from app.repositories.postgres.postgres_candidate_repository import PostgresCandidateRepository
from app.repositories.postgres.postgres_evaluation_repository import PostgresEvaluationRepository
from app.repositories.postgres.postgres_ranking_repository import PostgresRankingRepository
from app.repositories.postgres.role_dna_repository import PostgresRoleDNARepository

__all__ = [
    "PostgresCandidateRepository",
    "PostgresEvaluationRepository",
    "PostgresRankingRepository",
    "PostgresRoleDNARepository",
]
