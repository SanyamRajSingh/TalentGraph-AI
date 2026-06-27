"""Integration test for the startup seeder."""
import pytest

from app.domain.ranking import HiringPersona
from app.pipelines.evaluation_pipeline import EvaluationPipeline
from app.pipelines.ranking_pipeline import RankingPipeline
from app.pipelines.explanation_pipeline import ExplanationPipeline
from app.pipelines.embedding_pipeline import EmbeddingPipeline
from app.pipelines.graph_pipeline import GraphPipeline
from app.modules.evaluators import EvaluationService
from app.modules.explanations import CounterfactualService, ExplanationService
from app.modules.embeddings import EmbeddingFoundationService, LocalEmbeddingProvider, SummaryService
from app.modules.graph_builder import GraphBuilderService
from app.modules.ranking import RankingService
from app.repositories.memory import (
    InMemoryCandidateRepository,
    InMemoryEvaluationRepository,
    InMemoryExplanationRepository,
    InMemoryGraphRepository,
    InMemoryRankingRepository,
    InMemoryRoleDNARepository,
    InMemoryVectorRepository,
)
from app.startup.seeder import seed


def _make_pipelines(
    cand_repo, role_repo, eval_repo, rank_repo, exp_repo, vec_repo, graph_repo
):
    eval_pipeline = EvaluationPipeline(
        evaluation_service=EvaluationService(),
        evaluation_repository=eval_repo,
        role_repository=role_repo,
        candidate_repository=cand_repo,
    )
    ranking_pipeline = RankingPipeline(
        ranking_service=RankingService(
            evaluation_repository=eval_repo,
            ranking_repository=rank_repo,
        )
    )
    explanation_pipeline = ExplanationPipeline(
        explanation_service=ExplanationService(
            counterfactual_service=CounterfactualService(),
            explanation_repository=exp_repo,
        ),
        role_repository=role_repo,
        candidate_repository=cand_repo,
        evaluation_repository=eval_repo,
        ranking_repository=rank_repo,
    )
    embedding_pipeline = EmbeddingPipeline(
        embedding_service=EmbeddingFoundationService(
            summary_service=SummaryService(),
            embedding_provider=LocalEmbeddingProvider(),
        ),
        vector_repository=vec_repo,
        role_repository=role_repo,
        candidate_repository=cand_repo,
    )
    graph_pipeline = GraphPipeline(
        graph_builder_service=GraphBuilderService(),
        graph_repository=graph_repo,
        role_repository=role_repo,
        candidate_repository=cand_repo,
    )
    return eval_pipeline, ranking_pipeline, explanation_pipeline, embedding_pipeline, graph_pipeline


def test_seeder_populates_repositories():
    cand_repo  = InMemoryCandidateRepository()
    role_repo  = InMemoryRoleDNARepository()
    eval_repo  = InMemoryEvaluationRepository()
    rank_repo  = InMemoryRankingRepository()
    exp_repo   = InMemoryExplanationRepository()
    vec_repo   = InMemoryVectorRepository()
    graph_repo = InMemoryGraphRepository()

    eval_pipe, rank_pipe, exp_pipe, emb_pipe, graph_pipe = _make_pipelines(
        cand_repo, role_repo, eval_repo, rank_repo, exp_repo, vec_repo, graph_repo
    )

    seed(
        candidate_repository=cand_repo,
        role_repository=role_repo,
        evaluation_pipeline=eval_pipe,
        ranking_pipeline=rank_pipe,
        explanation_pipeline=exp_pipe,
        embedding_pipeline=emb_pipe,
        graph_pipeline=graph_pipe,
    )

    candidates = cand_repo.list_candidates()
    roles = role_repo.list_role_dna()

    assert len(candidates) == 50, f"Expected 50 candidates, got {len(candidates)}"
    assert len(roles) == 10, f"Expected 10 roles, got {len(roles)}"

    # Verify rankings were generated
    rankings = rank_repo.list_by_role_id("seed_role_00")
    assert len(rankings) > 0, "Expected rankings for seed_role_00"

    # Verify explanations were generated
    explanations = exp_repo.get_by_candidate_id("seed_backend_engineer_00")
    assert explanations is not None, "Expected explanation for seed_backend_engineer_00"


def test_seeder_is_idempotent():
    """Running seeder twice should not duplicate data."""
    cand_repo  = InMemoryCandidateRepository()
    role_repo  = InMemoryRoleDNARepository()
    eval_repo  = InMemoryEvaluationRepository()
    rank_repo  = InMemoryRankingRepository()
    exp_repo   = InMemoryExplanationRepository()
    vec_repo   = InMemoryVectorRepository()
    graph_repo = InMemoryGraphRepository()

    eval_pipe, rank_pipe, exp_pipe, emb_pipe, graph_pipe = _make_pipelines(
        cand_repo, role_repo, eval_repo, rank_repo, exp_repo, vec_repo, graph_repo
    )

    kwargs = dict(
        candidate_repository=cand_repo,
        role_repository=role_repo,
        evaluation_pipeline=eval_pipe,
        ranking_pipeline=rank_pipe,
        explanation_pipeline=exp_pipe,
        embedding_pipeline=emb_pipe,
        graph_pipeline=graph_pipe,
    )

    seed(**kwargs)
    seed(**kwargs)  # second run — must be a no-op

    candidates = cand_repo.list_candidates()
    assert len(candidates) == 50, f"Expected exactly 50 after 2 runs, got {len(candidates)}"
