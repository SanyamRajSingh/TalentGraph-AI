from enum import StrEnum

from pydantic import BaseModel, Field


class GraphEntityType(StrEnum):
    CANDIDATE = "Candidate"
    ROLE = "Role"
    SKILL = "Skill"
    TECHNOLOGY = "Technology"
    PROJECT = "Project"
    COMPANY = "Company"
    DOMAIN = "Domain"


class GraphRelationshipType(StrEnum):
    HAS_SKILL = "HAS_SKILL"
    RELATED_TO = "RELATED_TO"
    USES = "USES"
    BELONGS_TO = "BELONGS_TO"
    REQUIRES = "REQUIRES"
    WORKED_AT = "WORKED_AT"
    HAS_DOMAIN = "HAS_DOMAIN"


class GraphNode(BaseModel):
    id: str
    label: GraphEntityType
    name: str
    properties: dict[str, str | int | float | bool | None] = Field(default_factory=dict)


class GraphRelationship(BaseModel):
    source_id: str
    target_id: str
    type: GraphRelationshipType
    properties: dict[str, str | int | float | bool | None] = Field(default_factory=dict)


class KnowledgeGraph(BaseModel):
    graph_id: str
    nodes: list[GraphNode] = Field(default_factory=list)
    relationships: list[GraphRelationship] = Field(default_factory=list)
