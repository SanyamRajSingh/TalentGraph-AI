from functools import lru_cache

from app.modules.candidates import CandidateDigitalTwinService, LocalResumeParserProvider
from app.modules.embeddings import EmbeddingFoundationService, LocalEmbeddingProvider, SummaryService
from app.modules.evaluators import EvaluationService
from app.modules.graph_builder import GraphBuilderService
from app.modules.ranking import RankingService
from app.modules.role_dna import LocalRoleDNALLMProvider, RoleDNAService
from app.pipelines.candidate_pipeline import CandidatePipeline
from app.pipelines.embedding_pipeline import EmbeddingPipeline
from app.pipelines.evaluation_pipeline import EvaluationPipeline
from app.pipelines.graph_pipeline import GraphPipeline
from app.pipelines.ranking_pipeline import RankingPipeline
from app.pipelines.role_pipeline import RolePipeline
from app.repositories import (
    CandidateRepository,
    EvaluationRepository,
    GraphRepository,
    InMemoryCandidateRepository,
    InMemoryEvaluationRepository,
    InMemoryGraphRepository,
    InMemoryRankingRepository,
    InMemoryRoleDNARepository,
    InMemoryVectorRepository,
    RoleDNARepository,
    RankingRepository,
    VectorRepository,
)


@lru_cache
def get_role_dna_repository() -> RoleDNARepository:
    return InMemoryRoleDNARepository()


@lru_cache
def get_role_dna_service() -> RoleDNAService:
    return RoleDNAService(llm_provider=LocalRoleDNALLMProvider())


def get_role_pipeline() -> RolePipeline:
    return RolePipeline(
        role_dna_service=get_role_dna_service(),
        role_repository=get_role_dna_repository(),
    )


@lru_cache
def get_candidate_repository() -> CandidateRepository:
    return InMemoryCandidateRepository()


@lru_cache
def get_candidate_twin_service() -> CandidateDigitalTwinService:
    return CandidateDigitalTwinService(parser_provider=LocalResumeParserProvider())


def get_candidate_pipeline() -> CandidatePipeline:
    return CandidatePipeline(
        twin_service=get_candidate_twin_service(),
        candidate_repository=get_candidate_repository(),
    )


@lru_cache
def get_graph_repository() -> GraphRepository:
    return InMemoryGraphRepository()


@lru_cache
def get_graph_builder_service() -> GraphBuilderService:
    return GraphBuilderService()


def get_graph_pipeline() -> GraphPipeline:
    return GraphPipeline(
        graph_builder_service=get_graph_builder_service(),
        graph_repository=get_graph_repository(),
        role_repository=get_role_dna_repository(),
        candidate_repository=get_candidate_repository(),
    )


@lru_cache
def get_vector_repository() -> VectorRepository:
    return InMemoryVectorRepository()


@lru_cache
def get_embedding_foundation_service() -> EmbeddingFoundationService:
    return EmbeddingFoundationService(
        summary_service=SummaryService(),
        embedding_provider=LocalEmbeddingProvider(),
    )


def get_embedding_pipeline() -> EmbeddingPipeline:
    return EmbeddingPipeline(
        embedding_service=get_embedding_foundation_service(),
        vector_repository=get_vector_repository(),
        role_repository=get_role_dna_repository(),
        candidate_repository=get_candidate_repository(),
    )


@lru_cache
def get_evaluation_repository() -> EvaluationRepository:
    return InMemoryEvaluationRepository()


@lru_cache
def get_evaluation_service() -> EvaluationService:
    return EvaluationService()


def get_evaluation_pipeline() -> EvaluationPipeline:
    return EvaluationPipeline(
        evaluation_service=get_evaluation_service(),
        evaluation_repository=get_evaluation_repository(),
        role_repository=get_role_dna_repository(),
        candidate_repository=get_candidate_repository(),
    )


@lru_cache
def get_ranking_repository() -> RankingRepository:
    return InMemoryRankingRepository()


def get_ranking_service() -> RankingService:
    return RankingService(
        evaluation_repository=get_evaluation_repository(),
        ranking_repository=get_ranking_repository(),
    )


def get_ranking_pipeline() -> RankingPipeline:
    return RankingPipeline(ranking_service=get_ranking_service())
