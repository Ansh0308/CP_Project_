# Phase 2 — Docker Compose Configuration Explained

- **`x-airflow-common` anchor** — a YAML anchor/alias so the Postgres connection string, volumes, and user don't have to be repeated three times (once per Airflow service). Reduces copy-paste drift.
- **`image: apache/airflow:2.9.3`** — pinned exact version (not `latest`) so staging/production later use the identical Airflow build — reproducibility is the point of this whole project.
- **`AIRFLOW__CORE__EXECUTOR: LocalExecutor`** — tasks run as subprocesses on the scheduler container itself; no separate Celery/Redis worker cluster needed for local dev.
- **`AIRFLOW__DATABASE__SQL_ALCHEMY_CONN`** — tells every Airflow component where the metadata DB lives: `postgres` is the Compose service name, resolved automatically by Docker's internal DNS — no IP addresses needed.
- **`AIRFLOW__CORE__LOAD_EXAMPLES: "false"`** — keeps the DAGs list clean so our own DAGs are easy to find instead of buried under Airflow's ~20 bundled example DAGs.
- **`AIRFLOW__SCHEDULER__ENABLE_HEALTH_CHECK: "true"`** — required flag to expose the scheduler's `/health` endpoint on port 8974; without it Docker's healthcheck can never succeed (see troubleshooting log).
- **volumes (`./dags`, `./plugins`, `./logs`, `./config`)** — bind mounts: files on the host disk are the source of truth; the container just sees them live. Editing a DAG file locally means the scheduler picks it up immediately, no rebuild.
- **`user: "${AIRFLOW_UID:-50000}:0"`** — runs container processes as a non-root UID matching Airflow's official image convention, so files written by the container (logs) aren't root-owned on the host.
- **`postgres` healthcheck (`pg_isready`)** — Compose won't consider Postgres "ready" until it can actually accept connections, not just until the container starts.
- **`airflow-init`** — a one-shot service: runs `airflow db migrate` (creates all metadata tables) and creates the `admin`/`admin` user, then exits. Other services wait for it via `service_completed_successfully`.
- **`airflow-webserver` port `8081:8080`** — maps container port 8080 to `localhost:8081` on the host (remapped from the default 8080 due to a port conflict — see troubleshooting log).
- **webserver/scheduler healthchecks** — hit each service's own `/health` endpoint so `docker compose ps` reports real readiness, not just "container started."
- **named volume `postgres-db-volume`** — persists Postgres data across container restarts (not tied to the container's ephemeral filesystem), so `docker compose down` (without `-v`) keeps DAG run history.
