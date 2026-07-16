# CI/CD Setup

Two independent pieces:

1. **CI** — GitHub Actions ([`.github/workflows/ci.yml`](workflows/ci.yml)) runs
   lint + test + build on every push/PR to `main`.
2. **CD** — **Vercel's native Git integration** builds and deploys automatically on
   every push to `main`. There is no deploy job in GitHub Actions.

> No GitHub Actions secrets are required for this setup. `VERCEL_TOKEN` /
> `VERCEL_ORG_ID` / `VERCEL_PROJECT_ID` are only needed if you deploy *from* Actions,
> which we are not doing.

## CI job

| Trigger | Runs? |
| --- | --- |
| Pull request → `main` | ✅ |
| Push → `main` | ✅ |

Steps: `npm ci` (runs `postinstall` → `prisma generate`) → `prisma migrate deploy`
(creates a throwaway SQLite DB) → `npm run lint` → `npm test` → `npm run build`.

## Vercel deployment — required project settings

The Vercel project `seo-dept` (scope `lostphoenix33's-projects`) is already linked to
`Sterling-X/SEO_Dept`. For its builds to succeed you must configure, in
**Vercel → Project → Settings → Environment Variables** (Production):

- `DATABASE_URL` — **must point at a hosted database, not SQLite** (see below).
- Any other runtime vars the app needs (API keys, etc.).

`prisma generate` runs automatically on Vercel via the `postinstall` script.

### ⚠️ SQLite will not work on Vercel

The app currently uses **Prisma + SQLite** (`better-sqlite3`, `prisma/dev.db`). Vercel's
serverless filesystem is ephemeral/read-only at runtime — writes fail or vanish between
requests. Migrate before relying on the deploy:

1. **Turso / libSQL** — closest to SQLite, minimal schema changes.
2. **Postgres** (Neon / Vercel Postgres / Supabase) — set
   `datasource db { provider = "postgresql" }` in `prisma/schema.prisma`, re-run migrations.

## Optional: make Vercel wait for CI to pass

Vercel deploys on push **regardless** of whether GitHub Actions CI passed. To only ship
green commits, use Vercel's **Ignored Build Step** (Project → Settings → Git) or require
the CI check on the branch. Ask if you want this wired up.

## Local checks (mirror CI before pushing)

```bash
npm ci
npx prisma migrate deploy   # creates prisma/dev.db
npm run lint
npm test
npm run build
```
