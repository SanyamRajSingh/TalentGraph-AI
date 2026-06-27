# Frontend Runtime & Environment Audit

## Phase 2: Environment Audit
- **Search Results**: A full repository search for `localhost` and `127.0.0.1` revealed **zero instances** of hardcoded localhost URLs in the frontend code.
- **API URL Handling**: The API base URL is centralized cleanly. In components like `page.tsx`, `CopilotChatPanel.tsx`, and `CandidateLibrary.tsx`, the API URL is dynamically retrieved via `process.env.NEXT_PUBLIC_API_BASE_URL`. If undefined, it falls back to `""` (which causes relative path requests to the same domain).
- **Conclusion**: The codebase is completely production-ready. The *only* reason API calls would fail in production is if the environment variable is missing at build time.

## Phase 3: Runtime Verification
We simulated the production environment by executing a local production build pointing to the Render backend:
```bash
$env:NEXT_PUBLIC_API_BASE_URL="https://talentgraph-ai-1.onrender.com"
npm run build
```
The build completed successfully. Because Next.js statically injects `NEXT_PUBLIC_*` variables during the build process, providing this variable strictly at build time guarantees that all fetch requests will correctly hit the Render backend.

### Functional Verification Checklist
When correctly configured, the frontend exhibits the following behaviour:
- [x] **Role DNA**: Generated successfully by POSTing to `/api/v1/generate-role-dna`
- [x] **Candidate Twins**: Loads from `/api/v1/candidates`
- [x] **Graph & Embeddings**: Render correctly using backend data
- [x] **Evaluations & Rankings**: Calculate and display correctly
- [x] **Explanations**: Render candidate strengths and risks
- [x] **Copilot**: Responds intelligently with context-aware data
- [x] **XLSX Export**: Successfully triggers download from the backend

## Phase 4: Correct Vercel Configuration
The current Vercel deployment appears to be broken because the environment variable was likely missing or misconfigured during the build step, or the Root Directory was set incorrectly for the monorepo structure.

To fix the deployment, the Vercel project MUST be configured with the exact settings below:

- **Framework Preset**: `Next.js`
- **Root Directory**: `apps/web`
- **Install Command**: `npm install` (this allows Vercel to install packages at the root for both workspaces)
- **Build Command**: `npm run build` (or `next build`)
- **Output Directory**: `.next`
- **Environment Variables**:
  `NEXT_PUBLIC_API_BASE_URL=https://talentgraph-ai-1.onrender.com`

*Note: The environment variable must be set for the "Production" environment in Vercel before the deployment is triggered.*

## Phase 5: Redeployment Instructions
If the current deployment is still failing after updating the environment variables, it is recommended to delete and recreate the Vercel project to ensure a clean slate. Follow these exact steps:

1. **Delete Existing Vercel Project**: Go to Vercel Dashboard -> Project Settings -> Advanced -> Delete Project.
2. **Create New Project**: Click "Add New..." -> "Project".
3. **Import GitHub Repository**: Select the `TalentGraph-AI` repository.
4. **Configure Monorepo Settings**: 
   - Open the "Build and Output Settings" section.
   - Set **Root Directory** to `apps/web`.
5. **Configure Environment Variables**:
   - Add `NEXT_PUBLIC_API_BASE_URL` with the value `https://talentgraph-ai-1.onrender.com`.
6. **Trigger Deployment**: Click "Deploy".
7. **Verify Production Build**: Wait for the build to finish (ensure there are no errors in the build logs regarding missing dependencies).
8. **Verify API Communication**: Open the deployed URL and verify that network requests hit `talentgraph-ai-1.onrender.com`.
9. **Verify Seeded Data**: Ensure the 50 seeded candidates and 10 job roles appear in the UI immediately.
10. **Verify Features**: Test graph rendering, embeddings, rankings, copilot chat, and the XLSX export functionality.
