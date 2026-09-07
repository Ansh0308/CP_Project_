# Phase 4 — Commands and Verification

## Starting Staging

```bash
cd staging
docker compose up airflow-init                          # one-shot: DB migrate + staging_admin user
docker compose up -d airflow-webserver airflow-scheduler
```

## Starting Production

```bash
cd production
docker compose up airflow-init                           # one-shot: DB migrate + prod_admin user
docker compose up -d airflow-webserver airflow-scheduler
```

## Verification Performed

| Check | Method | Result |
|---|---|---|
| Staging containers healthy | `docker ps` | `airflow-staging-postgres-1`, `-airflow-scheduler-1`, `-airflow-webserver-1` all `healthy` |
| Production containers healthy | `docker ps` | `airflow-production-postgres-1`, `-airflow-scheduler-1`, `-airflow-webserver-1` all `healthy` |
| Staging UI reachable | Browser to `http://localhost:8082` | Login page titled "Sign In - STAGING" |
| Production UI reachable | Browser to `http://localhost:8083` | Login page titled "Sign In - PRODUCTION" |
| Ports do not conflict | Both UIs open simultaneously | Staging on 8082, Production on 8083, dev on 8081 — no clashes |
| Databases are separate (auth) | Logged into staging with `staging_admin`/`staging_admin` (success); tried same credentials on production | **"Invalid login. Please try again."** on production — proves separate user tables/DBs |
| Databases are separate (volumes) | `docker volume ls` | Three distinct volumes: `airflow-staging_staging-postgres-db-volume`, `airflow-production_production-postgres-db-volume`, `cp_project_postgres-db-volume` |
| Same DAGs exist in both | Logged into each UI separately with correct credentials | Both staging and production DAGs list show `hello_world` and `sales_data_pipeline`, both freshly paused with zero run history (proving genuinely fresh, isolated DBs) |
| Environments run independently | Stopped the dev environment (`docker compose stop` in repo root) while staging/production kept running | Staging and production containers remained `healthy` and unaffected |

## Screenshots-equivalent (state confirmed via UI navigation)

- `http://localhost:8082` → banner "STAGING", DAGs: `hello_world`, `sales_data_pipeline` (2 total, both paused, 0 runs)
- `http://localhost:8083` → banner "PRODUCTION", DAGs: `hello_world`, `sales_data_pipeline` (2 total, both paused, 0 runs)
