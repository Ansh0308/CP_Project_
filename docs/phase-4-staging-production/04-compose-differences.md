# Phase 4 — What Differs Between staging/docker-compose.yml and production/docker-compose.yml

| Setting | Staging | Production | Reason |
|---|---|---|---|
| `name:` | `airflow-staging` | `airflow-production` | Gives each Compose project its own isolated network/volume/container namespace |
| Webserver host port | `8082:8080` | `8083:8080` | Avoids port collisions; both can run at once |
| Postgres volume | `staging-postgres-db-volume` | `production-postgres-db-volume` | Physically separate data — a staging DB reset never touches production |
| Admin username/password | `staging_admin` / `staging_admin` | `prod_admin` / `prod_admin` | Credentials must never be shared across environments (demonstrated: staging_admin login is rejected on production) |
| `AIRFLOW__WEBSERVER__INSTANCE_NAME` | `"STAGING"` | `"PRODUCTION"` | Visible banner in the UI so nobody mistakes one environment for the other |
| `AIRFLOW__WEBSERVER__EXPOSE_CONFIG` | `"true"` | `"false"` | Production should not expose its internal Airflow config over the web UI — a small but real hardening difference |
| DAG/plugins/logs/config volumes | `./dags`, etc. (relative to `staging/`) | `./dags`, etc. (relative to `production/`) | Each environment reads DAGs from its own folder, not a shared one |

## What Stays Identical

- `apache/airflow:2.9.3` image version
- `LocalExecutor`
- Service names and Compose file structure (`postgres`, `airflow-init`, `airflow-webserver`, `airflow-scheduler`)
- Scheduler health check configuration

Keeping these identical is what makes staging a meaningful rehearsal for production — if the environments' fundamental architecture differed, a successful staging run would prove nothing about production.
