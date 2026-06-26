# TalentGraph AI

Explainable Hiring Intelligence Platform.

TalentGraph AI is a hackathon-oriented hiring intelligence platform that evaluates
candidates with structured role understanding, deterministic candidate profiles,
semantic foundations, evaluator modules, and persona-aware ranking. The current
implementation is a working local demo for Modules 1-5, not just scaffolding.

## Implemented Modules

1. **Role DNA Generator**
   - Accepts job descriptions.
   - Generates structured Role DNA profiles with skills, seniority, archetype,
     work environment signals, reasoning, and confidence.

2. **Candidate Digital Twin Builder**
   - Accepts pasted resume text.
   - Builds normalized candidate profiles with skills, technologies, projects,
     timeline entries, growth signals, reasoning, and confidence.

3. **Talent Knowledge Graph and Embedding Foundation**
   - Builds deterministic graph snapshots from role and candidate entities.
   - Generates deterministic summaries and local embedding vectors for inspection.

4. **Candidate Evaluation and Match Engine**
   - Evaluates candidate-role fit across technical, growth, domain, and culture
     dimensions.
   - Calculates an overall match score using deterministic evaluator weights.

5. **Ranking Engine and Hiring Personas**
   - Ranks existing evaluation records under a selected hiring persona.
   - Supports Startup Founder, Enterprise Recruiter, and Research Team personas.

## Current Architecture

The backend follows this pattern:

```text
API Router -> Pipeline -> Service -> Provider/Repository -> Domain Model
```

Runtime behavior is wired in `apps/api/app/api/v1/dependencies.py`.

The working implementation uses:

- FastAPI, Pydantic v2, and pytest for the backend.
- Next.js 15, React 19, TypeScript, Tailwind CSS, and lucide-react for the frontend.
- In-memory repositories for local demo and tests.
- Deterministic local providers for role parsing, resume parsing, and embeddings.

PostgreSQL, Neo4j, ChromaDB, OpenAI, and sentence-transformer integrations are
present only as dependency/configuration boundaries or skeletons. They are not
active in the current working flow.

## API Endpoints

System:

```text
GET  /health
```

Role DNA:

```text
POST /api/v1/upload-job
POST /api/v1/generate-role-dna
GET  /api/v1/role-dna
GET  /api/v1/role-dna/{role_id}
```

Candidates:

```text
POST /api/v1/upload-candidates
POST /api/v1/build-digital-twins
GET  /api/v1/candidates
GET  /api/v1/candidate/{candidate_id}
```

Graph and embeddings:

```text
POST /api/v1/build-graph
GET  /api/v1/graph/{graph_id}
POST /api/v1/generate-embeddings
GET  /api/v1/embeddings/{collection_id}
```

Evaluation and ranking:

```text
POST /api/v1/evaluate
GET  /api/v1/evaluations/{evaluation_id}
POST /api/v1/rank
GET  /api/v1/rankings/{role_id}
```

Future or legacy endpoints currently return `501 Not Implemented`:

```text
POST /api/v1/rank-candidates
POST /api/v1/generate-explanations
GET  /api/v1/rankings
```

## Persistence

The current working persistence layer is in-memory. Data is available only for
the lifetime of the running API process.

Functional repositories live under:

```text
apps/api/app/repositories/memory
```

Skeleton repositories exist for PostgreSQL, Neo4j, and ChromaDB, but they
intentionally raise `NotImplementedError` until persistence hardening is approved.

## Local Development

Backend setup from the repository root:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements/dev.txt
python -m pip install -e apps/api
```

Run the API:

```powershell
uvicorn app.main:app --app-dir apps/api --host 0.0.0.0 --port 8000 --reload
```

API docs:

```text
http://localhost:8000/docs
```

Frontend setup:

```powershell
npm.cmd install
npm.cmd --workspace apps/web run dev
```

Frontend URL:

```text
http://localhost:3000
```

PowerShell may block `npm.ps1`; use `npm.cmd` on Windows.

## Verification

Backend tests:

```powershell
python -m pytest apps/api/tests
```

Known-good command in the Codex runtime:

```powershell
C:\Users\sanya\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m pytest apps/api/tests
```

Current confirmed backend status:

```text
45 passed, 1 warning
```

The warning is a FastAPI/Starlette `TestClient` deprecation warning.

Frontend build status:

```text
Not yet verified in this environment.
```

The next frontend verification step is:

```powershell
npm.cmd install
npm.cmd --workspace apps/web run build
```

## Repository Layout

```text
apps/
  api/             FastAPI backend
  web/             Next.js frontend demo
packages/
  shared/          Shared TypeScript contracts
docs/              Persistent project memory and handoff notes
data/
  jobs/            Demo job descriptions
  resumes/         Demo markdown resumes
  ontology/        Skill/domain/technology ontology seeds
  structured/      Placeholder for structured artifacts
  samples/         Placeholder for demo samples
  seeds/           Placeholder for seed scripts
infra/
  docker/          API and web Dockerfiles
requirements/      Python dependency groups
```

## Not Implemented Yet

- Production database schema and migrations.
- Real PostgreSQL, Neo4j, or Chroma persistence.
- Real OpenAI calls or sentence-transformer embeddings.
- Explanation generation and counterfactuals.
- XLSX export.
- Recruiter chat or autonomous agents.
- Authentication.
- Verified frontend production build.
