# Airflow CI/CD

A CI/CD system for safely managing the lifecycle of Apache Airflow DAG changes:

```
Developer → Git → Pull Request → CI validation → Unit testing → Staging Airflow
→ Integration testing → Approval → Production deployment → Versioning/audit → Rollback
```

Full architecture, diagrams, terminology, and roadmap are documented in [`docs/`](docs/).

## Project Status

**Current phase: Phase 7 — Unit testing with pytest.**
`.github/workflows/ci.yml` runs four validation layers on every PR and push to `main`: Python syntax, Airflow DAG import validation, custom project lint rules, and now pytest unit tests (`tests/`) covering DAG structure and individual task logic, with Airflow's XCom/database mocked. `main` is protected (PR + all four CI layers required, enforced even for the repository owner). No automated staging/production deployment exists yet. See [`docs/roadmap/phase-roadmap.md`](docs/roadmap/phase-roadmap.md) for the full plan.

## Running Locally

```bash
cp .env.example .env
docker compose up airflow-init
docker compose up -d airflow-webserver airflow-scheduler
```

Then open http://localhost:8081 (login: `admin` / `admin`).

### Staging

```bash
cd staging
docker compose up airflow-init
docker compose up -d airflow-webserver airflow-scheduler
```

Open http://localhost:8082 (login: `staging_admin` / `staging_admin`).

### Production

```bash
cd production
docker compose up airflow-init
docker compose up -d airflow-webserver airflow-scheduler
```

Open http://localhost:8083 (login: `prod_admin` / `prod_admin`).

> Note: running all three environments at once may exceed available memory on lower-spec machines (see [docs/phase-4-staging-production/06-troubleshooting-log.md](docs/phase-4-staging-production/06-troubleshooting-log.md)). Run at most two at a time if you hit issues.

## Running Tests

```bash
pip install --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.9.3/constraints-3.12.txt" -r requirements.txt
pytest tests/ -v
```

> Note: Apache Airflow does not run natively on Windows (see [docs/phase-7-unit-testing/04-troubleshooting-log.md](docs/phase-7-unit-testing/04-troubleshooting-log.md)) — run this inside the dev Docker container, WSL2, or Linux/macOS.

## Repository Structure

```
airflow-cicd/
├── dags/                 # Airflow DAG definitions (added from Phase 2)
├── tests/                # pytest unit tests for DAGs (added from Phase 3)
├── plugins/              # Custom Airflow operators/hooks/sensors, if needed
├── scripts/              # Deployment and rollback scripts (added from Phase 6+)
├── staging/              # Staging environment Docker Compose + config (added Phase 5)
├── production/           # Production environment Docker Compose + config (added Phase 9)
├── .github/workflows/    # GitHub Actions CI/CD pipelines (added from Phase 4)
├── docs/                 # Architecture docs, roadmap, checklists, demo plan
├── requirements.txt      # Python dependencies
├── README.md             # This file
└── .gitignore
```

## Git Workflow

- `main` is the source of truth. All changes land here through Pull Requests only.
- Work happens on short-lived feature branches: `feature/<name>` or `fix/<name>`.
- Once all CI layers pass, it is merged into `main`.
- A merge to `main` will eventually trigger automatic deployment to staging (not yet implemented).

## Prerequisites

- Docker Desktop (with WSL2 backend on Windows)
