# Phase 2 — Commands Used and Verification

All commands run from the repo root: `E:\MU\CP\CP_Project`

## Startup

```bash
# One-shot: create DB schema + admin user
docker compose up airflow-init

# Start the long-running services
docker compose up -d airflow-webserver airflow-scheduler
```

## Verification Steps and Expected Results

| Check | Command | Expected Result |
|---|---|---|
| Containers running | `docker compose ps` | `postgres`, `airflow-webserver`, `airflow-scheduler` all show `Up ... (healthy)` |
| Airflow UI opens | Browse to `http://localhost:8081` | Airflow login page loads; after login (`admin`/`admin`) the DAGs list renders |
| Scheduler running | `docker compose logs airflow-scheduler` | Log shows `Loaded executor: LocalExecutor` and `Starting the scheduler` with no repeated crash/restart loop |
| Database running | `docker compose ps postgres` | `Up ... (healthy)` |
| Airflow can parse DAGs | `docker compose exec airflow-scheduler airflow dags list` | Lists `hello_world` with no errors |
| No import errors | `docker compose exec airflow-scheduler airflow dags list-import-errors` | `No data found` |
| End-to-end execution | `docker compose exec airflow-scheduler airflow dags trigger hello_world` then `airflow dags list-runs -d hello_world` | Run state becomes `success` |

## Actual Results Obtained

- `docker compose ps` showed all three containers `healthy`.
- Logged into the UI at `http://localhost:8081` with `admin`/`admin`; DAGs page showed exactly 1 DAG: `hello_world` (tags `phase-2`, `sanity-check`).
- `airflow dags list` showed `hello_world` correctly, `list-import-errors` returned no data (clean parse).
- Triggered `hello_world` manually; run completed with `state: success` in ~4 seconds, confirmed both via CLI and the DAG's Grid view in the UI (green success bar on the `say_hello` task).
