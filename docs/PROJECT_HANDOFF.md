# TalentGraph AI Project Handoff

## Project Name

TalentGraph AI

## Product Tagline

Explainable Hiring Intelligence Platform

## Project Vision

TalentGraph AI is a hackathon-oriented hiring intelligence platform that evaluates candidates based on predicted role fit, growth trajectory, technical signals, and transparent reasoning rather than naive resume keyword matching.

Traditional applicant tracking systems usually follow this flow:

```text
Job Description -> Extract Keywords -> Match Resume Keywords -> Rank Candidates
```

TalentGraph AI is designed to follow a richer intelligence flow:

```text
Job Description
-> Understand Role DNA
-> Build Candidate Digital Twins
-> Build Semantic Foundations
-> Evaluate Candidate-Role Fit
-> Rank Candidates by Hiring Persona
-> Explain Recommendations
```

The product should feel like an AI recruiter that reasons across multiple dimensions, not like a search engine.

## Problem Statement

Recruiters and hiring managers often need to compare candidates whose resumes use different language, levels of detail, and styles. Keyword matching misses adjacent skills, transferable experience, learning velocity, ownership, and domain context. TalentGraph AI aims to structure both the role and candidates into normalized, explainable objects, then apply deterministic and testable modules that make the evaluation process transparent.

## End Users

- Startup founders who care about ownership, learning speed, and ambiguity tolerance.
- Enterprise recruiters who care about skill alignment, experience, domain fit, and communication.
- Research or technical leads who care about problem solving, technical depth, research orientation, and domain transferability.
- Hackathon judges or demo viewers who need a polished end-to-end product flow.

## Primary Use Cases

1. Paste a job description and generate a Role DNA profile.
2. Paste resume text and generate a Candidate Digital Twin.
3. Build a simple Talent Knowledge Graph from role and candidate entities.
4. Generate deterministic summaries and local embeddings for inspection.
5. Evaluate how well a candidate matches a role across technical, growth, domain, and culture dimensions.
6. Rank evaluated candidates under a selected hiring persona.

## Current Tech Stack

### Monorepo

- Root `package.json` defines npm workspaces:
  - `apps/web`
  - `packages/shared`

### Frontend

- Next.js 15
- React 19
- TypeScript
- Tailwind CSS
- lucide-react icons
- Framer Motion is installed but not materially used yet.

Frontend app path:

```text
apps/web
```

### Backend

- Python 3.12
- FastAPI
- Pydantic v2
- pydantic-settings
- SQLAlchemy dependency present for future persistence skeletons
- Uvicorn
- pytest
- httpx for FastAPI TestClient dependencies

Backend app path:

```text
apps/api
```

### Optional AI Dependencies

AI dependencies are intentionally isolated in:

```text
requirements/ai.txt
```

They include:

- openai
- langchain
- sentence-transformers
- chromadb
- torch

The implemented modules do not require network calls or external AI services. Local deterministic providers are used.

### Planned/Stubbed Infrastructure

`docker-compose.yml` includes:

- API service
- Web service
- PostgreSQL
- Neo4j
- ChromaDB

Current code uses in-memory repositories for tests and demo flows. PostgreSQL, Neo4j, and Chroma repository classes are skeletons.

An initial baseline commit has been created after the README refresh:

```text
Implement TalentGraph AI modules 1-5
```

## Dependency Files

```text
requirements/base.txt
requirements/dev.txt
requirements/ai.txt
apps/api/pyproject.toml
apps/web/package.json
package.json
```

Backend dependency groups:

- `requirements/base.txt`: FastAPI, Pydantic, SQLAlchemy, Uvicorn, multipart support.
- `requirements/dev.txt`: base plus pytest, pytest-asyncio, httpx.
- `requirements/ai.txt`: optional AI/vector packages.

`apps/api/pyproject.toml` also exposes optional extras:

```text
[project.optional-dependencies]
dev
ai
postgres
```

## High-Level Architecture

The backend is organized around the pattern:

```text
API Router
-> Pipeline
-> Service
-> Provider and/or Repository
-> Domain Models
```

Important rule: routers should not contain business logic. Pipelines orchestrate. Services implement business logic. Providers wrap parsing, LLM, or embedding mechanisms. Repositories persist and retrieve data.

### Implemented Pipeline Patterns

Role DNA:

```text
RolePipeline
-> RoleDNAService
-> LLMProvider
-> RoleDNARepository
```

Candidate Digital Twin:

```text
CandidatePipeline
-> CandidateDigitalTwinService
-> ParserProvider
-> CandidateRepository
```

Graph:

```text
GraphPipeline
-> GraphBuilderService
-> GraphRepository
```

Embedding:

```text
EmbeddingPipeline
-> EmbeddingFoundationService
-> SummaryService
-> EmbeddingProvider
-> VectorRepository
```

Evaluation:

```text
EvaluationPipeline
-> EvaluationService
-> TechnicalEvaluator/GrowthEvaluator/DomainEvaluator/CultureEvaluator
-> EvaluationRepository
```

Ranking:

```text
RankingPipeline
-> RankingService
-> PersonaEngine
-> RankingRepository
```

## Folder Structure Overview

```text
apps/
  api/
    app/
      api/v1/             FastAPI routes and dependency injection
      contracts/          Request and response DTOs
      core/               Settings, logging, tracing, feature flags
      domain/             Canonical backend domain models
      events/             Domain event contracts
      modules/            Business logic modules
      pipelines/          Orchestration layer
      providers/          Abstract provider interfaces
      repositories/       Repository interfaces and implementations
      workflows/          Workflow state abstractions
    tests/                Pytest suite
  web/                    Next.js frontend
packages/
  shared/                 TypeScript shared contracts
data/
  jobs/                   Demo job descriptions
  resumes/                Demo markdown resumes
  ontology/               Skill/domain/technology ontology seeds
  samples/                Placeholder for demo samples
  seeds/                  Placeholder for seed scripts
  structured/             Placeholder for structured inputs
docs/                     Project documentation
infra/
  docker/                 Dockerfiles
requirements/             Dependency groups
```

## Implemented Modules

### Module 1: Role DNA Generator

Purpose: Convert job descriptions into structured Role DNA profiles.

Key files:

```text
apps/api/app/domain/role_dna.py
apps/api/app/modules/role_dna/service.py
apps/api/app/modules/role_dna/normalizer.py
apps/api/app/modules/role_dna/local_provider.py
apps/api/app/pipelines/role_pipeline.py
apps/api/app/repositories/memory/role_dna_repository.py
```

Outputs include:

- Role title
- Domain
- Seniority
- Role archetype
- Fingerprint
- Required skills
- Preferred skills
- Skill importance
- Radar-ready scores
- Work environment attributes
- Reasoning
- Confidence

### Module 2: Candidate Digital Twin Builder

Purpose: Convert resume text into normalized Candidate Digital Twins.

Key files:

```text
apps/api/app/domain/candidate_twin.py
apps/api/app/modules/candidates/service.py
apps/api/app/modules/candidates/local_parser_provider.py
apps/api/app/modules/candidates/normalizer.py
apps/api/app/pipelines/candidate_pipeline.py
apps/api/app/repositories/memory/in_memory_candidate_repository.py
```

Outputs include:

- Basic contact info
- Skills and technologies
- Projects and experiences
- Domains
- Deterministic timeline
- Technical depth
- Learning velocity
- Leadership
- Ownership
- Communication
- Project complexity
- Collaboration
- Consistency
- Growth stage
- Reasoning
- Confidence

### Module 3: Talent Knowledge Graph + Embedding Foundation

Purpose: Build semantic foundations without scoring or ranking.

Key files:

```text
apps/api/app/domain/knowledge_graph.py
apps/api/app/domain/vector.py
apps/api/app/modules/graph_builder/service.py
apps/api/app/modules/graph_builder/ontology.py
apps/api/app/modules/embeddings/service.py
apps/api/app/modules/embeddings/summary_service.py
apps/api/app/modules/embeddings/local_provider.py
apps/api/app/pipelines/graph_pipeline.py
apps/api/app/pipelines/embedding_pipeline.py
```

Graph entities:

- Candidate
- Role
- Skill
- Technology
- Project
- Company
- Domain

Relationships:

- HAS_SKILL
- RELATED_TO
- USES
- BELONGS_TO
- REQUIRES
- WORKED_AT
- HAS_DOMAIN

Embeddings are deterministic local vectors. No similarity scoring is implemented.

### Module 4: Candidate Evaluation & Match Engine

Purpose: Evaluate candidate-role fit using existing Role DNA and Candidate Digital Twin records.

Key files:

```text
apps/api/app/domain/evaluation.py
apps/api/app/modules/evaluators/technical.py
apps/api/app/modules/evaluators/growth.py
apps/api/app/modules/evaluators/domain.py
apps/api/app/modules/evaluators/culture.py
apps/api/app/modules/evaluators/service.py
apps/api/app/pipelines/evaluation_pipeline.py
apps/api/app/repositories/memory/in_memory_evaluation_repository.py
```

Evaluator weights for `overall_match`:

- Technical: 40%
- Growth: 25%
- Domain: 20%
- Culture: 15%

### Module 5: Ranking Engine + Hiring Personas

Purpose: Rank candidates using existing `EvaluationBundle` records under a selected hiring persona.

Key files:

```text
apps/api/app/domain/ranking.py
apps/api/app/modules/recruiter_brain/persona_engine.py
apps/api/app/modules/ranking/service.py
apps/api/app/pipelines/ranking_pipeline.py
apps/api/app/repositories/memory/in_memory_ranking_repository.py
```

Personas:

- Startup Founder
- Enterprise Recruiter
- Research Team

Ranking output:

- rank
- candidate_id
- role_id
- persona
- score
- confidence
- evaluation_id

No recommendation labels, explanations, or counterfactuals are implemented.

## API Surface

All API routes are under:

```text
/api/v1
```

Implemented:

```text
GET  /health
POST /api/v1/upload-job
POST /api/v1/generate-role-dna
GET  /api/v1/role-dna
GET  /api/v1/role-dna/{role_id}

POST /api/v1/upload-candidates
POST /api/v1/build-digital-twins
GET  /api/v1/candidates
GET  /api/v1/candidate/{candidate_id}

POST /api/v1/build-graph
GET  /api/v1/graph/{graph_id}

POST /api/v1/generate-embeddings
GET  /api/v1/embeddings/{collection_id}

POST /api/v1/evaluate
GET  /api/v1/evaluations/{evaluation_id}

POST /api/v1/rank
GET  /api/v1/rankings/{role_id}
```

Legacy/future endpoints intentionally returning `501`:

```text
POST /api/v1/rank-candidates
POST /api/v1/generate-explanations
GET  /api/v1/rankings
```

## Data Flow

Happy path demo flow:

```text
1. POST /generate-role-dna with job_description
   -> RolePipeline
   -> RoleDNAService
   -> LocalRoleDNALLMProvider
   -> InMemoryRoleDNARepository
   -> RoleDNAProfile

2. POST /build-digital-twins with resume_text
   -> CandidatePipeline
   -> CandidateDigitalTwinService
   -> LocalResumeParserProvider
   -> InMemoryCandidateRepository
   -> CandidateDigitalTwin

3. POST /build-graph with role_id and candidate_id
   -> GraphPipeline
   -> GraphBuilderService
   -> InMemoryGraphRepository
   -> KnowledgeGraph

4. POST /generate-embeddings with role_id and candidate_id
   -> EmbeddingPipeline
   -> EmbeddingFoundationService
   -> SummaryService
   -> LocalEmbeddingProvider
   -> InMemoryVectorRepository
   -> EmbeddingCollection

5. POST /evaluate with role_id and candidate_id
   -> EvaluationPipeline
   -> EvaluationService
   -> four deterministic evaluator modules
   -> InMemoryEvaluationRepository
   -> EvaluationBundle

6. POST /rank with role_id and persona
   -> RankingPipeline
   -> RankingService
   -> PersonaEngine
   -> InMemoryRankingRepository
   -> ordered RankingResult list
```

## System Boundaries

Implemented:

- Deterministic local providers only.
- In-memory persistence only for working behavior.
- PostgreSQL/Neo4j/Chroma repository skeletons only.
- One-page frontend demo covering Modules 1 through 5.

Not implemented:

- Production database schema.
- Migrations.
- Real OpenAI calls.
- Real sentence-transformer embeddings.
- Neo4j writes/queries.
- Chroma writes/queries.
- Candidate explanations.
- Counterfactuals.
- XLSX export.
- Recruiter chat.
- Autonomous agents.
- Authentication.

## Environment Setup

### Backend

Recommended from repository root:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements/dev.txt
python -m pip install -e apps/api
```

Alternative using `pyproject.toml`:

```powershell
python -m pip install -e "apps/api[dev]"
```

Optional AI dependencies:

```powershell
python -m pip install -r requirements/ai.txt
```

Postgres driver extra:

```powershell
python -m pip install -e "apps/api[postgres]"
```

### Frontend

PowerShell may block `npm.ps1`; use `npm.cmd` on Windows if needed:

```powershell
npm.cmd install
npm.cmd --workspace apps/web run dev
```

## Build and Run

### Backend API

From repository root:

```powershell
uvicorn app.main:app --app-dir apps/api --host 0.0.0.0 --port 8000 --reload
```

API docs:

```text
http://localhost:8000/docs
```

### Frontend

```powershell
npm.cmd --workspace apps/web run dev
```

Frontend URL:

```text
http://localhost:3000
```

### Docker Compose

```powershell
docker compose up --build
```

Docker setup exists but has not been the main verification path. The Python test suite has been the primary verification.

## Verification Status

Last successful backend verification:

```text
45 passed, 1 warning
```

Command used:

```powershell
C:\Users\sanya\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m pytest apps/api/tests
```

The warning is an upstream FastAPI/Starlette `TestClient` deprecation warning.

# START HERE FOR NEXT AI SESSION

1. Open `docs/SESSION_STATE.md` first.
2. Confirm the latest test status by running:

   ```powershell
   python -m pytest apps/api/tests
   ```

3. If continuing non-feature cleanup, verify frontend dependency install/build next.
4. Read `apps/api/app/api/v1/router.py` to see current endpoint behavior.
5. Read `apps/api/app/api/v1/dependencies.py` to understand current in-memory dependency wiring.
6. Continue only with the next approved module. Do not jump ahead to explanations, exports, real DB integration, or AI calls unless explicitly approved.
