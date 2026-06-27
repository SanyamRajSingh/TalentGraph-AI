# Current Status

## Snapshot

Project: TalentGraph AI

Current branch:

```text
master
```

Git status after baseline commit:

```text
Clean after initial baseline commit, pending any later work.
```

Baseline commit message:

```text
Implement TalentGraph AI modules 1-5
```

The commit includes the README refresh and the Modules 1-5 project baseline.

## Last Completed Task

Module 7: Dashboard Polish + XLSX Export + Submission Assets.

Completed:

- Polished dashboard into a five-step workflow.
- Added progress indicators, role radar, candidate metric cards, leaderboard, and counterfactual cards.
- Added `POST /api/v1/export-rankings`.
- Added XLSX generation using existing ranking, candidate, and explanation data.
- Added `data/demo/` release dataset with one job and four resumes.
- Added release docs: `RELEASE_NOTES.md`, `DEMO_SCRIPT.md`, and `SUBMISSION_CHECKLIST.md`.
- Verified backend tests, frontend build, demo dataset flow, and XLSX export.

Previous completed product task:

Module 6: Explainability + Counterfactual Engine.

The latest implemented feature ranks candidates from existing `EvaluationBundle` records using persona-specific deterministic weights.

## Features Completed

### Module 1: Role DNA Generator

Completed capabilities:

- Accept job descriptions.
- Generate structured `RoleDNAProfile`.
- Extract required and preferred skills.
- Infer role archetype.
- Infer role fingerprint.
- Infer work environment signals.
- Generate deterministic skill importance weights.
- Generate reasoning strings.
- Normalize scores to integers in `[0, 100]`.
- Persist jobs and Role DNA in memory.
- Expose REST endpoints.
- Unit tests.
- Frontend Role DNA panel.

Important files:

```text
apps/api/app/domain/role_dna.py
apps/api/app/modules/role_dna/service.py
apps/api/app/modules/role_dna/normalizer.py
apps/api/app/modules/role_dna/local_provider.py
apps/api/app/pipelines/role_pipeline.py
apps/api/app/repositories/memory/role_dna_repository.py
apps/api/tests/role_dna/
```

### Module 2: Candidate Digital Twin Builder

Completed capabilities:

- Accept pasted resume text.
- Parse deterministic structured fields.
- Build `CandidateDigitalTwin`.
- Extract skills, technologies, projects, experiences, domains, certifications, achievements.
- Generate deterministic timeline entries.
- Infer growth stage.
- Normalize candidate metrics to `[0, 100]`.
- Persist resumes and twins in memory.
- Expose REST endpoints.
- Unit tests.
- Frontend Candidate Digital Twin panel.

Important files:

```text
apps/api/app/domain/candidate_twin.py
apps/api/app/modules/candidates/service.py
apps/api/app/modules/candidates/local_parser_provider.py
apps/api/app/modules/candidates/normalizer.py
apps/api/app/pipelines/candidate_pipeline.py
apps/api/app/repositories/memory/in_memory_candidate_repository.py
apps/api/tests/candidate/
```

### Module 3: Talent Knowledge Graph + Embedding Foundation

Completed capabilities:

- Define graph node and relationship domain models.
- Load ontology seed files from `data/ontology`.
- Build deterministic graph snapshots from Role DNA and Candidate Twin.
- Generate deterministic role and candidate summaries.
- Generate deterministic local embedding vectors.
- Store graph snapshots and embedding collections in memory.
- Add Neo4j and Chroma repository skeletons.
- Expose REST endpoints.
- Unit tests.
- Frontend graph and embedding inspection panels.

Important files:

```text
apps/api/app/domain/knowledge_graph.py
apps/api/app/domain/vector.py
apps/api/app/modules/graph_builder/
apps/api/app/modules/embeddings/
apps/api/app/pipelines/graph_pipeline.py
apps/api/app/pipelines/embedding_pipeline.py
apps/api/app/repositories/memory/in_memory_graph_repository.py
apps/api/app/repositories/memory/in_memory_vector_repository.py
apps/api/tests/graph/
data/ontology/
```

### Module 4: Candidate Evaluation & Match Engine

Completed capabilities:

- Implement deterministic evaluator modules:
  - TechnicalEvaluator
  - GrowthEvaluator
  - DomainEvaluator
  - CultureEvaluator
- Produce `EvaluationBundle`.
- Calculate `overall_match` using:
  - Technical 40%
  - Growth 25%
  - Domain 20%
  - Culture 15%
- Calculate `overall_confidence` as average evaluator confidence.
- Persist evaluations in memory.
- Add Postgres evaluation skeleton.
- Expose REST endpoints.
- Unit tests.
- Frontend Evaluation panel.

Important files:

```text
apps/api/app/domain/evaluation.py
apps/api/app/modules/evaluators/
apps/api/app/pipelines/evaluation_pipeline.py
apps/api/app/repositories/memory/in_memory_evaluation_repository.py
apps/api/tests/evaluation/
```

### Module 5: Ranking Engine + Hiring Personas

Completed capabilities:

- Implement personas:
  - Startup Founder
  - Enterprise Recruiter
  - Research Team
- Apply persona weights to existing evaluation bundles.
- Rank candidates by score descending.
- Tie handling:
  1. score descending
  2. confidence descending
  3. candidate_id ascending
- Persist rankings in memory.
- Add Postgres ranking skeleton.
- Expose REST endpoints.
- Unit tests.
- Frontend Ranking panel with persona selector.

Important files:

```text
apps/api/app/domain/ranking.py
apps/api/app/modules/recruiter_brain/persona_engine.py
apps/api/app/modules/ranking/service.py
apps/api/app/pipelines/ranking_pipeline.py
apps/api/app/repositories/memory/in_memory_ranking_repository.py
apps/api/tests/ranking/
```

## Features Partially Completed

### Persistence

Working:

- In-memory repositories for Role DNA, candidates, graph, vector, evaluation, and ranking.

Skeleton only:

- PostgreSQL repositories:
  - `apps/api/app/repositories/postgres/role_dna_repository.py`
  - `apps/api/app/repositories/postgres/postgres_candidate_repository.py`
  - `apps/api/app/repositories/postgres/postgres_evaluation_repository.py`
  - `apps/api/app/repositories/postgres/postgres_ranking_repository.py`
- Neo4j:
  - `apps/api/app/repositories/neo4j/neo4j_graph_repository.py`
- Chroma:
  - `apps/api/app/repositories/chroma/chroma_vector_repository.py`

No database migrations or SQLAlchemy table mappings exist yet.

### Frontend

Working:

- One-page demo in `apps/web/app/page.tsx`.
- Panels for:
  - Role DNA
  - Candidate Digital Twin
  - Evaluation
  - Ranking
  - Explanation
  - XLSX Export
  - Knowledge Graph
  - Embedding Inspection

Verified:

- `npm.cmd install`
- `npm.cmd --workspace apps/web run build`

### Docker

Dockerfiles and `docker-compose.yml` exist. `docker compose config` passes. Full startup is blocked locally because Docker Desktop is not running.

## Features Not Started

Not implemented:

- Recruiter chat.
- Recommendation engine.
- Final polished multi-page dashboard routing.
- Authentication.
- Real OpenAI integration.
- Real sentence-transformer model usage.
- Real Chroma persistence.
- Real Neo4j persistence.
- Real PostgreSQL schema and migrations.
- Production deployment configuration beyond initial Docker scaffolding.

## APIs Implemented

### System

```text
GET /health
```

### Role DNA

```text
POST /api/v1/upload-job
POST /api/v1/generate-role-dna
GET  /api/v1/role-dna
GET  /api/v1/role-dna/{role_id}
```

### Candidate Digital Twin

```text
POST /api/v1/upload-candidates
POST /api/v1/build-digital-twins
GET  /api/v1/candidates
GET  /api/v1/candidate/{candidate_id}
```

### Graph

```text
POST /api/v1/build-graph
GET  /api/v1/graph/{graph_id}
```

### Embeddings

```text
POST /api/v1/generate-embeddings
GET  /api/v1/embeddings/{collection_id}
```

### Evaluation

```text
POST /api/v1/evaluate
GET  /api/v1/evaluations/{evaluation_id}
```

### Ranking

```text
POST /api/v1/rank
GET  /api/v1/rankings/{role_id}

POST /api/v1/generate-explanations
GET  /api/v1/explanations/{candidate_id}
POST /api/v1/export-rankings
```

### Future/Legacy 501 Endpoints

```text
POST /api/v1/rank-candidates
GET  /api/v1/rankings
```

## Database Schema Status

No concrete database schema exists.

Current state:

- `DATABASE_URL` is configured in `.env.example`.
- SQLAlchemy is a dependency.
- Postgres repository skeletons accept `Session`.
- No SQLAlchemy models.
- No Alembic.
- No migrations.
- No tables.

Assumption: database hardening should be a separate approved module.

## Integrations Completed

Completed:

- Local deterministic Role DNA provider.
- Local deterministic resume parser.
- Local deterministic embedding provider.
- Ontology JSON loading.
- FastAPI TestClient test coverage.

Skeleton only:

- OpenAI through `LLMProvider`.
- Sentence-transformer/embedding models through `EmbeddingProvider`.
- PostgreSQL repositories.
- Neo4j repository.
- Chroma repository.

## Latest Test Status

Last backend test run:

```text
53 passed, 1 warning
```

Command:

```powershell
C:\Users\sanya\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m pytest apps/api/tests
```

Warning:

```text
StarletteDeprecationWarning from FastAPI TestClient/httpx compatibility.
```

## Known Issues and Technical Debt

1. NPM audit reports 2 moderate dependency vulnerabilities after install.
   - No dependency upgrades were applied because Module 6 scope did not include dependency remediation.

2. In-memory storage resets on process restart.
   - Demo flow works only inside one API process lifetime.

3. Repository skeletons exist but are not functional.
   - Postgres, Neo4j, and Chroma skeletons intentionally raise `NotImplementedError`.

4. API route file is growing large.
   - `apps/api/app/api/v1/router.py` currently contains all endpoints.
   - A future cleanup could split routers by module, but do not do that without approval because current pattern is stable and tested.

5. No frontend automated tests.

6. No real PDF parsing.
   - Resume input is plain text/markdown.

7. No real similarity scoring.
   - Embeddings are generated and stored for inspection only.

8. No recommendation labels.
    - Module 6 intentionally avoids Hire/No Hire style recommendations.

# START HERE FOR NEXT AI SESSION

1. Run backend tests:

   ```powershell
   python -m pytest apps/api/tests
   ```

2. Inspect `apps/api/app/api/v1/router.py` for all live endpoints.
3. Inspect `apps/api/app/api/v1/dependencies.py` to understand in-memory repository wiring.
4. Ask which next module or cleanup task is approved before continuing product scope.
5. Before any major refactor, remember all current tests pass and the module-by-module architecture is intentional.
