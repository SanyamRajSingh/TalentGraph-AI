# TalentGraph AI v1.0 Release Notes

**Release Date:** 2026-06-27
**Tag:** v1.0
**Branch:** master

## Implemented Modules

1. Role DNA Generator
2. Candidate Digital Twin Builder
3. Knowledge Graph + Embedding Foundation
4. Candidate Evaluation Engine
5. Ranking Engine + Hiring Personas
6. Explainability + Counterfactuals
7. Dashboard + XLSX Export + Demo Dataset

## Architecture Overview

```text
API Router -> Pipeline -> Service -> Provider/Repository -> Domain Model
```

The release uses deterministic local providers and in-memory repositories for a reliable hackathon demo. External persistence and AI integrations remain explicit skeleton or provider boundaries.

Primary end-to-end flow:

```text
Job Description
-> Role DNA
-> Candidate Twins
-> Knowledge Graph + Embeddings
-> Evaluation
-> Ranking
-> Explanations
-> XLSX Export
```

## Verification Results

- Backend tests: `53 passed, 1 warning`
- Frontend build: passing
- Demo dataset execution: verified through API flow
- XLSX export generation: verified
- Docker Compose config: passing
- Docker Compose startup: blocked because Docker Desktop daemon is not running locally

Known warning:

- FastAPI/Starlette TestClient emits an upstream deprecation warning.
- Docker client is installed, but `docker compose up --build -d` cannot connect to `dockerDesktopLinuxEngine` until Docker Desktop is running.

## Known Limitations

- In-memory persistence resets when the API process restarts.
- PostgreSQL, Neo4j, and Chroma implementations are skeletons only.
- No real OpenAI calls or sentence-transformer inference.
- No authentication.
- No recruiter chat/copilot.
- No notifications.
- No autonomous agents.
- No Hire/No Hire recommendations.

## Future Improvements

- Add production database schema and migrations.
- Add optional real vector persistence.
- Add CI checks for backend tests and frontend build.
- Add screenshot assets and a short demo video.
- Add deployment-specific configuration.
