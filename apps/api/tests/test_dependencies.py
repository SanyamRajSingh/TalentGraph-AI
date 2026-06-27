from fastapi.testclient import TestClient
import os
from app.main import app
from app.api.v1.dependencies import get_copilot_repository

def test_postgres_dependencies_loadable():
    # If the files are missing, this would fail when use_postgres is true
    os.environ["DATABASE_URL"] = "sqlite:///./test.db"
    os.environ["USE_POSTGRES"] = "true"
    try:
        repo = get_copilot_repository()
        assert repo is not None
    finally:
        os.environ.pop("DATABASE_URL", None)
        os.environ.pop("USE_POSTGRES", None)
