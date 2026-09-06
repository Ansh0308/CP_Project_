# Phase 2 — Core Concepts

1. **Docker** — a platform for packaging an application together with everything it needs (code, runtime, system libraries, config) into a single unit that runs identically on any machine, eliminating "works on my machine" problems.

2. **Docker image** — a read-only, versioned blueprint (like a class) — e.g. `apache/airflow:2.9.3` bundles Python, Airflow, and all its dependencies into one file you can pull and reuse.

3. **Container** — a running instance of an image (like an object instantiated from that class). Multiple containers can run from the same image, each isolated from the others and from the host OS.

4. **Docker Compose** — a tool that defines multiple containers (and how they connect — networks, volumes, startup order) in one YAML file, so `docker compose up` starts an entire multi-service application with one command.

5. **Why Airflow needs multiple services** — Airflow is a distributed system with distinct responsibilities (parsing DAGs, deciding what to run, executing tasks, serving a UI, storing state) that scale and fail independently. Bundling them into one container would mean a UI crash could take down task execution.

6. **Scheduler** — continuously scans the `dags/` folder, evaluates each DAG's schedule, and decides when task instances are due to run, then queues them for execution.

7. **Webserver** — serves the Airflow UI (and REST API) so humans can view DAGs, trigger runs, inspect logs, and check status. It does not execute anything itself.

8. **Metadata database (PostgreSQL)** — the single source of truth for all state: DAG run history, task instance status, connections, variables, user accounts. Scheduler and webserver both read/write here instead of talking to each other directly.

9. **Executor** — decides how and where queued tasks actually run. This project uses `LocalExecutor` (runs tasks as local subprocesses on the same machine) — the simplest option for local dev, no separate worker/broker needed.

10. **Communication** — Scheduler and Webserver both connect directly to PostgreSQL over the network (never to each other). The Scheduler writes task/DAG run state to the DB; the Webserver reads that same DB to render the UI. With `LocalExecutor`, the Scheduler spawns and manages task subprocesses itself. All of this happens inside one Docker Compose network, with services addressed by name (e.g. `postgres:5432`).
