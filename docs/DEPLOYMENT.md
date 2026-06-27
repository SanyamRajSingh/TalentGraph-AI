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

**Target Platform:** Render

The backend can be deployed effortlessly on Render using the provided Blueprint (`render.yaml`), which installs the API natively using Python.

### Environment Variables Required
| Variable | Description | Example |
|---|---|---|
| `PYTHON_VERSION` | Python runtime version | `3.12` |
| `ENVIRONMENT` | Application environment mode | `production` |
| `CORS_ORIGINS` | Comma-separated list of allowed origins | `*` (or your frontend URL) |
| `OPENAI_API_KEY` | Your OpenAI API key | `sk-proj-...` |

### Known Limitations
**IMPORTANT**: Current persistence is entirely **in-memory**. Application state (Role DNA, Candidates, Graph nodes) completely resets if the backend process restarts or the deployment goes to sleep. v1.1 does not require PostgreSQL, Neo4j, or ChromaDB.

### Deployment Steps (Render Blueprint)
1. In the Render Dashboard, click **New +** and select **Blueprint**.
2. Connect your GitHub repository.
3. Render will automatically detect the `render.yaml` file in the root.
4. Provide a value for `OPENAI_API_KEY` when prompted in the environment variables sync step.
5. Click **Apply**.
6. Render will run the `buildCommand` (`pip install -r requirements/dev.txt && pip install -e apps/api`) and start the server using `uvicorn`. The health check is mapped to `/health`.

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
