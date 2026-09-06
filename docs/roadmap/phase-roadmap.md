# Phase Roadmap

| Phase | Name | Goal |
|---|---|---|
| **0** | Architecture & Concepts | *(no code)* Understand the full system |
| **1** | Local Environment Setup | Docker Compose for a single local Airflow (dev sandbox) |
| **2** | Repo & DAG Structure | Set up Git repo, folder layout, sample DAGs |
| **3** | Unit Testing Layer | pytest suite for DAG validation/unit tests |
| **4** | CI Pipeline | GitHub Actions workflow: lint + validate + pytest on PR |
| **5** | Staging Environment | Second Docker Compose stack (staging Airflow + its own Postgres) |
| **6** | Auto-deploy to Staging | GitHub Actions job: on merge to main, deploy to staging |
| **7** | Integration Testing | Trigger real DAG runs on staging, assert success via Airflow API/CLI |
| **8** | Approval Gate | GitHub Environments with required reviewers before prod job runs |
| **9** | Production Environment | Third Docker Compose stack (production Airflow + its own Postgres) |
| **10** | Auto-deploy to Production | GitHub Actions job: deploy after approval |
| **11** | Versioning & Audit | Git tagging automation + deployment log (file, DB, or GitHub Releases) |
| **12** | Rollback Mechanism | Manual-trigger workflow to redeploy a prior tag |
| **13** | Failure & Recovery Demo | Intentionally break a DAG, show it caught at each gate, then demo rollback |
