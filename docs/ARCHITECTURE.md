# TalentGraph AI Architecture

## Architecture Summary

TalentGraph AI is a modular monorepo with a FastAPI backend and a Next.js frontend. The backend uses explicit domain models, service modules, repository interfaces, provider abstractions, and pipeline orchestrators.

The core architecture rule is:

```text
API route -> Pipeline -> Service -> Provider/Repository -> Domain model
```

Each layer has a strict responsibility:

- API routes validate HTTP input/output and delegate.
- Pipelines orchestrate workflow steps.
- Services contain business logic.
- Providers handle external or local model/parser behavior.
- Repositories persist and retrieve data.
- Domain models define canonical application state.

## Component Architecture

```text
apps/web
  Next.js UI
  Calls FastAPI endpoints

apps/api/app/api/v1
  FastAPI router
  Dependency injection factories

apps/api/app/contracts
  Request/response DTOs

apps/api/app/domain
  Canonical Pydantic models

apps/api/app/pipelines
  Orchestration classes

apps/api/app/modules
  Business logic by module

apps/api/app/providers
  Abstract provider interfaces

apps/api/app/repositories
  Abstract repositories plus memory/skeleton implementations
```

## Service Responsibilities

### RoleDNAService

File:

```text
apps/api/app/modules/role_dna/service.py
```

Responsibilities:

- Request structured Role DNA JSON from `LLMProvider`.
- Parse provider JSON.
- Delegate deterministic normalization to `normalizer.py`.
- Return `RoleDNAProfile`.

Does not:

- Persist directly.
- Access FastAPI request objects.
- Call databases.

### CandidateDigitalTwinService

File:

```text
apps/api/app/modules/candidates/service.py
```

Responsibilities:

- Parse resume text through `ParserProvider`.
- Normalize extracted lists.
- Generate deterministic candidate timeline.
- Derive metrics.
- Infer growth stage.
- Build `CandidateDigitalTwin`.

Does not:

- Persist directly.
- Rank candidates.
- Generate embeddings.

### GraphBuilderService

File:

```text
apps/api/app/modules/graph_builder/service.py
```

Responsibilities:

- Build deterministic `KnowledgeGraph` from `RoleDNAProfile` and/or `CandidateDigitalTwin`.
- Create graph nodes for roles, candidates, skills, technologies, projects, companies, and domains.
- Create supported relationship types.
- Add ontology-adjacent `RELATED_TO` edges when both nodes exist.

Does not:

- Persist directly.
- Rank or evaluate.
- Perform graph reasoning.

### SummaryService

File:

```text
apps/api/app/modules/embeddings/summary_service.py
```

Responsibilities:

- Generate deterministic role summaries.
- Generate deterministic candidate summaries.

Does not:

- Call LLMs.
- Generate embeddings.
- Score similarity.

### EmbeddingFoundationService

File:

```text
apps/api/app/modules/embeddings/service.py
```

Responsibilities:

- Call `SummaryService`.
- Call `EmbeddingProvider`.
- Create `EmbeddingCollection`.
- Generate summary, skill, and project vectors.

Does not:

- Calculate similarity.
- Rank candidates.
- Use real AI model by default.

### EvaluationService

File:

```text
apps/api/app/modules/evaluators/service.py
```

Responsibilities:

- Run four deterministic evaluators.
- Calculate weighted `overall_match`.
- Calculate average `overall_confidence`.
- Return `EvaluationBundle`.

Evaluator weights:

```text
technical 40%
growth    25%
domain    20%
culture   15%
```

Does not:

- Rank candidates.
- Generate explanations.
- Persist directly.

### RankingService

File:

```text
apps/api/app/modules/ranking/service.py
```

Responsibilities:

- Load existing evaluations through `EvaluationRepository`.
- Use `PersonaEngine` to apply persona weights.
- Build `RankingResult` objects.
- Sort rankings.
- Persist rankings.

Tie handling:

```text
1. score descending
2. confidence descending
3. candidate_id ascending
```

Does not:

- Evaluate candidates.
- Generate recommendations.
- Persist explanations.

### ExplanationService

File:

```text
apps/api/app/modules/explanations/service.py
```

Responsibilities:

- Generate deterministic strengths, risks, and reasoning from role, candidate, evaluation, and ranking data.
- Call `CounterfactualService`.
- Persist `ExplanationProfile`.

Does not:

- Rank candidates.
- Evaluate candidates.
- Call LLMs.
- Generate Hire/No Hire recommendations.

### CounterfactualService

File:

```text
apps/api/app/modules/explanations/counterfactual_service.py
```

Responsibilities:

- Generate 1-3 actionable suggestions from evaluator score gaps.

Does not:

- Mutate candidate profiles.
- Re-rank candidates.
- Call LLMs.

## Class Responsibilities

### Domain Classes

`RoleDNAProfile`

- File: `apps/api/app/domain/role_dna.py`
- Represents structured role requirements.
- Key fields: `role_id`, `job_id`, `role_title`, `domain`, `seniority`, `role_archetype`, `fingerprint`, `required_skills`, `preferred_skills`, `skill_importance`, score fields, `reasoning`, `confidence`.

`CandidateDigitalTwin`

- File: `apps/api/app/domain/candidate_twin.py`
- Represents normalized candidate profile.
- Key fields: `candidate_id`, `resume_id`, contact info, `skills`, `technologies`, `projects`, `experiences`, `domains`, `timeline`, derived metric scores, `growth_stage`, `confidence`, `reasoning`.

`KnowledgeGraph`

- File: `apps/api/app/domain/knowledge_graph.py`
- Contains `graph_id`, `nodes`, and `relationships`.

`EmbeddingCollection`

- File: `apps/api/app/domain/vector.py`
- Contains `collection_id`, `summaries`, and `embeddings`.

`EvaluationBundle`

- File: `apps/api/app/domain/evaluation.py`
- Contains evaluator results and aggregate match metrics.

`RankingResult`

- File: `apps/api/app/domain/ranking.py`
- Contains `candidate_id`, `role_id`, `rank`, `persona`, `score`, `confidence`, `evaluation_id`.

### Pipeline Classes

`RolePipeline`

- Uploads jobs.
- Runs Role DNA generation.
- Persists Role DNA.

`CandidatePipeline`

- Uploads resume text.
- Runs Candidate Digital Twin build.
- Persists twin.

`GraphPipeline`

- Loads role/candidate by ID.
- Runs graph builder.
- Persists graph.

`EmbeddingPipeline`

- Loads role/candidate by ID.
- Runs embedding foundation service.
- Persists embedding collection.

`EvaluationPipeline`

- Loads role/candidate by ID.
- Runs evaluation service.
- Persists bundle.

`RankingPipeline`

- Delegates to `RankingService`.
- Returns ordered rankings.

## Sequence Flows

### Role DNA Generation

```text
POST /api/v1/generate-role-dna
-> router.generate_role_dna
-> RolePipeline.run
-> RoleDNAService.generate
-> LocalRoleDNALLMProvider.complete_json
-> normalize_role_dna_payload
-> InMemoryRoleDNARepository.save
-> RoleDNAResponse
```

### Candidate Digital Twin

```text
POST /api/v1/build-digital-twins
-> router.build_digital_twin
-> CandidatePipeline.run
-> CandidateDigitalTwinService.build_from_resume_text
-> LocalResumeParserProvider.parse_resume_text
-> build_timeline/infer_growth_stage
-> InMemoryCandidateRepository.save
-> CandidateTwinResponse
```

### Knowledge Graph

```text
POST /api/v1/build-graph
-> router.build_graph
-> GraphPipeline.run
-> RoleDNARepository.get_by_role_id
-> CandidateRepository.get_by_candidate_id
-> GraphBuilderService.build
-> load_ontology
-> InMemoryGraphRepository.save
-> GraphResponse
```

### Embedding Foundation

```text
POST /api/v1/generate-embeddings
-> router.generate_embeddings
-> EmbeddingPipeline.run
-> role/candidate repositories
-> EmbeddingFoundationService.generate
-> SummaryService.role_summary/candidate_summary
-> LocalEmbeddingProvider.embed/embed_batch
-> InMemoryVectorRepository.save
-> EmbeddingCollectionResponse
```

### Evaluation

```text
POST /api/v1/evaluate
-> router.evaluate_candidate
-> EvaluationPipeline.run
-> role/candidate repositories
-> EvaluationService.evaluate
-> TechnicalEvaluator/GrowthEvaluator/DomainEvaluator/CultureEvaluator
-> InMemoryEvaluationRepository.save
-> EvaluationResponse
```

### Ranking

```text
POST /api/v1/rank
-> router.rank
-> RankingPipeline.run
-> RankingService.rank
-> EvaluationRepository.list_by_role_id
-> PersonaEngine.score
-> InMemoryRankingRepository.save_many
-> RankingResponse
```

## Important Design Decisions

1. Deterministic local providers are used for hackathon reliability.
2. No external network/API calls are needed for implemented modules.
3. AI dependencies are optional and isolated.
4. In-memory repositories are the working implementations.
5. Database-backed repositories are skeletons until persistence is explicitly approved.
6. The frontend is currently a single demo page, not a full routed application.
7. Ranking depends on existing evaluations, not raw candidate/role objects.
8. Embeddings are for inspection only. No similarity calculations exist.
9. Evaluation produces match scores but not recommendations.
10. Ranking produces ordered results but not recommendations.
11. Explanations are generated separately from ranking outputs.

## Dependency Relationships

```text
RolePipeline
  depends on RoleDNAService, RoleDNARepository

CandidatePipeline
  depends on CandidateDigitalTwinService, CandidateRepository

GraphPipeline
  depends on GraphBuilderService, GraphRepository, RoleDNARepository, CandidateRepository

EmbeddingPipeline
  depends on EmbeddingFoundationService, VectorRepository, RoleDNARepository, CandidateRepository

EvaluationPipeline
  depends on EvaluationService, EvaluationRepository, RoleDNARepository, CandidateRepository

RankingPipeline
  depends on RankingService

RankingService
  depends on EvaluationRepository, RankingRepository, PersonaEngine
```

## Future Extension Points

### Persistence

Add concrete implementations for:

- PostgreSQL repositories
- Neo4j graph repository
- Chroma vector repository

Likely new files:

```text
apps/api/app/db/models.py
apps/api/app/db/session.py
migrations/
```

### Explanations

Implemented in Module 6 under:

```text
apps/api/app/modules/explanations/
apps/api/app/pipelines/explanation_pipeline.py
```

### Export

Use:

```text
apps/api/app/modules/exports/
```

Currently empty except `__init__.py`.

### Real AI Integration

Use provider interfaces:

```text
apps/api/app/providers/llm_provider.py
apps/api/app/providers/embedding_provider.py
apps/api/app/providers/parser_provider.py
```

Do not hardcode OpenAI, Chroma, or sentence-transformer calls in services or pipelines.

# START HERE FOR NEXT AI SESSION

1. Read `docs/AI_MEMORY.md` to understand constraints.
2. Read `apps/api/app/api/v1/dependencies.py`; this is where runtime implementations are wired.
3. If adding a new module, follow the established sequence:

   ```text
   domain -> repository interface/implementation -> service -> pipeline -> contracts -> router -> tests -> frontend
   ```

4. Run all backend tests before and after changes.
