"""Response DTOs for API endpoints."""

from app.contracts.responses.candidate_responses import (
    CandidateListResponse,
    CandidateTwinResponse,
    UploadCandidateResponse,
)
from app.contracts.responses.common import ErrorResponse, WorkflowAcceptedResponse
from app.contracts.responses.evaluation_responses import EvaluationResponse
from app.contracts.responses.explanation_responses import ExplanationResponse
from app.contracts.responses.foundation_responses import EmbeddingCollectionResponse, GraphResponse
from app.contracts.responses.rank_responses import RankingResponse
from app.contracts.responses.role_dna_responses import (
    RoleDNAListResponse,
    RoleDNAResponse,
    UploadJobResponse,
)

__all__ = [
    "ErrorResponse",
    "EmbeddingCollectionResponse",
    "EvaluationResponse",
    "ExplanationResponse",
    "CandidateListResponse",
    "CandidateTwinResponse",
    "GraphResponse",
    "RankingResponse",
    "RoleDNAListResponse",
    "RoleDNAResponse",
    "UploadJobResponse",
    "UploadCandidateResponse",
    "WorkflowAcceptedResponse",
]
