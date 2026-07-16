# CI/CD Setup

The app runs on **Google Cloud Run** with a **Cloud SQL for PostgreSQL** database, all
in the GCP project **`sterlingx-insights`** (region **`us-central1`**).

## Pipelines

| Workflow | Trigger | What it does |
| --- | --- | --- |
| [`ci.yml`](workflows/ci.yml) | push + PR to `main` | Spins up a throwaway Postgres, runs `prisma migrate deploy`, then **lint → test → build**. |
| [`deploy.yml`](workflows/deploy.yml) | push to `main` | Builds the image (Cloud Build), applies migrations to Cloud SQL (via Cloud SQL Auth Proxy), then **deploys to Cloud Run**. |

**Live URL:** https://seo-dept-315627031.us-central1.run.app

## GCP resources

| Resource | Name |
| --- | --- |
| Cloud Run service | `seo-dept` |
| Cloud SQL instance | `seo-dept-db` (POSTGRES_16, db-f1-micro) |
| Database / user | `seo_dept` / `seo_app` |
| Connection name | `sterlingx-insights:us-central1:seo-dept-db` |
| Artifact Registry | `us-central1-docker.pkg.dev/sterlingx-insights/seo-dept` |
| Runtime service account | `seo-dept-run@sterlingx-insights.iam.gserviceaccount.com` |
| Deploy service account | `github-deployer@sterlingx-insights.iam.gserviceaccount.com` |

## Secrets

**GitHub → Settings → Secrets → Actions**
- `GCP_SA_KEY` — JSON key for the `github-deployer` service account (used by `deploy.yml`).

**Secret Manager (GCP)**
- `seo-dept-database-url` — full `DATABASE_URL` (Cloud SQL socket form); mounted into Cloud Run at runtime.
- `seo-dept-db-app-password` — password for `seo_app` (used by the migration step).
- `seo-dept-db-root-password` — Postgres root password.

## Database connection

The app uses Prisma with the **`@prisma/adapter-pg`** driver adapter
([src/lib/prisma.ts](../src/lib/prisma.ts)) and reads `DATABASE_URL`:

- **Cloud Run:** `...@localhost/seo_dept?host=/cloudsql/<connection-name>` (Unix socket, injected from Secret Manager).
- **CI / local:** standard TCP `postgresql://user:pass@host:5432/db`.

## Deploying

Just **push to `main`** — `deploy.yml` builds, migrates, and rolls out a new Cloud Run
revision automatically.

Manual deploy of the current code:
```bash
gcloud builds submit --tag us-central1-docker.pkg.dev/sterlingx-insights/seo-dept/app:manual --project sterlingx-insights
gcloud run deploy seo-dept --image us-central1-docker.pkg.dev/sterlingx-insights/seo-dept/app:manual \
  --region us-central1 --service-account seo-dept-run@sterlingx-insights.iam.gserviceaccount.com \
  --add-cloudsql-instances sterlingx-insights:us-central1:seo-dept-db \
  --set-secrets DATABASE_URL=seo-dept-database-url:latest --allow-unauthenticated
```

## Local development

```bash
docker run --name seo-pg -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=seo_dept -p 5432:5432 -d postgres:16
cp .env.example .env.local            # DATABASE_URL points at localhost:5432
npm ci
npx prisma migrate deploy
npm run dev
```

## ⚠️ Access control

The Cloud Run service is deployed with **`--allow-unauthenticated`** (publicly reachable).
To restrict it, remove public access and put it behind Identity-Aware Proxy or require
authentication:
```bash
gcloud run services remove-iam-policy-binding seo-dept --region us-central1 \
  --member=allUsers --role=roles/run.invoker
```
