# Submission Checklist

## Repository

- [x] GitHub repo clean (all changes committed, tag v1.0 created)
- [x] README updated (modules 1-7, endpoints, architecture diagram, setup, known limitations)
- [x] Architecture diagram added (Mermaid in README)
- [ ] Screenshots captured (capture manually after running the demo)
- [x] Demo dataset verified (`data/demo/` — 1 job + 4 resumes)

## Code Quality

- [x] Backend tests passing: `53 passed, 2 warnings`
- [x] Frontend build verified: Next.js production build passing
- [x] No `.env` committed
- [x] No `node_modules` committed
- [x] No `__pycache__` committed
- [x] No `.ruff_cache` committed
- [x] XLSX export endpoint verified

## Docker

- [x] `docker compose config` passes (valid YAML and schema)
- [ ] Docker startup verified (blocked: Docker Desktop not running locally; documented limitation)

## Documentation

- [x] `docs/RELEASE_NOTES.md` — complete
- [x] `docs/DEMO_SCRIPT.md` — 2-minute walkthrough ready
- [x] `docs/SUBMISSION_CHECKLIST.md` — this file
- [x] `docs/ARCHITECTURE.md` — full design doc
- [x] `docs/PROJECT_HANDOFF.md` — future-engineer handoff complete

## Submission Assets

- [ ] PPT / slide deck (outline provided in release artifact; create slides from outline)
- [x] XLSX export output verified
- [ ] Demo video or GIF (optional but recommended)

## Release

- [x] `git tag v1.0` created
- [x] `git push origin master` completed
- [x] `git push origin v1.0` completed

## Known Limitations (Acceptable for v1.0 Hackathon Release)

1. In-memory persistence — data resets on process restart
2. PostgreSQL / Neo4j / Chroma repositories are skeleton boundaries only
3. No real OpenAI or sentence-transformer inference
4. No authentication, chat, autonomous agents, or recommendation labels
5. Docker startup requires Docker Desktop to be running
