"""Talent Knowledge Graph builder module."""

from app.modules.graph_builder.ontology import load_ontology
from app.modules.graph_builder.service import GraphBuilderService

__all__ = ["GraphBuilderService", "load_ontology"]
