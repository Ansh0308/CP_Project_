# Phase 0 — Components and Their Responsibilities

| Component | Responsibility |
|---|---|
| **Developer** | Writes/edits DAG code, writes unit tests, opens a Pull Request. Cannot push directly to production. |
| **Git** | Version control system. Every DAG change is a diff, every state is a commit hash. This is the source of truth. |
| **GitHub** | Hosts the Git repo remotely; provides PR workflow, branch protection, and triggers for CI/CD. |
| **Pull Request (PR)** | The checkpoint gate. No DAG change reaches `main` without one. It's where CI results are visible and human approval happens. |
| **GitHub Actions** | The automation engine. Listens for events (PR opened, merge to main, tag pushed) and runs jobs: lint, validate, test, build, deploy. |
| **CI (Continuous Integration)** | The *practice* of automatically checking every change before it merges. Implemented here via GitHub Actions jobs. |
| **Airflow** | The workflow orchestration platform itself — schedules and executes DAGs. |
| **DAG (Directed Acyclic Graph)** | A Python file defining a workflow: a set of Tasks and their dependencies. This is the actual artifact being shipped through the pipeline. |
| **Task** | A single unit of work inside a DAG (e.g., "extract data", "run transform"). |
| **Operator** | A template/class that defines *what kind* of work a Task does (e.g., `PythonOperator`, `BashOperator`). Tasks are instances of Operators. |
| **Scheduler** | The Airflow component that reads DAG files, decides when tasks should run, and queues them. |
| **PostgreSQL** | Airflow's metadata database — stores DAG run history, task state, connections, variables. Staging and Production each have their **own** Postgres instance (never shared). |
| **Docker** | Containerizes each component (webserver, scheduler, worker, Postgres) so environments are reproducible. |
| **Docker Compose** | Orchestrates multiple containers together to stand up a full Airflow environment (staging or prod) with one command. |
| **Staging** | A near-identical, lower-stakes copy of production Airflow. Used to run integration tests against real Airflow internals before anything touches prod. |
| **Production** | The real, business-critical Airflow environment. Only receives DAGs that passed every prior gate. |
| **pytest** | The test runner used for DAG unit tests (e.g., "does this DAG import without errors," "does it have the expected task count/dependencies"). |
| **Integration Testing** | Testing the DAG *inside a running Airflow instance* (staging) — actually triggering a DAG run and checking it completes and produces correct results. |
| **Git tags** | Immutable markers (e.g., `v1.4.0`) pointing at a specific commit that was deployed to production. This is your version history. |
| **Deployment** | The act of copying validated DAG files into an Airflow environment's `dags/` folder (staging or production). |
| **Rollback** | Redeploying a previous known-good Git tag when the current production version misbehaves. |
