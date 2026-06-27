"""Request DTOs for API endpoints."""

from app.contracts.requests.candidate_requests import BuildDigitalTwinRequest, UploadCandidateRequest
from app.contracts.requests.evaluation_requests import EvaluateRequest
from app.contracts.requests.explanation_requests import GenerateExplanationRequest
from app.contracts.requests.export_requests import ExportRankingsRequest
from app.contracts.requests.foundation_requests import BuildGraphRequest, GenerateEmbeddingsRequest
from app.contracts.requests.rank_requests import RankRequest
from app.contracts.requests.role_dna_requests import GenerateRoleDNARequest, UploadJobRequest

__all__ = [
    "BuildDigitalTwinRequest",
    "BuildGraphRequest",
    "EvaluateRequest",
    "ExportRankingsRequest",
    "GenerateExplanationRequest",
    "GenerateEmbeddingsRequest",
    "GenerateRoleDNARequest",
    "RankRequest",
    "UploadCandidateRequest",
    "UploadJobRequest",
]
