"""Phase 1 tests — PostgreSQL repositories via SQLite in-memory.

These tests use SQLAlchemy's SQLite backend so no real PostgreSQL is required
in CI. They verify the full CRUD contract for each repository.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.session import Base
import app.db.models  # noqa: F401 — register ORM tables

from app.domain.candidate_twin import CandidateDigitalTwin, CandidateResume, GrowthStage
from app.domain.evaluation import EvaluationBundle, EvaluatorResult
from app.domain.explanation import ExplanationProfile
from app.domain.ranking import HiringPersona, RankingResult
from app.domain.role_dna import RoleDNAProfile, RoleJob
from app.repositories.postgres.postgres_candidate_repository import PostgresCandidateRepository
from app.repositories.postgres.postgres_evaluation_repository import PostgresEvaluationRepository
from app.repositories.postgres.postgres_explanation_repository import PostgresExplanationRepository
from app.repositories.postgres.postgres_ranking_repository import PostgresRankingRepository
from app.repositories.postgres.role_dna_repository import PostgresRoleDNARepository


@pytest.fixture(scope="module")
def sqlite_session():
    """Provide a SQLite in-memory session for testing Postgres repos."""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    engine.dispose()


# ─────────────────────────────────────────────────────────────────────────────
# CandidateRepository
# ─────────────────────────────────────────────────────────────────────────────

class TestPostgresCandidateRepository:
    def test_save_and_get_resume(self, sqlite_session):
        repo = PostgresCandidateRepository(session=sqlite_session)
        resume = CandidateResume(resume_text="Alice's resume text", source_name="test")
        saved = repo.save_resume(resume)
        assert saved.resume_id == resume.resume_id

        fetched = repo.get_resume(resume.resume_id)
        assert fetched is not None
        assert fetched.resume_text == "Alice's resume text"

    def test_get_resume_not_found(self, sqlite_session):
        repo = PostgresCandidateRepository(session=sqlite_session)
        assert repo.get_resume("nonexistent_resume") is None

    def test_save_and_get_twin(self, sqlite_session):
        repo = PostgresCandidateRepository(session=sqlite_session)
        twin = CandidateDigitalTwin(
            name="Alice Chen",
            skills=["Python", "ML"],
            growth_stage=GrowthStage.BUILDER,
            confidence=82,
        )
        saved = repo.save(twin)
        assert saved.candidate_id == twin.candidate_id

        fetched = repo.get_by_candidate_id(twin.candidate_id)
        assert fetched is not None
        assert fetched.name == "Alice Chen"
        assert "Python" in fetched.skills

    def test_list_candidates(self, sqlite_session):
        repo = PostgresCandidateRepository(session=sqlite_session)
        initial_count = len(repo.list_candidates())
        twin = CandidateDigitalTwin(name="Bob Smith", skills=["Java"])
        repo.save(twin)
        assert len(repo.list_candidates()) == initial_count + 1

    def test_update_existing_twin(self, sqlite_session):
        repo = PostgresCandidateRepository(session=sqlite_session)
        twin = CandidateDigitalTwin(name="Carol White", skills=["Go"])
        repo.save(twin)
        twin.skills = ["Go", "Rust"]
        repo.save(twin)
        fetched = repo.get_by_candidate_id(twin.candidate_id)
        assert "Rust" in fetched.skills


# ─────────────────────────────────────────────────────────────────────────────
# RoleDNARepository
# ─────────────────────────────────────────────────────────────────────────────

class TestPostgresRoleDNARepository:
    def test_save_and_get_job(self, sqlite_session):
        repo = PostgresRoleDNARepository(session=sqlite_session)
        job = RoleJob(job_description="We need a senior ML engineer", source_name="test")
        saved = repo.save_job(job)
        assert saved.job_id == job.job_id

        fetched = repo.get_job(job.job_id)
        assert fetched is not None
        assert "ML engineer" in fetched.job_description

    def test_save_and_get_role_dna(self, sqlite_session):
        repo = PostgresRoleDNARepository(session=sqlite_session)
        role = RoleDNAProfile(
            role_title="ML Engineer",
            domain="Machine Learning",
            seniority="Senior",
            role_archetype="Builder",
            fingerprint="ml-senior-builder",
            technical_depth=80,
            problem_solving=75,
            communication=60,
            ownership=70,
            leadership=55,
            learning_agility=75,
            ambiguity_tolerance=70,
            collaboration=65,
            startup_vs_enterprise_environment=60,
        )
        repo.save(role)
        fetched = repo.get_by_role_id(role.role_id)
        assert fetched is not None
        assert fetched.role_title == "ML Engineer"

    def test_list_role_dna(self, sqlite_session):
        repo = PostgresRoleDNARepository(session=sqlite_session)
        initial = len(repo.list_role_dna())
        role = RoleDNAProfile(
            role_title="Backend Engineer",
            domain="Engineering",
            seniority="Mid",
            role_archetype="Operator",
            fingerprint="be-mid-operator",
            technical_depth=70,
            problem_solving=65,
            communication=60,
            ownership=65,
            leadership=45,
            learning_agility=65,
            ambiguity_tolerance=55,
            collaboration=70,
            startup_vs_enterprise_environment=50,
        )
        repo.save(role)
        assert len(repo.list_role_dna()) == initial + 1


# ─────────────────────────────────────────────────────────────────────────────
# EvaluationRepository
# ─────────────────────────────────────────────────────────────────────────────

class TestPostgresEvaluationRepository:
    def test_save_and_get(self, sqlite_session):
        repo = PostgresEvaluationRepository(session=sqlite_session)
        evaluation = EvaluationBundle(
            candidate_id="candidate_abc",
            role_id="role_xyz",
            overall_match=78,
            overall_confidence=80,
        )
        repo.save(evaluation)
        fetched = repo.get(evaluation.evaluation_id)
        assert fetched is not None
        assert fetched.overall_match == 78

    def test_list_by_role_id(self, sqlite_session):
        repo = PostgresEvaluationRepository(session=sqlite_session)
        role_id = "role_list_test"
        e1 = EvaluationBundle(candidate_id="c1", role_id=role_id, overall_match=70)
        e2 = EvaluationBundle(candidate_id="c2", role_id=role_id, overall_match=85)
        repo.save(e1)
        repo.save(e2)
        results = repo.list_by_role_id(role_id)
        assert len(results) == 2

    def test_get_not_found(self, sqlite_session):
        repo = PostgresEvaluationRepository(session=sqlite_session)
        assert repo.get("nonexistent_eval") is None


# ─────────────────────────────────────────────────────────────────────────────
# RankingRepository
# ─────────────────────────────────────────────────────────────────────────────

class TestPostgresRankingRepository:
    def test_save_many_and_list(self, sqlite_session):
        repo = PostgresRankingRepository(session=sqlite_session)
        role_id = "role_rank_test"
        rankings = [
            RankingResult(
                candidate_id=f"c{i}",
                role_id=role_id,
                rank=i + 1,
                persona=HiringPersona.STARTUP_FOUNDER,
                score=90 - i * 10,
                confidence=80,
                evaluation_id=f"eval_{i}",
            )
            for i in range(3)
        ]
        repo.save_many(rankings)
        results = repo.list_by_role_id(role_id, persona="startup_founder")
        assert len(results) == 3
        assert results[0].rank == 1

    def test_persona_filter(self, sqlite_session):
        repo = PostgresRankingRepository(session=sqlite_session)
        role_id = "role_persona_filter"
        r1 = RankingResult(
            candidate_id="cx",
            role_id=role_id,
            rank=1,
            persona=HiringPersona.STARTUP_FOUNDER,
            score=85,
            confidence=80,
            evaluation_id="e1",
        )
        r2 = RankingResult(
            candidate_id="cy",
            role_id=role_id,
            rank=1,
            persona=HiringPersona.ENTERPRISE_RECRUITER,
            score=90,
            confidence=85,
            evaluation_id="e2",
        )
        repo.save_many([r1, r2])
        startup = repo.list_by_role_id(role_id, persona="startup_founder")
        assert len(startup) == 1
        enterprise = repo.list_by_role_id(role_id, persona="enterprise_recruiter")
        assert len(enterprise) == 1


# ─────────────────────────────────────────────────────────────────────────────
# ExplanationRepository
# ─────────────────────────────────────────────────────────────────────────────

class TestPostgresExplanationRepository:
    def test_save_and_get_by_candidate(self, sqlite_session):
        repo = PostgresExplanationRepository(session=sqlite_session)
        profile = ExplanationProfile(
            candidate_id="cand_exp_1",
            role_id="role_exp_1",
            ranking_position=2,
            strengths=["Strong Python skills"],
            risks=["Limited leadership"],
        )
        repo.save(profile)
        fetched = repo.get_by_candidate_id("cand_exp_1")
        assert fetched is not None
        assert fetched.ranking_position == 2

    def test_save_replaces_previous(self, sqlite_session):
        repo = PostgresExplanationRepository(session=sqlite_session)
        candidate_id = "cand_exp_replace"
        role_id = "role_exp_replace"
        p1 = ExplanationProfile(
            candidate_id=candidate_id,
            role_id=role_id,
            ranking_position=3,
        )
        p2 = ExplanationProfile(
            candidate_id=candidate_id,
            role_id=role_id,
            ranking_position=1,
        )
        repo.save(p1)
        repo.save(p2)
        fetched = repo.get_by_candidate_id(candidate_id)
        assert fetched.ranking_position == 1

    def test_get_not_found(self, sqlite_session):
        repo = PostgresExplanationRepository(session=sqlite_session)
        assert repo.get_by_candidate_id("nonexistent_cand") is None


# ─────────────────────────────────────────────────────────────────────────────
# Settings — use_postgres property
# ─────────────────────────────────────────────────────────────────────────────

class TestSettingsUsePostgres:
    def test_no_url_returns_false(self):
        from app.core.settings import Settings
        s = Settings(DATABASE_URL="")
        assert s.use_postgres is False

    def test_sqlite_url_returns_false(self):
        from app.core.settings import Settings
        s = Settings(DATABASE_URL="sqlite:///./local.db")
        assert s.use_postgres is False

    def test_postgres_url_returns_true(self):
        from app.core.settings import Settings
        s = Settings(DATABASE_URL="postgresql://user:pass@localhost/db")
        assert s.use_postgres is True

    def test_postgresql_plus_psycopg2(self):
        from app.core.settings import Settings
        s = Settings(DATABASE_URL="postgresql+psycopg2://user:pass@localhost/db")
        assert s.use_postgres is True
