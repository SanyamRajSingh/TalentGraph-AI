import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.api.v1.router import api_router
from app.core.settings import get_settings
from app.core.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: initialise database tables and seed demo data."""
    # ── PostgreSQL: create tables ────────────────────────────────────────────
    if settings.use_postgres:
        from app.db.session import create_tables
        try:
            create_tables()
            logger.info("Database tables verified / created.")
        except Exception as exc:
            logger.warning("Could not create database tables: %s", exc)

    # ── Startup seeding ──────────────────────────────────────────────────────
    try:
        from app.api.v1.dependencies import (
            get_candidate_repository,
            get_role_dna_repository,
            get_evaluation_pipeline,
            get_ranking_pipeline,
            get_explanation_pipeline,
            get_embedding_pipeline,
            get_graph_pipeline,
        )
        from app.startup.seeder import seed

        seed(
            candidate_repository=get_candidate_repository(),
            role_repository=get_role_dna_repository(),
            evaluation_pipeline=get_evaluation_pipeline(),
            ranking_pipeline=get_ranking_pipeline(),
            explanation_pipeline=get_explanation_pipeline(),
            embedding_pipeline=get_embedding_pipeline(),
            graph_pipeline=get_graph_pipeline(),
        )
    except Exception as exc:
        logger.warning("Startup seeder failed (non-fatal): %s", exc)

    yield  # ← application runs here

    logger.info("Application shutdown.")


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Explainable Hiring Intelligence Platform API",
    docs_url="/docs" if settings.app_env != "production" else None,
    redoc_url="/redoc" if settings.app_env != "production" else None,
    openapi_url="/openapi.json" if settings.app_env != "production" else None,
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store, max-age=0"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.app_name,
        "env": settings.app_env,
        "version": "0.1.0",
    }


app.include_router(api_router, prefix="/api/v1")
