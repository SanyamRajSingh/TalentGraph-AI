import sys
import os

from app.domain.evaluation import EvaluationBundle
from app.db.session import _get_session_local, create_tables
from app.repositories.postgres.postgres_evaluation_repository import PostgresEvaluationRepository

# Force sqlite for local test
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["USE_POSTGRES"] = "true"

create_tables()
session = _get_session_local()()
repo = PostgresEvaluationRepository(session)

# Create dummy bundle
b = EvaluationBundle(candidate_id="c1", role_id="r1", overall_match=100, overall_confidence=100)
repo.save(b)

res = repo.list_by_role_id("r1")
print(f"Found {len(res)} evaluations")
