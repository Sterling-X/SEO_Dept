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

## Database: Turso (libSQL)

The app uses the **`@prisma/adapter-libsql`** adapter ([src/lib/prisma.ts](../src/lib/prisma.ts)),
which speaks both local SQLite files (`file:…`, used for dev + CI) and **remote Turso**
(`libsql://…`, used in production). Two env vars control it:

| Var | Local dev | Production (Vercel) |
| --- | --- | --- |
| `DATABASE_URL` | `file:./prisma/dev.db` | `libsql://seo-dept-<org>.turso.io` |
| `DATABASE_AUTH_TOKEN` | *(unset)* | Turso db token |

### One-time Turso setup

```bash
# 1. Install + log in
brew install tursodatabase/tap/turso   # or: curl -sSfL https://get.tur.so/install.sh | bash
turso auth login

# 2. Create the database
turso db create seo-dept

# 3. Grab the two values you'll paste into Vercel
turso db show seo-dept --url          # -> DATABASE_URL
turso db tokens create seo-dept       # -> DATABASE_AUTH_TOKEN

# 4. Apply the schema (Prisma's migrate engine can't talk to Turso remote,
#    so pipe the migration SQL through the Turso shell)
turso db shell seo-dept < prisma/migrations/20260312160707_init_mvp/migration.sql
turso db shell seo-dept < prisma/migrations/20260312185345_phase2_real_exports/migration.sql
```

### Then, in Vercel → `seo-dept` → Settings → Environment Variables (Production)

- `DATABASE_URL` = the `libsql://…` URL from step 3
- `DATABASE_AUTH_TOKEN` = the token from step 3
- plus any other runtime vars the app needs (API keys, etc.)

`prisma generate` runs automatically on Vercel via the `postinstall` script.

Redeploy (push a commit or hit **Redeploy** in Vercel) and the deployment goes green.

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
