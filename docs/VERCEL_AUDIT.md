# Vercel Deployment Audit

## 1. Repository Structure
- The project is a monorepo defined by the root `package.json` containing npm workspaces: `apps/web` and `packages/shared`.
- The Next.js application lives in `apps/web`.
- No `vercel.json` configuration file is present in the repository.

## 2. Next.js Configuration
- `apps/web/package.json` defines standard Next.js scripts (`dev`, `build`, `start`).
- `apps/web/next.config.ts` includes `transpilePackages: ["@talentgraph/shared"]`, confirming its dependency on the shared workspace package.
- The build command should therefore be executed from `apps/web` but must have access to the root `node_modules` (which Vercel handles automatically if the Root Directory is set).

## 3. Environment Variables
- `apps/web/.env.example` defines `NEXT_PUBLIC_API_BASE_URL=`.
- `app/page.tsx` references `process.env.NEXT_PUBLIC_API_BASE_URL`.
- Because `NEXT_PUBLIC_*` variables are statically injected into the frontend bundle at build time by Next.js, this variable **must be set in Vercel's Environment Variables before building**.

## Conclusion & Diagnosis
The Next.js app is located at `apps/web`. Vercel natively supports this if the **Root Directory** is configured as `apps/web`. If it's configured as `/`, it will fail or try to build the wrong thing. If `NEXT_PUBLIC_API_BASE_URL` is omitted, the frontend will fallback to `""` and make relative requests to its own domain (which will 404).

### Required Correct Settings
- **Framework Preset**: Next.js
- **Root Directory**: `apps/web`
- **Build Command**: `npm run build` (Vercel will detect and run this properly)
- **Install Command**: `npm install` (Vercel will run this at the root to respect workspaces)
- **Output Directory**: `.next` (Vercel default)
- **Environment Variables**: `NEXT_PUBLIC_API_BASE_URL=https://talentgraph-ai-1.onrender.com`
