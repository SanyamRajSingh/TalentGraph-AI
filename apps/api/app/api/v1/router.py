from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.api.v1.dependencies import (
    get_candidate_pipeline,
    get_candidate_repository,
    get_embedding_pipeline,
    get_evaluation_pipeline,
    get_evaluation_repository,
    get_explanation_pipeline,
    get_explanation_repository,
    get_graph_pipeline,
    get_graph_repository,
    get_ranking_export_service,
    get_ranking_pipeline,
    get_ranking_repository,
    get_role_dna_repository,
    get_role_pipeline,
    get_vector_repository,
    get_search_service,
    get_recommendation_service,
    get_copilot_pipeline,
    get_copilot_chat_service,
    get_comparison_service,
    get_analytics_service,
)
from app.contracts.requests import (
    BuildDigitalTwinRequest,
    BuildGraphRequest,
    EvaluateRequest,
    ExportRankingsRequest,
    GenerateExplanationRequest,
    GenerateEmbeddingsRequest,
    GenerateRoleDNARequest,
    RankRequest,
    UploadCandidateRequest,
    UploadJobRequest,
)
from app.contracts.requests.recommend_requests import RecommendRequest
from app.contracts.responses.candidate_responses import (
    CandidateListResponse,
    CandidateTwinResponse,
    UploadCandidateResponse,
)
from app.contracts.responses.evaluation_responses import EvaluationResponse
from app.contracts.responses.explanation_responses import ExplanationResponse
from app.contracts.responses.foundation_responses import EmbeddingCollectionResponse, GraphResponse
from app.contracts.responses.rank_responses import RankingResponse
from app.contracts.responses.role_dna_responses import (
    RoleDNAListResponse,
    RoleDNAResponse,
    UploadJobResponse,
)
from app.pipelines.candidate_pipeline import CandidatePipeline
from app.pipelines.embedding_pipeline import EmbeddingPipeline
from app.pipelines.evaluation_pipeline import EvaluationPipeline
from app.pipelines.explanation_pipeline import ExplanationPipeline
from app.pipelines.graph_pipeline import GraphPipeline
from app.pipelines.ranking_pipeline import RankingPipeline
from app.modules.exports import RankingExportService
from app.pipelines.role_pipeline import RolePipeline
from app.repositories import (
    CandidateRepository,
    EvaluationRepository,
    ExplanationRepository,
    GraphRepository,
    RankingRepository,
    RoleDNARepository,
    VectorRepository,
)

api_router = APIRouter()


def not_implemented(module_name: str) -> None:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=f"{module_name} is planned but not implemented in the scaffolding increment.",
    )


@api_router.post("/upload-job", response_model=UploadJobResponse, tags=["jobs", "role-dna"])
def upload_job(
    request: UploadJobRequest,
    pipeline: RolePipeline = Depends(get_role_pipeline),
) -> UploadJobResponse:
    job, _event = pipeline.upload_job(
        job_description=request.job_description,
        source_name=request.source_name,
    )
    return UploadJobResponse(job_id=job.job_id, job=job)


@api_router.post("/upload-candidates", response_model=UploadCandidateResponse, tags=["candidates"])
def upload_candidates(
    request: UploadCandidateRequest,
    pipeline: CandidatePipeline = Depends(get_candidate_pipeline),
) -> UploadCandidateResponse:
    resume, _event = pipeline.upload_resume(
        resume_text=request.resume_text,
        source_name=request.source_name,
    )
    return UploadCandidateResponse(resume_id=resume.resume_id, resume=resume)


from fastapi import File, UploadFile

@api_router.post("/upload-file", response_model=CandidateTwinResponse, tags=["candidates"])
async def upload_file(
    file: UploadFile = File(...),
    pipeline: CandidatePipeline = Depends(get_candidate_pipeline),
) -> CandidateTwinResponse:
    """Upload a PDF, DOCX, or TXT resume file to build a Digital Twin."""
    file_bytes = await file.read()
    twin, _event = pipeline.upload_from_file(
        file_bytes=file_bytes,
        filename=file.filename or "unknown",
        content_type=file.content_type or "application/octet-stream",
    )
    return CandidateTwinResponse(candidate_id=twin.candidate_id, twin=twin)


from app.pipelines.batch_pipeline import BatchPipeline
from app.api.v1.dependencies import get_batch_pipeline

@api_router.post("/batch/upload-zip", tags=["batch"])
async def batch_upload_zip(
    file: UploadFile = File(...),
    pipeline: BatchPipeline = Depends(get_batch_pipeline),
):
    """Upload a ZIP file of resumes to be parsed and converted to Digital Twins asynchronously."""
    if not file.filename or not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Must be a .zip file")
    file_bytes = await file.read()
    job_id = await pipeline.upload_zip_async(file_bytes=file_bytes)
    return {"job_id": job_id, "message": "Batch processing started"}

@api_router.get("/batch/status/{job_id}", tags=["batch"])
def get_batch_status(
    job_id: str,
    pipeline: BatchPipeline = Depends(get_batch_pipeline),
):
    status = pipeline.get_job_status(job_id)
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    return status



@api_router.post("/generate-role-dna", response_model=RoleDNAResponse, tags=["role-dna"])
def generate_role_dna(
    request: GenerateRoleDNARequest,
    pipeline: RolePipeline = Depends(get_role_pipeline),
) -> RoleDNAResponse:
    if not request.job_id and not request.job_description:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Either job_id or job_description is required.",
        )

    try:
        role_dna, _event = pipeline.run(
            job_description=request.job_description or "",
            job_id=request.job_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return RoleDNAResponse(role_id=role_dna.role_id, job_id=role_dna.job_id, role_dna=role_dna)


@api_router.get("/role-dna", response_model=RoleDNAListResponse, tags=["role-dna"])
def list_role_dna(
    repository: RoleDNARepository = Depends(get_role_dna_repository),
) -> RoleDNAListResponse:
    return RoleDNAListResponse(items=repository.list_role_dna())


@api_router.get("/role-dna/{role_id}", response_model=RoleDNAResponse, tags=["role-dna"])
def get_role_dna(
    role_id: str,
    repository: RoleDNARepository = Depends(get_role_dna_repository),
) -> RoleDNAResponse:
    role_dna = repository.get_by_role_id(role_id)
    if role_dna is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role DNA {role_id} not found.")
    return RoleDNAResponse(role_id=role_dna.role_id, job_id=role_dna.job_id, role_dna=role_dna)


@api_router.post("/build-digital-twins", response_model=CandidateTwinResponse, tags=["candidates"])
def build_digital_twin(
    request: BuildDigitalTwinRequest,
    pipeline: CandidatePipeline = Depends(get_candidate_pipeline),
) -> CandidateTwinResponse:
    if not request.resume_id and not request.resume_text:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Either resume_id or resume_text is required.",
        )

    try:
        twin, _event = pipeline.run(
            resume_text=request.resume_text,
            resume_id=request.resume_id,
            source_name=request.source_name,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return CandidateTwinResponse(candidate_id=twin.candidate_id, twin=twin)


@api_router.post("/rank-candidates", tags=["ranking"])
def rank_candidates() -> None:
    not_implemented("Ranking pipeline")


@api_router.post("/rank", response_model=RankingResponse, tags=["ranking"])
def rank(
    request: RankRequest,
    pipeline: RankingPipeline = Depends(get_ranking_pipeline),
) -> RankingResponse:
    rankings = pipeline.run(role_id=request.role_id, persona=request.persona)
    return RankingResponse(role_id=request.role_id, persona=request.persona.value, rankings=rankings)


@api_router.post("/build-graph", response_model=GraphResponse, tags=["graph"])
def build_graph(
    request: BuildGraphRequest,
    pipeline: GraphPipeline = Depends(get_graph_pipeline),
) -> GraphResponse:
    if not request.role_id and not request.candidate_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Either role_id or candidate_id is required.",
        )
    try:
        graph = pipeline.run(role_id=request.role_id, candidate_id=request.candidate_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return GraphResponse(graph_id=graph.graph_id, graph=graph)


@api_router.post("/generate-embeddings", response_model=EmbeddingCollectionResponse, tags=["embeddings"])
def generate_embeddings(
    request: GenerateEmbeddingsRequest,
    pipeline: EmbeddingPipeline = Depends(get_embedding_pipeline),
) -> EmbeddingCollectionResponse:
    if not request.role_id and not request.candidate_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Either role_id or candidate_id is required.",
        )
    try:
        collection = pipeline.run(role_id=request.role_id, candidate_id=request.candidate_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return EmbeddingCollectionResponse(collection_id=collection.collection_id, collection=collection)


@api_router.post("/evaluate", response_model=EvaluationResponse, tags=["evaluation"])
def evaluate_candidate(
    request: EvaluateRequest,
    pipeline: EvaluationPipeline = Depends(get_evaluation_pipeline),
) -> EvaluationResponse:
    try:
        evaluation = pipeline.run(role_id=request.role_id, candidate_id=request.candidate_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return EvaluationResponse(evaluation_id=evaluation.evaluation_id, evaluation=evaluation)


from app.contracts.responses.recommend_responses import RecommendResponse
from app.modules.recommendation.service import RecommendationService

@api_router.post("/recommend", response_model=RecommendResponse, tags=["recommendation"])
def recommend_candidate(
    request: RecommendRequest,
    pipeline: EvaluationPipeline = Depends(get_evaluation_pipeline),
    recommendation_service: RecommendationService = Depends(get_recommendation_service),
) -> RecommendResponse:
    try:
        evaluation = pipeline.run(role_id=request.role_id, candidate_id=request.candidate_id)
        recommendation = recommendation_service.recommend(evaluation)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return RecommendResponse(recommendation=recommendation)


@api_router.post("/generate-explanations", response_model=ExplanationResponse, tags=["explanations"])
def generate_explanations(
    request: GenerateExplanationRequest,
    pipeline: ExplanationPipeline = Depends(get_explanation_pipeline),
) -> ExplanationResponse:
    try:
        explanation = pipeline.run(
            role_id=request.role_id,
            candidate_id=request.candidate_id,
            persona=request.persona,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return ExplanationResponse(
        candidate_id=explanation.candidate_id,
        role_id=explanation.role_id,
        explanation=explanation,
    )


@api_router.post("/export-rankings", tags=["exports"])
def export_rankings(
    request: ExportRankingsRequest,
    export_service: RankingExportService = Depends(get_ranking_export_service),
) -> Response:
    content = export_service.export_rankings(
        role_id=request.role_id,
        persona=request.persona.value if request.persona is not None else None,
    )
    filename = f"talentgraph-rankings-{request.role_id}.xlsx"
    return Response(
        content=content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@api_router.get("/explanations/{candidate_id}", response_model=ExplanationResponse, tags=["explanations"])
def get_explanation(
    candidate_id: str,
    repository: ExplanationRepository = Depends(get_explanation_repository),
) -> ExplanationResponse:
    explanation = repository.get_by_candidate_id(candidate_id)
    if explanation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Explanation for candidate {candidate_id} not found.",
        )
    return ExplanationResponse(
        candidate_id=explanation.candidate_id,
        role_id=explanation.role_id,
        explanation=explanation,
    )


@api_router.get("/rankings/{role_id}", response_model=RankingResponse, tags=["ranking"])
def get_rankings(
    role_id: str,
    persona: str | None = None,
    repository: RankingRepository = Depends(get_ranking_repository),
) -> RankingResponse:
    rankings = repository.list_by_role_id(role_id, persona=persona)
    response_persona = persona or "all"
    return RankingResponse(role_id=role_id, persona=response_persona, rankings=rankings)


@api_router.get("/rankings", tags=["ranking"])
def get_rankings_legacy() -> None:
    not_implemented("Legacy rankings read model")


from fastapi import Query
from app.contracts.responses.candidate_responses import PaginatedCandidateListResponse
from app.repositories.candidate_repository import CandidateFilter

@api_router.get("/candidates", response_model=PaginatedCandidateListResponse, tags=["candidates"])
def list_candidates_paginated(
    search: str | None = Query(None, description="Search by name or current role"),
    skills: list[str] = Query(None, description="Filter by skills (must have all)"),
    growth_stage: str | None = Query(None, description="Filter by growth stage"),
    min_confidence: int | None = Query(None, description="Minimum confidence score"),
    sort_by: str = Query("created_at", description="Sort by field: name, confidence, created_at"),
    page: int = Query(1, description="Page number"),
    page_size: int = Query(20, description="Page size"),
    repository: CandidateRepository = Depends(get_candidate_repository),
) -> PaginatedCandidateListResponse:
    filters = CandidateFilter(
        search=search,
        skills=skills,
        growth_stage=growth_stage,
        min_confidence=min_confidence,
        sort_by=sort_by,
        page=page,
        page_size=page_size,
    )
    result = repository.search_candidates(filters)
    return PaginatedCandidateListResponse(
        items=result.items,
        total=result.total,
        page=result.page,
        page_size=result.page_size,
    )


@api_router.get("/candidate/{candidate_id}", response_model=CandidateTwinResponse, tags=["candidates"])
def get_candidate(
    candidate_id: str,
    repository: CandidateRepository = Depends(get_candidate_repository),
) -> CandidateTwinResponse:
    twin = repository.get_by_candidate_id(candidate_id)
    if twin is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Candidate {candidate_id} not found.",
        )
    return CandidateTwinResponse(candidate_id=twin.candidate_id, twin=twin)


from app.modules.search.search_service import SearchService, SearchResult

@api_router.get("/search/candidates", response_model=list[SearchResult], tags=["search"])
def search_candidates(
    query: str | None = Query(None),
    candidate_id: str | None = Query(None),
    role_id: str | None = Query(None),
    limit: int = Query(10),
    match_type: str = Query("similar"),
    search_service: SearchService = Depends(get_search_service),
) -> list[SearchResult]:
    try:
        if query:
            return search_service.find_candidates(query=query, limit=limit)
        elif candidate_id:
            return search_service.find_similar_candidates(candidate_id=candidate_id, limit=limit, match_type=match_type)
        elif role_id:
            return search_service.find_candidates_for_role(role_id=role_id, limit=limit)
        else:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Must provide one of: query, candidate_id, or role_id",
            )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@api_router.get("/search/roles", response_model=list[SearchResult], tags=["search"])
def search_roles(
    query: str | None = Query(None),
    role_id: str | None = Query(None),
    limit: int = Query(10),
    search_service: SearchService = Depends(get_search_service),
) -> list[SearchResult]:
    try:
        if query:
            return search_service.find_roles(query=query, limit=limit)
        elif role_id:
            return search_service.find_similar_roles(role_id=role_id, limit=limit)
        else:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Must provide one of: query or role_id",
            )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc



@api_router.get("/graph/{graph_id}", response_model=GraphResponse, tags=["graph"])
def get_graph(
    graph_id: str,
    repository: GraphRepository = Depends(get_graph_repository),
) -> GraphResponse:
    graph = repository.get(graph_id)
    if graph is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Graph {graph_id} not found.")
    return GraphResponse(graph_id=graph.graph_id, graph=graph)


@api_router.get("/embeddings/{collection_id}", response_model=EmbeddingCollectionResponse, tags=["embeddings"])
def get_embeddings(
    collection_id: str,
    repository: VectorRepository = Depends(get_vector_repository),
) -> EmbeddingCollectionResponse:
    collection = repository.get(collection_id)
    if collection is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Embedding collection {collection_id} not found.",
        )
    return EmbeddingCollectionResponse(collection_id=collection.collection_id, collection=collection)


@api_router.get("/evaluations/{evaluation_id}", response_model=EvaluationResponse, tags=["evaluation"])
def get_evaluation(
    evaluation_id: str,
    repository: EvaluationRepository = Depends(get_evaluation_repository),
) -> EvaluationResponse:
    evaluation = repository.get(evaluation_id)
    if evaluation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evaluation {evaluation_id} not found.",
        )
    return EvaluationResponse(evaluation_id=evaluation.evaluation_id, evaluation=evaluation)


from app.contracts.requests.copilot_requests import CopilotDraftRequest
from app.contracts.responses.copilot_responses import CopilotDraftResponse
from app.pipelines.copilot_pipeline import CopilotPipeline

@api_router.post("/copilot/draft-email", response_model=CopilotDraftResponse, tags=["copilot"])
def draft_copilot_email(
    request: CopilotDraftRequest,
    pipeline: CopilotPipeline = Depends(get_copilot_pipeline),
) -> CopilotDraftResponse:
    try:
        response = pipeline.draft_email(role_id=request.role_id, candidate_id=request.candidate_id)
        return response
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


from app.domain.copilot import CopilotChatRequest, CopilotChatResponse
from app.modules.copilot.chat_service import CopilotChatService

@api_router.post("/copilot/chat", response_model=CopilotChatResponse, tags=["copilot"])
def copilot_chat(
    request: CopilotChatRequest,
    chat_service: CopilotChatService = Depends(get_copilot_chat_service),
) -> CopilotChatResponse:
    """Free-form recruiter chat with deterministic intent matching."""
    return chat_service.chat(request)


from pydantic import BaseModel as _BaseModel
from app.domain.comparison import ComparisonMatrix
from app.modules.comparison.service import ComparisonService
from app.repositories import CandidateRepository, RoleDNARepository

class CompareRequest(_BaseModel):
    candidate_a_id: str
    candidate_b_id: str
    role_id: str

@api_router.post("/compare", response_model=ComparisonMatrix, tags=["comparison"])
def compare_candidates(
    request: CompareRequest,
    comparison_service: ComparisonService = Depends(get_comparison_service),
    candidate_repository: CandidateRepository = Depends(get_candidate_repository),
    role_repository: RoleDNARepository = Depends(get_role_dna_repository),
) -> ComparisonMatrix:
    """Generate a side-by-side comparison matrix for two candidates against a role."""
    candidate_a = candidate_repository.get_by_candidate_id(request.candidate_a_id)
    candidate_b = candidate_repository.get_by_candidate_id(request.candidate_b_id)
    role = role_repository.get_by_role_id(request.role_id)
    if candidate_a is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Candidate A '{request.candidate_a_id}' not found.")
    if candidate_b is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Candidate B '{request.candidate_b_id}' not found.")
    if role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role '{request.role_id}' not found.")
    return comparison_service.compare(candidate_a, candidate_b, role)


from app.domain.analytics import AnalyticsOverview
from app.modules.analytics.service import AnalyticsService

@api_router.get("/analytics/overview", response_model=AnalyticsOverview, tags=["analytics"])
def get_analytics_overview(
    analytics_service: AnalyticsService = Depends(get_analytics_service),
) -> AnalyticsOverview:
    """Get high-level analytics overview for the dashboard."""
    return analytics_service.get_overview()
