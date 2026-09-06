# Phase 1 — Why Every Directory Exists

| Directory | Why it exists | What lands here later |
|---|---|---|
| `dags/` | The actual product being shipped through the whole pipeline. Keeping DAGs in one dedicated folder means the deploy step can copy/sync *exactly this folder* into Airflow's `dags/` — nothing more, nothing less. | Phase 2+: Python DAG files |
| `tests/` | Separates test code from production code, mirroring how pytest expects to discover tests. Keeping tests outside `dags/` means test files never accidentally get deployed to Airflow. | Phase 3: `test_dag_validation.py`, etc. |
| `plugins/` | Airflow has a first-class `plugins/` folder for custom operators/hooks/sensors that aren't in core Airflow. Kept separate from DAGs because plugins are infrastructure, DAGs are workflow definitions. | Only if the project needs a custom operator/hook |
| `scripts/` | Deployment and rollback are operations, not DAG logic. Isolating them means CI/CD workflows call one well-known script instead of embedding deploy logic inline in YAML. | Phase 6/10: `deploy.sh`, Phase 12: `rollback.sh` |
| `staging/` | Staging needs its own Docker Compose file, `.env`, and Airflow config — separate from prod so the two environments can never accidentally collide. | Phase 5: `docker-compose.yaml`, staging `.env` |
| `production/` | Same reasoning as staging, kept as a separate folder (not a flag on one shared compose file) so a mistake editing "the" compose file can't affect both environments at once. | Phase 9: `docker-compose.yaml`, prod `.env` |
| `.github/workflows/` | GitHub Actions only discovers workflow YAML files in this exact path. | Phase 4+: `ci.yml`, `deploy-staging.yml`, `deploy-production.yml`, `rollback.yml` |
| `requirements.txt` | Pins Python dependencies so CI, staging, and production all install the same package versions. | Grows as `apache-airflow`, `pytest`, etc. are added |
| `README.md` | Single entry point for anyone to understand what the repo is and how to navigate it. | Living document, updated every phase |
| `.gitignore` | Prevents committing machine-specific junk or secrets. | Static, occasionally extended |
