# Local Setup Report

## 1. Required Environment Variables

Backend (`.env.local` or `.env.development`):
```env
APP_ENV=development
APP_NAME=TalentGraph AI
API_HOST=0.0.0.0
API_PORT=8000
BACKEND_CORS_ORIGINS=http://localhost:3000
# Database and External API dependencies are optional for local v1.0
ENABLE_ROLE_DNA_GENERATOR=false
ENABLE_CANDIDATE_TWIN_BUILDER=false
ENABLE_RANKING_PIPELINE=false
ENABLE_GRAPH_INTEGRATION=false
ENABLE_EMBEDDING_ENGINE=false
```

Frontend (`apps/web/.env.local`):
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## 2. Required Dependencies

**Backend:**
Python >= 3.12
- `fastapi`, `uvicorn[standard]`, `pydantic`, `pydantic-settings`, `python-multipart`, `sqlalchemy`, `openpyxl`, `python-json-logger`, `slowapi`
- Dev dependencies: `pytest`, `pytest-asyncio`, `httpx`, `ruff`

**Frontend:**
Node.js (matching `@types/node` ^22.0.0)
- `next`, `react`, `react-dom`, `framer-motion`, `lucide-react`, `d3`, `dagre`, `@tanstack/react-virtual`
- Dev dependencies: `typescript`, `tailwindcss`, `eslint`, `postcss`

## 3. Startup Order

1. Backend (FastAPI on port 8000)
2. Frontend (Next.js on port 3000)

## 4. Ports

- Backend API: `8000`
- Frontend UI: `3000`

## 5. Workspace Configuration

Monorepo using npm workspaces:
- `apps/api` (FastAPI Python backend)
- `apps/web` (Next.js frontend)
- `packages/shared` (Shared dependencies/types)

Scripts available at root `package.json`:
- `npm run dev:web` -> `npm --workspace apps/web run dev`
- `npm run build:web` -> `npm --workspace apps/web run build`
