from app.domain.candidate_twin import CandidateDigitalTwin
from app.domain.knowledge_graph import (
    GraphEntityType,
    GraphNode,
    GraphRelationship,
    GraphRelationshipType,
    KnowledgeGraph,
)
from app.domain.role_dna import RoleDNAProfile
from app.modules.graph_builder.ontology import load_ontology


class GraphBuilderService:
    """Builds deterministic graph snapshots from Role DNA and Candidate Twins."""

    def build(
        self,
        role_dna: RoleDNAProfile | None = None,
        candidate_twin: CandidateDigitalTwin | None = None,
    ) -> KnowledgeGraph:
        if role_dna is None and candidate_twin is None:
            raise ValueError("At least one role or candidate input is required to build a graph.")

        graph_id = self._graph_id(role_dna, candidate_twin)
        nodes: dict[str, GraphNode] = {}
        relationships: list[GraphRelationship] = []

        if role_dna is not None:
            self._add_role(role_dna, nodes, relationships)
        if candidate_twin is not None:
            self._add_candidate(candidate_twin, nodes, relationships)

        self._add_ontology_edges(nodes, relationships)
        return KnowledgeGraph(
            graph_id=graph_id,
            nodes=sorted(nodes.values(), key=lambda node: node.id),
            relationships=sorted(
                relationships,
                key=lambda rel: (rel.source_id, rel.type.value, rel.target_id),
            ),
        )

    def _add_role(
        self,
        role: RoleDNAProfile,
        nodes: dict[str, GraphNode],
        relationships: list[GraphRelationship],
    ) -> None:
        role_id = f"role:{role.role_id}"
        nodes[role_id] = GraphNode(
            id=role_id,
            label=GraphEntityType.ROLE,
            name=role.role_title,
            properties={"domain": role.domain, "archetype": role.role_archetype},
        )
        self._add_named_node(role.domain, GraphEntityType.DOMAIN, nodes)
        relationships.append(
            GraphRelationship(
                source_id=role_id,
                target_id=self._node_id(GraphEntityType.DOMAIN, role.domain),
                type=GraphRelationshipType.HAS_DOMAIN,
            )
        )
        for skill in [*role.required_skills, *role.preferred_skills]:
            self._add_named_node(skill, GraphEntityType.SKILL, nodes)
            relationships.append(
                GraphRelationship(
                    source_id=role_id,
                    target_id=self._node_id(GraphEntityType.SKILL, skill),
                    type=GraphRelationshipType.REQUIRES,
                    properties={"importance": role.skill_importance.get(skill)},
                )
            )

    def _add_candidate(
        self,
        candidate: CandidateDigitalTwin,
        nodes: dict[str, GraphNode],
        relationships: list[GraphRelationship],
    ) -> None:
        candidate_id = f"candidate:{candidate.candidate_id}"
        nodes[candidate_id] = GraphNode(
            id=candidate_id,
            label=GraphEntityType.CANDIDATE,
            name=candidate.name,
            properties={"growth_stage": candidate.growth_stage.value, "confidence": candidate.confidence},
        )
        for skill in candidate.skills:
            self._add_named_node(skill, GraphEntityType.SKILL, nodes)
            relationships.append(
                GraphRelationship(
                    source_id=candidate_id,
                    target_id=self._node_id(GraphEntityType.SKILL, skill),
                    type=GraphRelationshipType.HAS_SKILL,
                )
            )
        for technology in candidate.technologies:
            self._add_named_node(technology, GraphEntityType.TECHNOLOGY, nodes)
            relationships.append(
                GraphRelationship(
                    source_id=candidate_id,
                    target_id=self._node_id(GraphEntityType.TECHNOLOGY, technology),
                    type=GraphRelationshipType.USES,
                )
            )
        for project in candidate.projects:
            self._add_named_node(project, GraphEntityType.PROJECT, nodes)
            relationships.append(
                GraphRelationship(
                    source_id=candidate_id,
                    target_id=self._node_id(GraphEntityType.PROJECT, project),
                    type=GraphRelationshipType.USES,
                )
            )
        for domain in candidate.domains:
            self._add_named_node(domain, GraphEntityType.DOMAIN, nodes)
            relationships.append(
                GraphRelationship(
                    source_id=candidate_id,
                    target_id=self._node_id(GraphEntityType.DOMAIN, domain),
                    type=GraphRelationshipType.HAS_DOMAIN,
                )
            )
        for experience in candidate.experiences:
            company = self._extract_company(experience)
            if company:
                self._add_named_node(company, GraphEntityType.COMPANY, nodes)
                relationships.append(
                    GraphRelationship(
                        source_id=candidate_id,
                        target_id=self._node_id(GraphEntityType.COMPANY, company),
                        type=GraphRelationshipType.WORKED_AT,
                    )
                )

    def _add_ontology_edges(
        self,
        nodes: dict[str, GraphNode],
        relationships: list[GraphRelationship],
    ) -> None:
        ontology = load_ontology()
        known_names = {node.name.casefold(): node for node in nodes.values()}
        for source, targets in ontology["skills"].items():
            source_node = known_names.get(source.casefold())
            if source_node is None:
                continue
            for target in targets:
                target_node = known_names.get(target.casefold())
                if target_node is not None:
                    relationships.append(
                        GraphRelationship(
                            source_id=source_node.id,
                            target_id=target_node.id,
                            type=GraphRelationshipType.RELATED_TO,
                        )
                    )

    @staticmethod
    def _graph_id(role: RoleDNAProfile | None, candidate: CandidateDigitalTwin | None) -> str:
        parts = ["graph"]
        if role is not None:
            parts.append(role.role_id)
        if candidate is not None:
            parts.append(candidate.candidate_id)
        return ":".join(parts)

    @classmethod
    def _add_named_node(cls, name: str, label: GraphEntityType, nodes: dict[str, GraphNode]) -> None:
        node_id = cls._node_id(label, name)
        nodes.setdefault(node_id, GraphNode(id=node_id, label=label, name=name))

    @staticmethod
    def _node_id(label: GraphEntityType, name: str) -> str:
        slug = name.strip().casefold().replace(" ", "-").replace("/", "-")
        return f"{label.value.casefold()}:{slug}"

    @staticmethod
    def _extract_company(experience: str) -> str | None:
        marker = " at "
        lowered = experience.casefold()
        if marker not in lowered:
            return None
        return experience[lowered.index(marker) + len(marker) :].split(",", maxsplit=1)[0].strip()
