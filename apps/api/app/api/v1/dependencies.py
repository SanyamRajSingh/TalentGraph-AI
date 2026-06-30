"""FastAPI dependency providers for all pipelines and repositories.

Repository selection strategy:
- If DATABASE_URL points to a PostgreSQL instance (settings.use_postgres == True),
  PostgreSQL-backed repositories are returned.
- Otherwise (default / tests), in-memory repositories are used.

This means: existing tests continue to pass without any DATABASE_URL set.
New production deployments set DATABASE_URL to enable persistence.
"""

from functools import lru_cache

from app.core.settings import get_settings
from app.modules.candidates import CandidateDigitalTwinService, LocalResumeParserProvider
from app.modules.embeddings import EmbeddingFoundationService, LocalEmbeddingProvider, SummaryService
from app.modules.evaluators import EvaluationService
from app.modules.explanations import CounterfactualService, ExplanationService
from app.modules.exports import RankingExportService
from app.modules.graph_builder import GraphBuilderService
from app.modules.ranking import RankingService
from app.modules.role_dna import LocalRoleDNALLMProvider, RoleDNAService
from app.pipelines.candidate_pipeline import CandidatePipeline
from app.pipelines.embedding_pipeline import EmbeddingPipeline
from app.pipelines.evaluation_pipeline import EvaluationPipeline
from app.pipelines.explanation_pipeline import ExplanationPipeline
from app.pipelines.graph_pipeline import GraphPipeline
from app.pipelines.ranking_pipeline import RankingPipeline
from app.pipelines.role_pipeline import RolePipeline
from app.repositories import (
    CandidateRepository,
    EvaluationRepository,
    ExplanationRepository,
    GraphRepository,
    InMemoryCandidateRepository,
    InMemoryEvaluationRepository,
    InMemoryExplanationRepository,
    InMemoryGraphRepository,
    InMemoryRankingRepository,
    InMemoryRoleDNARepository,
    InMemoryVectorRepository,
    PostgresCandidateRepository,
    PostgresEvaluationRepository,
    PostgresExplanationRepository,
    PostgresRankingRepository,
    PostgresRoleDNARepository,
    PostgresGraphRepository,
    RoleDNARepository,
    RankingRepository,
    VectorRepository,
    RecommendationRepository,
    CopilotConversationRepository,
    InMemoryRecommendationRepository,
    InMemoryCopilotRepository,
    PostgresRecommendationRepository,
    PostgresCopilotRepository,
)


# ---------------------------------------------------------------------------
# Shared singleton session (only created when use_postgres is True)
# ---------------------------------------------------------------------------

_pg_session = None


def _get_pg_session():
    """Return a long-lived SQLAlchemy Session for singleton Postgres repos.

    For a production app with request-scoped sessions, use get_db() instead.
    Here we use a single session per process for simplicity, matching the
    lru_cache pattern already used for in-memory repos.
    """
    global _pg_session  # noqa: PLW0603
    if _pg_session is None:
        from app.db.session import _get_session_local, create_tables
        create_tables()  # idempotent — creates tables if they don't exist
        _pg_session = _get_session_local()()
    return _pg_session


# ---------------------------------------------------------------------------
# Repository factories — switch between memory and postgres
# ---------------------------------------------------------------------------

@lru_cache
def get_role_dna_repository() -> RoleDNARepository:
    settings = get_settings()
    if settings.use_postgres:
        return PostgresRoleDNARepository(session=_get_pg_session())
    return InMemoryRoleDNARepository()


@lru_cache
def get_candidate_repository() -> CandidateRepository:
    settings = get_settings()
    if settings.use_postgres:
        return PostgresCandidateRepository(session=_get_pg_session())
    return InMemoryCandidateRepository()


@lru_cache
def get_evaluation_repository() -> EvaluationRepository:
    settings = get_settings()
    if settings.use_postgres:
        return PostgresEvaluationRepository(session=_get_pg_session())
    return InMemoryEvaluationRepository()


@lru_cache
def get_ranking_repository() -> RankingRepository:
    settings = get_settings()
    if settings.use_postgres:
        return PostgresRankingRepository(session=_get_pg_session())
    return InMemoryRankingRepository()


@lru_cache
def get_explanation_repository() -> ExplanationRepository:
    settings = get_settings()
    if settings.use_postgres:
        return PostgresExplanationRepository(session=_get_pg_session())
    return InMemoryExplanationRepository()


@lru_cache
def get_graph_repository() -> GraphRepository:
    settings = get_settings()
    if settings.use_postgres:
        return PostgresGraphRepository(session_factory=_get_pg_session)
    return InMemoryGraphRepository()


@lru_cache
def get_vector_repository() -> VectorRepository:
    # Vector repository remains in-memory (Chroma integration is a separate phase)
    return InMemoryVectorRepository()


@lru_cache
def get_recommendation_repository() -> RecommendationRepository:
    settings = get_settings()
    if settings.use_postgres:
        return PostgresRecommendationRepository(session_factory=_get_pg_session)
    return InMemoryRecommendationRepository()


@lru_cache
def get_copilot_repository() -> CopilotConversationRepository:
    settings = get_settings()
    if settings.use_postgres:
        return PostgresCopilotRepository(session_factory=_get_pg_session)
    return InMemoryCopilotRepository()


# ---------------------------------------------------------------------------
# Service factories (unchanged from v1.0)
# ---------------------------------------------------------------------------

@lru_cache
def get_role_dna_service() -> RoleDNAService:
    return RoleDNAService(llm_provider=LocalRoleDNALLMProvider())


def get_role_pipeline() -> RolePipeline:
    return RolePipeline(
        role_dna_service=get_role_dna_service(),
        role_repository=get_role_dna_repository(),
    )


@lru_cache
def get_candidate_twin_service() -> CandidateDigitalTwinService:
    return CandidateDigitalTwinService(parser_provider=LocalResumeParserProvider())


def get_candidate_pipeline() -> CandidatePipeline:
    return CandidatePipeline(
        twin_service=get_candidate_twin_service(),
        candidate_repository=get_candidate_repository(),
    )


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
def get_embedding_foundation_service() -> EmbeddingFoundationService:
    settings = get_settings()
    try:
        import sentence_transformers
        from app.providers.sentence_transformer_provider import SentenceTransformerEmbeddingProvider
        provider = SentenceTransformerEmbeddingProvider(model_name=settings.sentence_transformers_model)
    except ImportError:
        provider = LocalEmbeddingProvider()

    return EmbeddingFoundationService(
        summary_service=SummaryService(),
        embedding_provider=provider,
    )


def get_embedding_pipeline() -> EmbeddingPipeline:
    return EmbeddingPipeline(
        embedding_service=get_embedding_foundation_service(),
        vector_repository=get_vector_repository(),
        role_repository=get_role_dna_repository(),
        candidate_repository=get_candidate_repository(),
    )


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


def get_ranking_service() -> RankingService:
    return RankingService(
        evaluation_repository=get_evaluation_repository(),
        ranking_repository=get_ranking_repository(),
        candidate_repository=get_candidate_repository(),
    )


def get_ranking_pipeline() -> RankingPipeline:
    return RankingPipeline(ranking_service=get_ranking_service())


@lru_cache
def get_counterfactual_service() -> CounterfactualService:
    return CounterfactualService()


def get_explanation_service() -> ExplanationService:
    return ExplanationService(
        counterfactual_service=get_counterfactual_service(),
        explanation_repository=get_explanation_repository(),
    )


def get_explanation_pipeline() -> ExplanationPipeline:
    return ExplanationPipeline(
        explanation_service=get_explanation_service(),
        role_repository=get_role_dna_repository(),
        candidate_repository=get_candidate_repository(),
        evaluation_repository=get_evaluation_repository(),
        ranking_repository=get_ranking_repository(),
    )


def get_ranking_export_service() -> RankingExportService:
    return RankingExportService(
        ranking_repository=get_ranking_repository(),
        candidate_repository=get_candidate_repository(),
        explanation_repository=get_explanation_repository(),
        evaluation_repository=get_evaluation_repository(),
    )


@lru_cache
def get_search_service():
    from app.modules.search.search_service import SearchService
    return SearchService(
        candidate_repository=get_candidate_repository(),
        role_repository=get_role_dna_repository(),
        embedding_provider=get_embedding_foundation_service().embedding_provider,
    )


@lru_cache
def get_recommendation_service():
    from app.modules.recommendation.service import RecommendationService
    return RecommendationService()

@lru_cache
def get_copilot_service():
    from app.modules.copilot.service import CopilotService
    return CopilotService()

def get_copilot_pipeline():
    from app.pipelines.copilot_pipeline import CopilotPipeline
    return CopilotPipeline(
        copilot_service=get_copilot_service(),
        candidate_repository=get_candidate_repository(),
        role_repository=get_role_dna_repository(),
        evaluation_repository=get_evaluation_repository(),
    )


@lru_cache
def get_batch_pipeline():
    from app.pipelines.batch_pipeline import BatchPipeline
    return BatchPipeline(candidate_pipeline=get_candidate_pipeline())


def get_copilot_chat_service():
    from app.modules.copilot.chat_service import CopilotChatService
    return CopilotChatService(
        candidate_repository=get_candidate_repository(),
        role_repository=get_role_dna_repository(),
    )


def get_comparison_service():
    from app.modules.comparison.service import ComparisonService
    return ComparisonService()


def get_analytics_service():
    from app.modules.analytics.service import AnalyticsService
    return AnalyticsService(
        candidate_repository=get_candidate_repository(),
        role_repository=get_role_dna_repository(),
        evaluation_repository=get_evaluation_repository(),
    )
