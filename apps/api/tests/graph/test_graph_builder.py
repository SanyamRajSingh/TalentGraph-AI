from app.domain.candidate_twin import CandidateDigitalTwin
from app.domain.knowledge_graph import GraphRelationshipType
from app.domain.role_dna import RoleDNAProfile
from app.modules.graph_builder import GraphBuilderService


def test_graph_builder_constructs_nodes_and_relationships() -> None:
    role = RoleDNAProfile(
        role_id="role_test",
        role_title="Backend Engineer",
        domain="Backend Systems",
        seniority="Senior",
        role_archetype="Systems Builder",
        fingerprint="Builder",
        required_skills=["Python", "FastAPI"],
        preferred_skills=["SQL"],
        skill_importance={"Python": 50, "FastAPI": 30, "SQL": 20},
        technical_depth=90,
        problem_solving=80,
        communication=70,
        ownership=75,
        leadership=60,
        learning_agility=70,
        ambiguity_tolerance=65,
        collaboration=75,
        startup_vs_enterprise_environment=60,
    )
    candidate = CandidateDigitalTwin(
        candidate_id="candidate_test",
        name="Ada Backend",
        skills=["Python", "FastAPI"],
        technologies=["Python", "PostgreSQL"],
        projects=["Built API Platform"],
        experiences=["2024 Backend Engineer at CloudLedger"],
        domains=["Backend Systems"],
    )

    graph = GraphBuilderService().build(role_dna=role, candidate_twin=candidate)

    assert graph.graph_id == "graph:role_test:candidate_test"
    assert any(node.label.value == "Candidate" for node in graph.nodes)
    assert any(node.label.value == "Role" for node in graph.nodes)
    relationship_types = {relationship.type for relationship in graph.relationships}
    assert GraphRelationshipType.REQUIRES in relationship_types
    assert GraphRelationshipType.HAS_SKILL in relationship_types
    assert GraphRelationshipType.RELATED_TO in relationship_types
