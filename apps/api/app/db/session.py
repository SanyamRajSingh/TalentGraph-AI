"""SQLAlchemy engine and session factory.

The engine is created lazily on first access so that in-memory-only
deployments (DATABASE_URL unset) never import database drivers.
"""

from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.settings import get_settings


class Base(DeclarativeBase):
    """Shared declarative base for all ORM models."""


_engine = None
_SessionLocal = None


def _get_engine():
    global _engine  # noqa: PLW0603
    if _engine is None:
        settings = get_settings()
        url = settings.database_url
        if not url:
            raise RuntimeError(
                "DATABASE_URL is not set. Cannot create a database engine. "
                "Use in-memory repositories instead."
            )
        # SQLite needs check_same_thread=False for use in FastAPI
        connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
        _engine = create_engine(url, connect_args=connect_args, echo=False)
    return _engine


def _get_session_local():
    global _SessionLocal  # noqa: PLW0603
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_get_engine())
    return _SessionLocal


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a database session and closes it after use."""
    SessionLocal = _get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables() -> None:
    """Create all tables defined in ORM models. Used for tests and SQLite fallback."""
    from app.db import models as _  # noqa: F401 — register models
    Base.metadata.create_all(bind=_get_engine())


def verify_connection() -> bool:
    """Verify that the database is reachable. Returns True on success."""
    try:
        engine = _get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
