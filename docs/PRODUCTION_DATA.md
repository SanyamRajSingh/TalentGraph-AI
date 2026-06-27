# TalentGraph AI — Production Data Guide

## Overview

TalentGraph AI supports two storage modes and automatically seeds demo data on every cold start.

---

## Storage Modes

### 1. PostgreSQL Mode (Production / Render)

Set the `DATABASE_URL` environment variable to a PostgreSQL connection string:

```
DATABASE_URL=postgresql://user:password@host:5432/talentgraph
```

**What happens on startup:**
- SQLAlchemy creates all tables automatically (idempotent `CREATE TABLE IF NOT EXISTS`)
- The startup seeder checks if candidates exist
- If empty → seeds 50 candidates + 10 roles + full pipeline data
- If already populated → skips seeding (no-op)
- All data persists across restarts

**Render setup:**
1. Create a PostgreSQL database on Render
2. Copy the internal connection string
3. Set `DATABASE_URL` in your Render backend service environment variables
4. Redeploy — tables and seed data are created automatically

---

### 2. Memory Mode (Default / Development)

No `DATABASE_URL` set, or `DATABASE_URL` points to SQLite.

**What happens on startup:**
- In-memory repositories are used (no disk persistence)
- Startup seeder always runs (repositories are empty on every restart)
- Data is seeded fresh on every cold start (~5–10 seconds)
- Data is lost on restart — this is expected

**To run locally:**
```bash
cd apps/api
$env:PYTHONPATH="."; uvicorn app.main:app --reload
```

---

## Automatic Seeding Behaviour

The seeder (`app/startup/seeder.py`) runs inside the FastAPI `lifespan` context on every startup.

### Seed contents

| Entity | Count | Details |
|---|---|---|
| Candidates | 50 | 10 per role × 5 roles (Backend, ML, Data Science, Product Analyst, Full Stack) |
| Job Roles | 10 | Senior + Lead per role type |
| Evaluations | up to 500 | Every candidate × every role |
| Rankings | 20 | 2 personas (startup_founder, enterprise_recruiter) × 10 roles |
| Explanations | 50 | Every candidate vs. first role |
| Embeddings | 10 | First 10 candidates vs. first role (fast startup) |
| Graph snapshots | 5 | First 5 candidates vs. first role |

### Candidate diversity

| Dimension | Values |
|---|---|
| Roles | Backend Engineer, ML Engineer, Data Scientist, Product Analyst, Full Stack Engineer |
| Levels | Junior, Mid-Level, Senior, Lead, Principal |
| Domains | Fintech, Healthcare, E-commerce, EdTech, SaaS, Cybersecurity, Cloud, AI/ML, Gaming, Automotive |
| Locations | San Francisco, New York, Austin, Seattle, Remote, London, Berlin, Toronto |

### Idempotency

The seeder guards against duplicate data:

```python
existing = candidate_repository.list_candidates()
if existing:
    logger.info("Seeder: %d candidates already loaded — skipping.", len(existing))
    return
```

Safe to restart multiple times — only seeds when the repository is empty.

---

## Startup Logs

A successful cold start produces logs like:

```
Startup seeder: repository is empty — seeding demo data...
  Loaded 10 jobs
  Loaded 50 candidates
  Loaded evaluations (500)
  Loaded rankings (20 runs)
  Loaded explanations (50)
  Loaded embeddings (10)
  Loaded graph data (5 snapshots)
Startup seeder: DONE
```

A warm start (data already exists) produces:

```
Startup seeder: 50 candidates already loaded — skipping.
```

---

## Verifying the Seed

After startup, these endpoints should return populated data:

```bash
# 50 candidates
GET /api/v1/candidates

# 10 job roles
GET /api/v1/role-dna

# Rankings for first seeded role
GET /api/v1/rankings?role_id=seed_role_00

# Copilot (uses seeded candidate)
POST /api/v1/copilot/chat
{"role_id": "seed_role_00", "candidate_id": "seed_backend_engineer_00", "message": "What are their strengths?"}
```

---

## Running Tests

```bash
cd apps/api
C:/Users/sanya/anaconda3/python.exe -m pytest tests/ -q
```

All 88+ tests should pass in both memory and postgres modes.

## Building the Frontend

```bash
cd apps/web
npm run build
```

Should compile clean with 0 TypeScript errors.
