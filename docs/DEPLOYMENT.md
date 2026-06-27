# Deployment Guide

This document outlines the production deployment strategy for TalentGraph AI v1.0.

The stack consists of a Next.js frontend (optimized for serverless platforms like Vercel) and a FastAPI backend (containerized, best suited for platforms like Render, Railway, or AWS ECS).

---

## 1. Frontend (Next.js)

**Target Platform:** Vercel

Vercel is the recommended hosting provider for Next.js applications, offering zero-configuration deployments.

### Environment Variables
| Variable | Description | Example |
|---|---|---|
| NEXT_PUBLIC_API_BASE_URL | The URL of your deployed FastAPI backend | https://api.talentgraph.app |

### Deployment Steps
1. Push your repository to GitHub, GitLab, or Bitbucket.
2. Log in to Vercel and create a new project.
3. Import the repository.
4. **Build Settings:**
   - **Framework Preset:** Next.js
   - **Root Directory:** apps/web
   - **Build Command:** npm run build
   - **Install Command:** npm install
5. Configure the Environment Variables (add NEXT_PUBLIC_API_BASE_URL).
6. Click **Deploy**.

---

## 2. Backend (FastAPI)

**Target Platform:** Render, Railway, or any Docker-compatible PaaS.

The backend is fully containerized using infra/docker/api.Dockerfile.

### Environment Variables
| Variable | Description | Example |
|---|---|---|
| APP_ENV | Application environment mode | production |
| APP_NAME | Name of the application | TalentGraph AI |
| BACKEND_CORS_ORIGINS | Comma-separated list of allowed origins | https://talentgraph.app |
| OPENAI_API_KEY | Your OpenAI API key | sk-proj-... |
| DATABASE_URL | PostgreSQL connection string | postgresql+psycopg://user:pass@host/db |
| NEO4J_URI | Neo4j Bolt URI | bolt://neo4j:7687 |
| NEO4J_USER | Neo4j username | neo4j |
| NEO4J_PASSWORD | Neo4j password | my-secret-password |
| CHROMA_HOST | ChromaDB host | chromadb-service |
| CHROMA_PORT | ChromaDB port | 8000 |

### Deployment Steps (Render/Railway)
1. In your PaaS dashboard, create a new **Web Service** or **App**.
2. Connect your GitHub repository.
3. **Build Settings:**
   - **Source Directory:** / (Root of the repository)
   - **Dockerfile Path:** infra/docker/api.Dockerfile
4. Add all the required Environment Variables.
5. Deploy the service.
6. The service will expose port 8000. Make sure the health check points to GET /health.

---

## 3. Docker Compose (Self-Hosted / Validation)

To validate the production configuration locally, use the provided docker-compose.yml.

1. Ensure the Docker daemon is running.
2. Build and start the production containers:
   docker compose up --build -d
3. The API will be available at http://localhost:8000.
4. The Web app will be available at http://localhost:3000.

*Note: In production mode, local codebase changes are not synced into the containers. Rebuild the images to see changes.*

---

## Troubleshooting

- **CORS Errors:** Ensure the frontend URL is correctly set in BACKEND_CORS_ORIGINS without trailing slashes.
- **OpenAPI Docs Missing:** In production mode, /docs and /redoc are intentionally disabled for security. Set APP_ENV=development to enable them.
- **Database/Neo4j Connection Refused:** Verify that the respective URI/Host environment variables point to publicly accessible or internally linked services, not localhost.
