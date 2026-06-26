from app.domain.candidate_twin import CandidateDigitalTwin
from app.domain.knowledge_graph import KnowledgeGraph
from app.domain.role_dna import RoleDNAProfile
from app.domain.vector import EmbeddingCollection
from app.pipelines.embedding_pipeline import EmbeddingPipeline
from app.pipelines.graph_pipeline import GraphPipeline
from app.repositories.memory import (
    InMemoryCandidateRepository,
    InMemoryGraphRepository,
    InMemoryRoleDNARepository,
    InMemoryVectorRepository,
)


class MockGraphBuilderService:
    def build(self, role_dna: object | None = None, candidate_twin: object | None = None) -> KnowledgeGraph:
        return KnowledgeGraph(graph_id="graph_pipeline")


class MockEmbeddingService:
    def generate(
        self,
        role_dna: object | None = None,
        candidate_twin: object | None = None,
    ) -> EmbeddingCollection:
        return EmbeddingCollection(collection_id="embeddings_pipeline")


def test_graph_pipeline_builds_and_persists_graph() -> None:
    role_repository = InMemoryRoleDNARepository()
    candidate_repository = InMemoryCandidateRepository()
    graph_repository = InMemoryGraphRepository()
    role_repository.save(_role())
    candidate_repository.save(_candidate())

    graph = GraphPipeline(
        graph_builder_service=MockGraphBuilderService(),
        graph_repository=graph_repository,
        role_repository=role_repository,
        candidate_repository=candidate_repository,
    ).run(role_id="role_pipeline", candidate_id="candidate_pipeline")

    assert graph_repository.get(graph.graph_id) == graph


def test_embedding_pipeline_generates_and_persists_collection() -> None:
    role_repository = InMemoryRoleDNARepository()
    candidate_repository = InMemoryCandidateRepository()
    vector_repository = InMemoryVectorRepository()
    role_repository.save(_role())
    candidate_repository.save(_candidate())

    collection = EmbeddingPipeline(
        embedding_service=MockEmbeddingService(),
        vector_repository=vector_repository,
        role_repository=role_repository,
        candidate_repository=candidate_repository,
    ).run(role_id="role_pipeline", candidate_id="candidate_pipeline")

    assert vector_repository.get(collection.collection_id) == collection


def _role() -> RoleDNAProfile:
    return RoleDNAProfile(
        role_id="role_pipeline",
        role_title="Backend Engineer",
        domain="Backend Systems",
        seniority="Senior",
        role_archetype="Systems Builder",
        fingerprint="Builder",
        required_skills=["Python"],
        technical_depth=80,
        problem_solving=80,
        communication=70,
        ownership=75,
        leadership=60,
        learning_agility=70,
        ambiguity_tolerance=60,
        collaboration=70,
        startup_vs_enterprise_environment=55,
    )


def _candidate() -> CandidateDigitalTwin:
    return CandidateDigitalTwin(candidate_id="candidate_pipeline", name="Pipeline Candidate", skills=["Python"])
