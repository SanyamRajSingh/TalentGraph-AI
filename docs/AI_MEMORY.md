# AI Memory

## Non-Negotiable Development Constraints

1. Implement incrementally by approved module only.
2. Do not implement future modules early.
3. Keep business logic out of routers.
4. Keep orchestration in pipelines.
5. Keep business rules in services/modules.
6. Keep providers responsible for external/local model behavior.
7. Keep repositories responsible for persistence only.
8. Prefer deterministic logic over LLM calls for hackathon reliability unless the user explicitly approves AI integration.
9. Add tests for every implemented module.
10. Preserve existing passing tests.

## Important Decisions Made

### Deterministic Local Providers

The project uses deterministic local providers:

- `LocalRoleDNALLMProvider`
- `LocalResumeParserProvider`
- `LocalEmbeddingProvider`

Reason:

- No network calls in tests.
- Reliable hackathon demo.
- Easier to explain and debug.

### In-Memory Repositories Are the Working Implementation

Memory repositories are currently the only functional persistence layer.

Implemented memory repositories:

```text
InMemoryRoleDNARepository
InMemoryCandidateRepository
InMemoryGraphRepository
InMemoryVectorRepository
InMemoryEvaluationRepository
InMemoryRankingRepository
InMemoryExplanationRepository
```

### External Persistence Is Skeleton Only

These skeletons intentionally raise `NotImplementedError`:

```text
PostgresRoleDNARepository
PostgresCandidateRepository
PostgresEvaluationRepository
PostgresRankingRepository
Neo4jGraphRepository
ChromaVectorRepository
```

Do not claim they work.

### Single-Page Frontend Demo

The frontend is currently one page:

```text
apps/web/app/page.tsx
```

It includes panels for:

- Role DNA
- Candidate Digital Twin
- Evaluation
- Ranking
- Explanation
- Knowledge Graph
- Embeddings

This is intentional for a hackathon demo. A routed UI can be added later.

## Naming Conventions

### IDs

Generated IDs use prefixes:

```text
job_
role_
resume_
candidate_
evaluation_
graph:
embeddings:
summary:
embedding:
```

### Domain Model Names

Use canonical domain names:

```text
RoleDNAProfile
RoleJob
CandidateDigitalTwin
CandidateResume
CandidateTimelineEntry
KnowledgeGraph
GraphNode
GraphRelationship
SummaryDocument
EmbeddingRecord
EmbeddingCollection
EvaluationBundle
EvaluatorResult
RankingResult
ExplanationProfile
```

### Module Names

Use existing module folders:

```text
modules/role_dna
modules/candidates
modules/graph_builder
modules/embeddings
modules/evaluators
modules/ranking
modules/recruiter_brain
modules/scoring
modules/explanations
modules/exports
```

Do not create competing names like `matching_engine` unless explicitly approved.

## Coding Standards

- Python 3.12.
- Pydantic v2 models.
- Type hints everywhere.
- Deterministic normalization to integer scores in `[0, 100]`.
- Use `NotImplementedError` only for approved skeletons.
- Tests should not call network.
- Tests should use memory repositories or mock services/providers.
- Keep files focused and small.
- Do not add comments unless they clarify non-obvious logic.

## Established Patterns

### Adding a Module

Follow this sequence:

```text
1. Domain model
2. Repository interface
3. Memory repository
4. Skeleton external repository if requested
5. Service/module logic
6. Pipeline
7. Request/response contracts
8. Router endpoints
9. Dependency injection
10. Tests
11. Frontend panel
12. Shared TypeScript type updates
```

### API Error Handling

Pattern in `router.py`:

```python
try:
    result = pipeline.run(...)
except ValueError as exc:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
```

### Dependency Injection

All runtime wiring is in:

```text
apps/api/app/api/v1/dependencies.py
```

Use `@lru_cache` for singleton in-memory repositories and services where appropriate.

### Test Organization

Tests are grouped by module:

```text
apps/api/tests/role_dna
apps/api/tests/candidate
apps/api/tests/graph
apps/api/tests/evaluation
apps/api/tests/ranking
```

## Things That Should NOT Be Changed Without Approval

1. Do not replace deterministic local providers with real OpenAI calls.
2. Do not switch memory repositories to database repositories globally.
3. Do not remove existing 501 endpoints without understanding their future-module role.
4. Do not merge evaluator and ranking logic.
5. Do not put business logic in `router.py`.
6. Do not add recommendations to ranking results.
7. Do not add explanation fields to ranking results.
8. Keep counterfactuals inside the explanations module, not evaluation or ranking.
9. Do not create autonomous agents.
10. Do not add unrelated UI landing/marketing pages.

## Things Intentionally Postponed

- Real PDF upload/parsing.
- Real OpenAI provider.
- Real sentence-transformer embeddings.
- Vector similarity.
- Neo4j persistence.
- Chroma persistence.
- PostgreSQL persistence.
- Database migrations.
- Recommendation labels such as Hire/No Hire.
- Authentication.
- Multi-page frontend routing.
- CI/CD.
- Production deployment verification.

## Assumptions

1. Hackathon demo quality is more important than enterprise complexity.
2. Deterministic local behavior is preferred until external integrations are explicitly requested.
3. In-memory repositories are acceptable for the current demo.
4. The next AI engineer will continue module-by-module.
5. The user values clean architecture and explicit approval gates.

## Current Test Baseline

Backend test suite:

```text
53 passed, 1 warning
```

Use this as the regression baseline.

## Current Warning

FastAPI/Starlette TestClient emits a deprecation warning related to `httpx`.

Do not spend time on it unless the user asks for dependency cleanup.

# START HERE FOR NEXT AI SESSION

1. Preserve the module approval workflow.
2. Read `docs/NEXT_TASKS.md` before implementing anything.
3. Run tests before changes:

   ```powershell
   python -m pytest apps/api/tests
   ```

4. Make only the approved change.
5. Run tests after changes.
6. Update this file if a major decision changes.
