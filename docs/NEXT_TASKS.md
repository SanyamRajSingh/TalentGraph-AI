# Next Tasks

## Current Recommended Next Module

TalentGraph AI v1.0 feature work has been completed. The project is in Release Mode only.

Allowed work:

1. Verification
2. Crash fixes
3. Broken route fixes
4. Documentation cleanup
5. Release packaging

Do not implement new features without explicit approval.

## Immediate Next Tasks

### Task 1: Update README

Status: Complete.

Reason: `README.md` previously described the project as architecture scaffolding only, which was outdated after Modules 1 through 5.

Files to modify:

```text
README.md
```

Acceptance criteria:

- README lists implemented Modules 1-7. Complete.
- README includes current API endpoints. Complete.
- README explains in-memory persistence. Complete.
- README includes backend test command. Complete.
- README notes frontend build is verified. Complete.

Potential pitfalls:

- Do not claim PostgreSQL/Neo4j/Chroma are fully implemented.
- Do not claim real OpenAI or sentence-transformer calls are active.

### Task 2: Commit Baseline

Status: Complete.

Reason: All project files are currently untracked.

Commands:

```powershell
git status --short
git add .
git commit -m "Implement TalentGraph AI modules 1-5"
```

Acceptance criteria:

- Clean or expected Git status after commit. Complete.
- No generated cache folders committed. Complete.

Potential pitfalls:

- Avoid committing `.env`.
- Avoid committing `node_modules`.
- Avoid committing `.pytest_cache`.
- Avoid committing Python `__pycache__`.

### Task 3: Verify Frontend Dependency Install

Status: Complete.

Reason: Backend tests pass, but frontend build has not been verified.

Files involved:

```text
package.json
apps/web/package.json
apps/web/app/page.tsx
```

Commands:

```powershell
npm.cmd install
npm.cmd --workspace apps/web run build
```

Acceptance criteria:

- Dependencies install successfully. Complete.
- Next.js build succeeds. Complete.
- If build fails, fix TypeScript or Next.js issues only. Not needed.

Potential pitfalls:

- PowerShell may block `npm.ps1`; use `npm.cmd`.
- Earlier `npm.cmd install` stalled in this environment. If this repeats, do not leave Node processes running.

### Task 4: Frontend UX Cleanup

Reason: The current frontend is a single dense page. It works as a demo surface but could become too long.

Files to modify:

```text
apps/web/app/page.tsx
apps/web/app/globals.css
```

Possible approach:

- Add compact tabs or segmented navigation for:
  - Role
  - Candidate
  - Evaluation
  - Ranking
  - Graph
  - Embeddings

Acceptance criteria:

- No new feature scope.
- No ranking explanations.
- No recruiter chat.
- Existing API calls still work.

Potential pitfalls:

- Do not create a marketing landing page.
- Keep the actual app workflow as the first screen.

## Module 6: Explanations + Counterfactuals

Status: Complete.

Recommended implementation order:

1. Extend or create explanation domain.
2. Implement deterministic explanation service.
3. Implement explanation repository memory/Postgres skeleton.
4. Implement `ExplanationPipeline`.
5. Add endpoints:

   ```text
   POST /api/v1/generate-explanations
   GET  /api/v1/explanations/{id}
   ```

6. Add frontend explanation panel.
7. Add tests.

Files likely to create or modify:

```text
apps/api/app/domain/explanation.py
apps/api/app/modules/explanations/service.py
apps/api/app/repositories/explanation_repository.py
apps/api/app/repositories/memory/in_memory_explanation_repository.py
apps/api/app/repositories/postgres/postgres_explanation_repository.py
apps/api/app/pipelines/explanation_pipeline.py
apps/api/app/contracts/requests/explanation_requests.py
apps/api/app/contracts/responses/explanation_responses.py
apps/api/app/api/v1/router.py
apps/api/app/api/v1/dependencies.py
apps/api/tests/explanations/
apps/web/app/page.tsx
packages/shared/src/index.ts
```

Acceptance criteria:

- Explanation uses existing evaluation/ranking data. Complete.
- No LLM calls unless explicitly approved. Complete.
- Counterfactuals included because the approved Module 6 scope requested them. Complete.
- Tests cover service, counterfactual service, repository, pipeline, API. Complete.

Potential pitfalls:

- Do not mutate ranking outputs to include recommendations unless approved.
- Do not add autonomous agents.

## Module 7: Dashboard + XLSX Export + Demo Dataset

Status: Complete.

Completed:

- Five-step dashboard workflow.
- Visual cards and role radar.
- XLSX export endpoint.
- Demo dataset.
- Release documentation.
- Backend and frontend verification.

## Future: Persistence Hardening

Only proceed if explicitly approved.

Recommended implementation order:

1. Add DB session management.
2. Add SQLAlchemy models.
3. Add migrations or simple create-all flow.
4. Implement one repository at a time.
5. Switch dependency wiring behind feature/config flag.
6. Keep memory repos for tests.

Files likely to create or modify:

```text
apps/api/app/db/session.py
apps/api/app/db/models.py
apps/api/app/repositories/postgres/*.py
apps/api/app/api/v1/dependencies.py
requirements/base.txt
requirements/dev.txt
docker-compose.yml
```

Acceptance criteria:

- Existing tests still pass with memory repositories.
- New Postgres repository tests use isolated test DB or are integration-marked.
- No production-only assumptions.

## Global Acceptance Criteria for Any Next Module

- No unrelated refactors.
- Follow existing architecture.
- Add tests.
- Keep future modules untouched.
- Run backend test suite.
- Update relevant docs if the module changes project status.

# START HERE FOR NEXT AI SESSION

1. Ask the user which next module is approved if they have not explicitly said it.
2. Before coding, inspect:

   ```text
   docs/CURRENT_STATUS.md
   apps/api/app/api/v1/router.py
   apps/api/app/api/v1/dependencies.py
   ```

3. Implement in this order:

   ```text
   domain/contracts -> repository -> service -> pipeline -> API -> tests -> frontend
   ```

4. Stop after the approved module.
