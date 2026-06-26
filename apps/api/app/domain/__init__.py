"""Canonical domain entities for TalentGraph AI."""

from app.domain.candidate_twin import (
    CandidateDigitalTwin,
    CandidateResume,
    CandidateTimelineEntry,
    GrowthStage,
)
from app.domain.evaluation import EvaluatorResult, EvaluationBundle
from app.domain.explanation import CandidateExplanation, CounterfactualSuggestion
from app.domain.knowledge_graph import (
    GraphEntityType,
    GraphNode,
    GraphRelationship,
    GraphRelationshipType,
    KnowledgeGraph,
)
from app.domain.ranking import HiringPersona, RankingResult
from app.domain.role_dna import RoleDNAProfile, RoleJob, WorkEnvironmentAttributes
from app.domain.vector import EmbeddingCollection, EmbeddingRecord, SummaryDocument

__all__ = [
    "CandidateDigitalTwin",
    "CandidateResume",
    "CandidateTimelineEntry",
    "CandidateExplanation",
    "CounterfactualSuggestion",
    "EvaluationBundle",
    "EvaluatorResult",
    "GraphEntityType",
    "GraphNode",
    "GraphRelationship",
    "GraphRelationshipType",
    "HiringPersona",
    "GrowthStage",
    "KnowledgeGraph",
    "RankingResult",
    "RoleDNAProfile",
    "RoleJob",
    "EmbeddingCollection",
    "EmbeddingRecord",
    "SummaryDocument",
    "WorkEnvironmentAttributes",
]
