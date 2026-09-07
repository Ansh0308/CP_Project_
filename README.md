# Airflow CI/CD

A CI/CD system for safely managing the lifecycle of Apache Airflow DAG changes:

```
Developer → Git → Pull Request → CI validation → Unit testing → Staging Airflow
→ Integration testing → Approval → Production deployment → Versioning/audit → Rollback
```

Full architecture, diagrams, terminology, and roadmap are documented in [`docs/`](docs/).

## Project Status

**Current phase: Phase 5 — Git development workflow.**
The repository is now hosted on GitHub at [Ansh0308/CP_Project_](https://github.com/Ansh0308/CP_Project_), with a `main` branch protection rule (PR required, status checks required) and an open Pull Request (#1) demonstrating the feature-branch → commit → push → PR workflow. No CI or automated deployment exists yet. See [`docs/roadmap/phase-roadmap.md`](docs/roadmap/phase-roadmap.md) for the full plan.

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
- Once CI passes (from Phase 4 onward) and a PR is approved, it is merged into `main`.
- A merge to `main` will eventually (from Phase 6 onward) trigger automatic deployment to staging.

## Prerequisites

- Docker Desktop (with WSL2 backend on Windows)
