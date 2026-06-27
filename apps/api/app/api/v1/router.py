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


@api_router.get("/candidates", response_model=CandidateListResponse, tags=["candidates"])
def list_candidates(
    repository: CandidateRepository = Depends(get_candidate_repository),
) -> CandidateListResponse:
    return CandidateListResponse(items=repository.list_candidates())


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
