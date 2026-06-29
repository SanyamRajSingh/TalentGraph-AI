# TalentGraph AI v3.0 — System Audit

Generated: 2026-06-29

## 1. Architecture Map

```
┌─────────────────────────────────────────────────────────────────────┐
│  Browser (localhost:3000)                                           │
│  Next.js 15 App Router — apps/web/app/page.tsx (single page SPA)   │
└───────────────────────────────┬─────────────────────────────────────┘
                                │ HTTP REST (CORS)
┌───────────────────────────────▼─────────────────────────────────────┐
│  FastAPI Backend (localhost:8000)                                   │
│  apps/api/app/main.py                                               │
│  ├── Middleware: CORS, RateLimit (slowapi), SecurityHeaders         │
│  ├── Lifespan: PostgreSQL setup → Startup Seeder                   │
│  └── Router: /api/v1/* (22 endpoints)                               │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
   Pipelines               Services              Repositories
   (orchestration)         (business logic)      (data storage)
        │                       │                       │
   role_pipeline           RoleDNAService         InMemory (default)
   candidate_pipeline      EvaluationService      PostgreSQL (if set)
   evaluation_pipeline     ExplanationService
   ranking_pipeline        RankingService
   explanation_pipeline    GraphBuilderService
   embedding_pipeline      EmbeddingService
   graph_pipeline          CopilotService
   copilot_pipeline        SearchService
   batch_pipeline          ComparisonService
                           AnalyticsService
                           RecommendationService
```

## 2. Module Dependency Graph

```
app/main.py
  └── app/api/v1/router.py
        └── app/api/v1/dependencies.py
              ├── app/pipelines/*
              │     ├── app/modules/*          (business logic)
              │     ├── app/repositories/*     (data layer)
              │     └── app/domain/*           (domain models)
              └── app/core/settings.py
```

## 3. API Dependency Graph (all 22 endpoints)

| Method | Path | Pipeline/Service |
|--------|------|-----------------|
| GET  | /health | — |
| POST | /api/v1/upload-job | RolePipeline |
| POST | /api/v1/generate-role-dna | RolePipeline |
| GET  | /api/v1/role-dna | RoleDNARepository |
| GET  | /api/v1/role-dna/{id} | RoleDNARepository |
| POST | /api/v1/upload-candidates | CandidatePipeline |
| POST | /api/v1/upload-file | CandidatePipeline |
| POST | /api/v1/build-digital-twins | CandidatePipeline |
| GET  | /api/v1/candidates | CandidateRepository (paginated) |
| GET  | /api/v1/candidate/{id} | CandidateRepository |
| POST | /api/v1/batch/upload-zip | BatchPipeline |
| GET  | /api/v1/batch/status/{id} | BatchPipeline |
| POST | /api/v1/evaluate | EvaluationPipeline |
| POST | /api/v1/rank | RankingPipeline |
| GET  | /api/v1/rankings/{role_id} | RankingRepository |
| POST | /api/v1/generate-explanations | ExplanationPipeline |
| GET  | /api/v1/explanations/{candidate_id} | ExplanationRepository |
| POST | /api/v1/build-graph | GraphPipeline |
| GET  | /api/v1/graph/{id} | GraphRepository |
| POST | /api/v1/generate-embeddings | EmbeddingPipeline |
| GET  | /api/v1/embeddings/{id} | VectorRepository |
| POST | /api/v1/recommend | EvaluationPipeline + RecommendationService |
| POST | /api/v1/export-rankings | RankingExportService |
| GET  | /api/v1/search/candidates | SearchService |
| GET  | /api/v1/search/roles | SearchService |
| POST | /api/v1/copilot/draft-email | CopilotPipeline |
| POST | /api/v1/copilot/chat | CopilotChatService |
| POST | /api/v1/compare | ComparisonService |
| GET  | /api/v1/analytics/overview | AnalyticsService |

## 4. Frontend Data Flow

```
page.tsx (Client Component)
  │
  ├── State (useState hooks)
  │    ├── roleDNA, candidateTwin, candidateTwins
  │    ├── evaluation, rankings, explanation
  │    ├── graph, embeddingCollection
  │    ├── copilotResponse, comparison, analytics
  │    └── loading/error states for each flow
  │
  ├── Event Handlers → fetch() → Backend API
  │    ├── handleRoleSubmit        → POST /generate-role-dna
  │    ├── handleCandidateSubmit   → POST /build-digital-twins
  │    ├── handleEvaluateSubmit    → POST /evaluate
  │    ├── handleRankSubmit        → POST /rank
  │    ├── handleExplanationSubmit → POST /generate-explanations
  │    ├── handleExportRankings    → POST /export-rankings
  │    ├── handleGraphSubmit       → POST /build-graph
  │    ├── handleEmbedSubmit       → POST /generate-embeddings
  │    ├── handleCopilotDraft      → POST /copilot/draft-email
  │    ├── handleCompare           → POST /compare
  │    └── handleLoadAnalytics     → GET /analytics/overview
  │
  └── Sub-components
       ├── CandidateLibrary   (apps/web/components/CandidateLibrary.tsx)
       └── CopilotChatPanel   (apps/web/components/CopilotChatPanel.tsx)
```

## 5. Backend Startup Flow

```
uvicorn app.main:app
  │
  ├─ 1. setup_logging()
  ├─ 2. Limiter init (slowapi)
  ├─ 3. get_settings()  [reads .env]
  ├─ 4. FastAPI app created
  ├─ 5. Lifespan startup:
  │     ├─ [if postgres] create_tables()
  │     └─ seed(
  │           candidate_repository,    ← lru_cache singleton
  │           role_repository,          ← lru_cache singleton
  │           evaluation_pipeline,
  │           ranking_pipeline,
  │           explanation_pipeline,
  │           embedding_pipeline,
  │           graph_pipeline
  │        )
  │        ├─ skip if already seeded
  │        ├─ build 10 roles → save
  │        ├─ build 50 candidates → save
  │        ├─ 500 evaluations (10×50)
  │        ├─ 20 ranking runs (10×2 personas)
  │        ├─ 50 explanations (50 candidates × 1 role)
  │        ├─ 10 embeddings (first 10 candidates)
  │        └─ 5 graphs (first 5 candidates)
  └─ 6. API ready
```

## 6. Repository Usage Map

| Repository | Interface | Memory impl | Postgres impl |
|-----------|-----------|-------------|---------------|
| RoleDNARepository | role_dna_repository.py | InMemoryRoleDNARepository | PostgresRoleDNARepository |
| CandidateRepository | candidate_repository.py | InMemoryCandidateRepository | PostgresCandidateRepository |
| EvaluationRepository | evaluation_repository.py | InMemoryEvaluationRepository | PostgresEvaluationRepository |
| RankingRepository | ranking_repository.py | InMemoryRankingRepository | PostgresRankingRepository |
| ExplanationRepository | explanation_repository.py | InMemoryExplanationRepository | PostgresExplanationRepository |
| GraphRepository | graph_repository.py | InMemoryGraphRepository | PostgresGraphRepository |
| VectorRepository | vector_repository.py | InMemoryVectorRepository | — (Chroma planned) |
| RecommendationRepository | recommendation_repository.py | InMemoryRecommendationRepository | PostgresRecommendationRepository |
| CopilotConversationRepository | copilot_repository.py | InMemoryCopilotRepository | PostgresCopilotRepository |

## 7. Component Tree (Frontend)

```
page.tsx (root client component, 1968 lines)
  ├── <header> — branding, dark mode toggle, step progress
  ├── <section id="role-dna"> — job description form
  ├── <section id="digital-twins"> — resume upload form
  ├── <section id="evaluate"> — evaluation trigger
  ├── <section id="rank"> — persona selector + ranking table
  ├── <section id="explanations"> — explanation card
  ├── <section id="graph"> — D3/Dagre graph visualization
  ├── <section id="embeddings"> — embedding scatterplot
  ├── <section id="compare"> — candidate comparison table
  ├── <section id="analytics"> — analytics dashboard cards
  ├── <section id="export"> — XLSX export button
  └── <section id="copilot"> — tabbed copilot panel
        ├── CopilotChatPanel (components/CopilotChatPanel.tsx)
        └── CandidateLibrary (components/CandidateLibrary.tsx)
```

## 8. Package Dependency Graph

### Backend (Python)
```
fastapi → starlette, pydantic
pydantic → pydantic-core (Rust extension, compiled from source)
pydantic-settings → python-dotenv
sqlalchemy → greenlet (compiled from source)
uvicorn → h11, click
slowapi → limits
openpyxl → et-xmlfile (XLSX export)
pypdf → (PDF parsing)
python-docx → lxml (compiled, DOCX parsing)
python-multipart → (file uploads)
python-json-logger → (JSON logging)
```

### Frontend (Node.js)
```
next → react, react-dom
d3 → (graph visualization)
dagre → (graph layout)
framer-motion → (animations)
lucide-react → (icons)
@tanstack/react-virtual → (virtual scrolling)
@talentgraph/shared → (workspace package)
```
