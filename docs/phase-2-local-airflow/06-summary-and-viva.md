# Phase 2 — Summary and Viva Questions

## What We Built

A local, containerized Apache Airflow 2.x environment defined entirely in `docker-compose.yml`, consisting of:
- A PostgreSQL 15 metadata database (own persistent volume).
- A one-shot `airflow-init` service (DB migration + admin user creation).
- An `airflow-webserver` service exposing the UI on `http://localhost:8081`.
- An `airflow-scheduler` service running with `LocalExecutor`.
- A sample DAG (`hello_world`) proving DAGs can be authored, parsed, scheduled, and executed successfully end-to-end.

## Why We Built It This Way

- **Docker Compose over manual `docker run`**: one declarative file captures every service, its config, volumes, and startup order — reproducible on any machine (a requirement for later staging/production parity).
- **Separate services per Airflow component**: mirrors Airflow's real distributed architecture and how staging/production will also be structured, rather than a single "do everything" container that would hide real operational behavior.
- **`LocalExecutor`**: sufficient for local development and grading; avoids the added complexity of Celery/Redis/multiple workers, which the project doesn't currently need.
- **Bind-mounted `dags/`**: lets DAG development happen entirely on the host filesystem (tracked by Git) with zero rebuilds — the same DAGs will later be what CI validates and what gets deployed to staging/production.
- **Pinned image version (`apache/airflow:2.9.3`)**: guarantees the exact same Airflow build will be used in every environment this project stands up later.

## What Is Still Not Built

- No staging or production environments (Phase 5, Phase 9).
- No GitHub Actions / CI pipeline (Phase 4).
- No automated deployment or promotion logic.
- No unit or integration tests (Phase 3, Phase 7).
- No rollback mechanism.

## Likely Viva Questions

1. Why does Airflow need a separate scheduler and webserver instead of one process?
2. What is the difference between a Docker image and a Docker container?
3. Why is `LocalExecutor` appropriate here but not for a production-scale deployment?
4. What is a bind mount, and why was it used for `dags/` instead of copying files into the image?
5. Why does the metadata database need its own named volume separate from the container?
6. What actually happens when you run `docker compose up`? What's the difference between that and `docker compose up -d`?
7. Why did the scheduler container show "unhealthy" even though the scheduler process itself was working correctly? What does this teach you about healthchecks vs. actual service correctness?
8. Why was the host port changed from 8080 to 8081 instead of stopping the process using 8080?
9. How does the webserver know where to find task/DAG state, given that it never talks to the scheduler directly?
10. What would you have to change in this Compose file to add a second developer's DAG without rebuilding any image?
