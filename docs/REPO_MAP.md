# Repository Map

This document explains the repository layout for TalentGraph AI. It is written for a future AI engineer with no prior conversation context.

## Root

```text
.
|-- .dockerignore
|-- .env.example
|-- .gitignore
|-- README.md
|-- docker-compose.yml
|-- package.json
|-- apps/
|-- data/
|-- docs/
|-- infra/
|-- packages/
`-- requirements/
```

### `.env.example`

Environment variable template for local development and future deployment.

Important variables:

- `APP_NAME`
- `APP_ENV`
- `API_HOST`
- `API_PORT`
- `NEXT_PUBLIC_API_BASE_URL`
- `POSTGRES_*`
- `NEO4J_*`
- `CHROMA_*`
- `OPENAI_API_KEY`
- `EMBEDDING_MODEL`
- feature flags for major modules

The current test path uses in-memory repositories and deterministic local providers, so external services are not required.

### `README.md`

Project README. Updated for v1.0 to describe implemented Modules 1-7, architecture, module flow, API endpoints, setup, screenshots, and known limitations.

### `docker-compose.yml`

Defines services for:

- `api`
- `web`
- `postgres`
- `neo4j`
- `chromadb`

The current backend can run without PostgreSQL, Neo4j, or Chroma because memory repositories are wired by default.

### `package.json`

Root npm workspace definition.

Current workspace packages:

```json
{
  "workspaces": ["apps/web", "packages/shared"]
}
```

## `requirements/`

Python dependency groups.

```text
requirements/
|-- base.txt
|-- dev.txt
`-- ai.txt
```

### `requirements/base.txt`

Runtime backend dependencies:

- FastAPI
- Pydantic
- Pydantic Settings
- SQLAlchemy
- Uvicorn
- python-multipart

### `requirements/dev.txt`

Development and test dependencies:

- pytest
- pytest-asyncio
- httpx

### `requirements/ai.txt`

Optional AI dependencies isolated from the base runtime:

- OpenAI
- LangChain
- sentence-transformers
- chromadb
- torch

Do not add heavy AI libraries to `base.txt`.

## `apps/`

Application packages.

```text
apps/
|-- api/
`-- web/
```

## `apps/api/`

FastAPI backend.

```text
apps/api/
|-- pyproject.toml
|-- app/
`-- tests/
```

### `apps/api/pyproject.toml`

Python package metadata, dependency declarations, pytest config, and lint config.

## `apps/api/app/`

Backend source tree.

```text
apps/api/app/
|-- api/
|-- ai/
|-- contracts/
|-- core/
|-- db/
|-- domain/
|-- events/
|-- graph/
|-- modules/
|-- pipelines/
|-- providers/
|-- repositories/
|-- vector/
|-- workflows/
`-- main.py
```

### `apps/api/app/main.py`

Creates the FastAPI application, configures CORS, exposes `/health`, and mounts the v1 API router under `/api/v1`.

### `apps/api/app/api/v1/router.py`

Primary HTTP boundary. Contains implemented endpoints for Modules 1-7 and 501 placeholders for explicitly postponed future endpoints.

Implemented endpoints:

- `POST /api/v1/upload-job`
- `POST /api/v1/generate-role-dna`
- `GET /api/v1/role-dna`
- `GET /api/v1/role-dna/{role_id}`
- `POST /api/v1/upload-candidates`
- `POST /api/v1/build-digital-twins`
- `GET /api/v1/candidates`
- `GET /api/v1/candidate/{candidate_id}`
- `POST /api/v1/build-graph`
- `GET /api/v1/graph/{graph_id}`
- `POST /api/v1/generate-embeddings`
- `GET /api/v1/embeddings/{collection_id}`
- `POST /api/v1/evaluate`
- `GET /api/v1/evaluations/{evaluation_id}`
- `POST /api/v1/rank`
- `GET /api/v1/rankings/{role_id}`
- `POST /api/v1/generate-explanations`
- `GET /api/v1/explanations/{candidate_id}`
- `POST /api/v1/export-rankings`

Known future or legacy placeholder endpoints:

- `POST /api/v1/rank-candidates`
- `GET /api/v1/rankings`

### `apps/api/app/api/v1/dependencies.py`

Runtime dependency injection wiring.

Currently wires:

- in-memory repositories
- deterministic local providers
- services
- pipelines

This is the main file to change when swapping memory repositories for PostgreSQL, Neo4j, Chroma, or real AI providers.

## `apps/api/app/domain/`

Canonical Pydantic domain models.

```text
domain/
|-- candidate_twin.py
|-- evaluation.py
|-- explanation.py
|-- knowledge_graph.py
|-- ranking.py
|-- role_dna.py
|-- vector.py
`-- __init__.py
```

Important files:

- `role_dna.py`: `RoleJob`, `WorkEnvironmentAttributes`, `RoleDNAProfile`.
- `candidate_twin.py`: `GrowthStage`, `CandidateResume`, `CandidateTimelineEntry`, `CandidateDigitalTwin`.
- `knowledge_graph.py`: graph entity types, relationship types, nodes, relationships, graph aggregate.
- `vector.py`: summary and embedding record models.
- `evaluation.py`: `EvaluatorResult`, `EvaluationBundle`.
- `ranking.py`: `HiringPersona`, `RankingResult`.
- `explanation.py`: `ExplanationProfile`.

## `apps/api/app/modules/`

Business logic grouped by module.

```text
modules/
|-- candidates/
|-- embeddings/
|-- evaluators/
|-- explanations/
|-- exports/
|-- graph_builder/
|-- ranking/
|-- recruiter_brain/
|-- role_dna/
`-- scoring/
```

### `modules/role_dna/`

Module 1 business logic.

Important files:

- `service.py`: `RoleDNAService`; owns Role DNA business logic.
- `normalizer.py`: deterministic normalization and validation helpers.
- `local_provider.py`: local deterministic LLM-like provider.
- `prompts.py`: prompt boundary for future LLM provider use.

### `modules/candidates/`

Module 2 business logic.

Important files:

- `service.py`: `CandidateDigitalTwinService`; owns candidate twin construction.
- `normalizer.py`: deterministic candidate normalization helpers.
- `local_parser_provider.py`: local deterministic resume parser.

### `modules/graph_builder/`

Module 3 graph business logic.

Important files:

- `service.py`: `GraphBuilderService`; constructs deterministic graph nodes and relationships.
- `ontology.py`: loads ontology seed files from `data/ontology`.

### `modules/embeddings/`

Module 3 embedding foundation.

Important files:

- `summary_service.py`: deterministic role and candidate summaries.
- `service.py`: embedding orchestration logic inside service boundary.
- `local_provider.py`: deterministic local embedding provider.

### `modules/evaluators/`

Module 4 deterministic evaluator modules.

Important files:

- `technical.py`: required/preferred skill overlap, technical depth, project complexity.
- `growth.py`: learning velocity, growth stage, consistency, leadership.
- `domain.py`: domain overlap, transferable skills, adjacent ontology technologies.
- `culture.py`: communication, ownership, collaboration, ambiguity tolerance.
- `service.py`: `EvaluationService`; combines evaluator outputs.
- `utils.py`: score clamping and shared evaluator helpers.

### `modules/ranking/`

Module 5 ranking business logic.

Important files:

- `service.py`: `RankingService`; loads evaluations, applies persona weights, sorts rankings, persists results.

### `modules/recruiter_brain/`

Persona and future recruiter intelligence boundary.

Important files:

- `persona_engine.py`: implemented for Module 5; provides persona weights.

### `modules/scoring/`

Scoring extension boundary.

Important files:

- `weight_registry.py`: wraps persona weight access for ranking.

### `modules/explanations/`

Module 6 explanation and counterfactual logic.

Important files:

- `service.py`: deterministic strengths, risks, reasoning, and profile persistence.
- `counterfactual_service.py`: score-gap-driven improvement suggestions.

### `modules/exports/`

Future module. Do not implement unless the user explicitly approves exports.

## `apps/api/app/pipelines/`

Orchestration layer.

```text
pipelines/
|-- candidate_pipeline.py
|-- embedding_pipeline.py
|-- evaluation_pipeline.py
|-- graph_pipeline.py
|-- ranking_pipeline.py
|-- role_pipeline.py
`-- __init__.py
```

Rules:

- Pipelines orchestrate only.
- Pipelines should not contain business logic.
- Pipelines should not call external providers directly.
- Pipelines may coordinate repositories and services.

Current pipelines:

- `RolePipeline`
- `CandidatePipeline`
- `GraphPipeline`
- `EmbeddingPipeline`
- `EvaluationPipeline`
- `RankingPipeline`

## `apps/api/app/providers/`

Provider interfaces.

```text
providers/
|-- embedding_provider.py
|-- llm_provider.py
|-- parser_provider.py
`-- __init__.py
```

Provider rules:

- Providers handle external model, parser, or embedding calls.
- Current implementations are deterministic local providers.
- Future OpenAI, LangChain, or sentence-transformers integrations should implement these interfaces.

## `apps/api/app/repositories/`

Repository interfaces and persistence implementations.

```text
repositories/
|-- candidate_repository.py
|-- evaluation_repository.py
|-- graph_repository.py
|-- ranking_repository.py
|-- role_dna_repository.py
|-- vector_repository.py
|-- memory/
|-- postgres/
|-- neo4j/
`-- chroma/
```

### Repository interfaces

- `candidate_repository.py`
- `evaluation_repository.py`
- `graph_repository.py`
- `ranking_repository.py`
- `role_dna_repository.py`
- `vector_repository.py`

### `repositories/memory/`

Fully functional in-memory repositories for tests and local demo:

- `in_memory_candidate_repository.py`
- `in_memory_evaluation_repository.py`
- `in_memory_graph_repository.py`
- `in_memory_ranking_repository.py`
- `in_memory_vector_repository.py`
- `role_dna_repository.py`

### `repositories/postgres/`

Skeleton PostgreSQL repositories:

- candidate repository skeleton
- evaluation repository skeleton
- ranking repository skeleton
- role DNA repository skeleton

These are intentionally not production-ready.

### `repositories/neo4j/`

Skeleton Neo4j graph repository.

### `repositories/chroma/`

Skeleton Chroma vector repository.

## `apps/api/app/contracts/`

Request and response DTO boundary.

```text
contracts/
|-- requests/
`-- responses/
```

Use this package for future API request/response schemas when `router.py` becomes too large.

## `apps/api/app/core/`

Shared backend configuration and infrastructure helpers.

Important files:

- `config.py`: settings.
- `feature_flags.py`: feature flag boundary.
- `logging.py`: logging setup boundary.
- `tracing.py`: tracing boundary.

## `apps/api/app/events/`

Event names and event boundaries for future asynchronous workflows.

Events requested during architecture setup:

- `JobUploaded`
- `RoleDNAGenerated`
- `CandidateUploaded`
- `DigitalTwinBuilt`
- `RankingGenerated`
- `ExplanationGenerated`

## `apps/api/app/workflows/`

Workflow state boundary.

Important files:

- `processing_state.py`
- `workflow_manager.py`

These are scaffolding and should not become business logic containers.

## `apps/api/tests/`

Pytest suite.

```text
tests/
|-- candidate/
|-- evaluation/
|-- graph/
|-- ranking/
|-- role_dna/
`-- test_health.py
```

Current known test status:

```text
53 passed, 1 warning
```

Run command:

```powershell
python -m pytest apps/api/tests
```

Known-good command in this Codex environment:

```powershell
C:\Users\sanya\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m pytest apps/api/tests
```

## `apps/web/`

Next.js frontend.

```text
apps/web/
|-- app/
|   |-- globals.css
|   |-- layout.tsx
|   `-- page.tsx
|-- package.json
|-- next.config.ts
|-- postcss.config.js
|-- tailwind.config.ts
`-- tsconfig.json
```

### `apps/web/app/page.tsx`

Single-page dashboard UI for Modules 1-7.

Current panels:

- Role DNA Generator
- Candidate Digital Twin
- Candidate Evaluation
- Ranking Engine
- Knowledge Graph
- Embedding Inspection

Known frontend status:

- Source files exist.
- Frontend build has been successfully verified with `npm.cmd --workspace apps/web run build`.

### `apps/web/app/globals.css`

Tailwind and global styles.

### `apps/web/app/layout.tsx`

Next.js root layout metadata and wrapper.

## `packages/shared/`

Shared TypeScript package.

```text
packages/shared/
`-- src/
    `-- index.ts
```

### `packages/shared/src/index.ts`

Shared TypeScript types corresponding to backend concepts.

Note: `apps/web/app/page.tsx` currently defines local API response types. Future cleanup can migrate those to `packages/shared`.

## `data/`

Demo data and seed data.

```text
data/
|-- jobs/
|-- ontology/
|-- resumes/
|-- samples/
|-- seeds/
`-- structured/
```

### `data/jobs/`

Sample job descriptions:

- `data-scientist-fintech.md`
- `backend-engineer-startup.md`
- `ml-engineer-enterprise.md`
- `product-analyst.md`

### `data/resumes/`

Sample resumes:

- `junior-python-developer.md`
- `ml-engineer.md`
- `backend-engineer.md`
- `product-analyst.md`

### `data/ontology/`

Seed ontology files:

- `skills.json`
- `technologies.json`
- `domains.json`

Used by graph construction and domain evaluation.

### `data/structured/`

Placeholder for normalized structured artifacts.

### `data/samples/` and `data/seeds/`

Scaffolded sample/seed folders. Verify actual usage before adding logic that depends on them.

## `infra/docker/`

Dockerfiles:

- `api.Dockerfile`
- `web.Dockerfile`

These support future containerized local development.

## `docs/`

Handoff and architecture documentation.

```text
docs/
|-- AI_MEMORY.md
|-- ARCHITECTURE.md
|-- CURRENT_STATUS.md
|-- NEXT_TASKS.md
|-- PROJECT_HANDOFF.md
|-- REPO_MAP.md
`-- SESSION_STATE.md
```

Recommended reading order for future AI sessions:

1. `SESSION_STATE.md`
2. `CURRENT_STATUS.md`
3. `AI_MEMORY.md`
4. `NEXT_TASKS.md`
5. `ARCHITECTURE.md`
6. `PROJECT_HANDOFF.md`
7. `REPO_MAP.md`

## Important Navigation Tips

For backend behavior:

1. Start at `apps/api/app/api/v1/router.py`.
2. Check dependency wiring in `apps/api/app/api/v1/dependencies.py`.
3. Follow the relevant pipeline in `apps/api/app/pipelines/`.
4. Follow the service in `apps/api/app/modules/`.
5. Check domain models in `apps/api/app/domain/`.
6. Check repository interfaces and memory implementations in `apps/api/app/repositories/`.

For frontend behavior:

1. Start at `apps/web/app/page.tsx`.
2. Check styling in `apps/web/app/globals.css`.
3. Check shared types in `packages/shared/src/index.ts`.

For tests:

1. Match the feature to the folder under `apps/api/tests/`.
2. Prefer adding focused unit tests for service/evaluator behavior.
3. Add API tests only for new or changed HTTP behavior.

# START HERE FOR NEXT AI SESSION

1. Read `docs/SESSION_STATE.md` first.
2. Run the backend test suite with `python -m pytest apps/api/tests`.
3. If tests pass, inspect `docs/NEXT_TASKS.md`.
4. Ask the user which next module or cleanup task is approved before implementing new features.
5. Preserve the established architecture boundaries: pipelines orchestrate, services/modules own business logic, providers handle external calls, and repositories persist.
