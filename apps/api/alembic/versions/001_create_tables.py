"""Initial schema — create all TalentGraph AI tables.

Revision ID: 001
Revises:
Create Date: 2026-06-27
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # jobs
    op.create_table(
        "jobs",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("job_id", sa.String(64), unique=True, index=True, nullable=False),
        sa.Column("source_name", sa.String(255), nullable=True),
        sa.Column("payload", sa.JSON, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # role_dna_profiles
    op.create_table(
        "role_dna_profiles",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("role_id", sa.String(64), unique=True, index=True, nullable=False),
        sa.Column("job_id", sa.String(64), index=True, nullable=True),
        sa.Column("role_title", sa.String(255), nullable=False),
        sa.Column("domain", sa.String(128), nullable=False),
        sa.Column("seniority", sa.String(64), nullable=False),
        sa.Column("payload", sa.JSON, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # candidate_resumes
    op.create_table(
        "candidate_resumes",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("resume_id", sa.String(64), unique=True, index=True, nullable=False),
        sa.Column("source_name", sa.String(255), nullable=True),
        sa.Column("resume_text", sa.Text, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # candidates
    op.create_table(
        "candidates",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("candidate_id", sa.String(64), unique=True, index=True, nullable=False),
        sa.Column("resume_id", sa.String(64), index=True, nullable=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("growth_stage", sa.String(64), nullable=False),
        sa.Column("confidence", sa.Integer, nullable=False),
        sa.Column("payload", sa.JSON, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    # evaluations
    op.create_table(
        "evaluations",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("evaluation_id", sa.String(64), unique=True, index=True, nullable=False),
        sa.Column("candidate_id", sa.String(64), index=True, nullable=False),
        sa.Column("role_id", sa.String(64), index=True, nullable=False),
        sa.Column("overall_match", sa.Integer, nullable=False),
        sa.Column("overall_confidence", sa.Integer, nullable=False),
        sa.Column("payload", sa.JSON, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # rankings
    op.create_table(
        "rankings",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("candidate_id", sa.String(64), index=True, nullable=False),
        sa.Column("role_id", sa.String(64), index=True, nullable=False),
        sa.Column("persona", sa.String(64), nullable=False),
        sa.Column("rank", sa.Integer, nullable=False),
        sa.Column("score", sa.Integer, nullable=False),
        sa.Column("confidence", sa.Integer, nullable=False),
        sa.Column("evaluation_id", sa.String(64), nullable=False),
        sa.Column("payload", sa.JSON, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # explanations
    op.create_table(
        "explanations",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("candidate_id", sa.String(64), index=True, nullable=False),
        sa.Column("role_id", sa.String(64), index=True, nullable=False),
        sa.Column("ranking_position", sa.Integer, nullable=False),
        sa.Column("payload", sa.JSON, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # embeddings
    op.create_table(
        "embeddings",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("source_id", sa.String(64), index=True, nullable=False),
        sa.Column("kind", sa.String(64), nullable=False),
        sa.Column("owner_id", sa.String(64), index=True, nullable=False),
        sa.Column("text_summary", sa.Text, nullable=False),
        sa.Column("vector_dim", sa.Integer, nullable=False),
        sa.Column("payload", sa.JSON, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # graphs
    op.create_table(
        "graphs",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("graph_id", sa.String(64), unique=True, index=True, nullable=False),
        sa.Column("role_id", sa.String(64), index=True, nullable=True),
        sa.Column("candidate_id", sa.String(64), index=True, nullable=True),
        sa.Column("node_count", sa.Integer, nullable=False),
        sa.Column("payload", sa.JSON, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("graphs")
    op.drop_table("embeddings")
    op.drop_table("explanations")
    op.drop_table("rankings")
    op.drop_table("evaluations")
    op.drop_table("candidates")
    op.drop_table("candidate_resumes")
    op.drop_table("role_dna_profiles")
    op.drop_table("jobs")
