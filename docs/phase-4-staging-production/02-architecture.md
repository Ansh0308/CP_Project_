# Phase 4 — Architecture

```
                    HOST MACHINE (Docker Desktop / WSL2)

  +----------------------------+   +----------------------------+
  |      STAGING (airflow-staging)  |      PRODUCTION (airflow-production) |
  |  docker-compose project     |   |  docker-compose project     |
  |                              |   |                              |
  |  +---------+  +-----------+ |   |  +---------+  +-----------+ |
  |  |Scheduler|->| Postgres  | |   |  |Scheduler|->| Postgres  | |
  |  +---------+  | (staging) | |   |  +---------+  |  (prod)   | |
  |  +---------+  +-----------+ |   |  +---------+  +-----------+ |
  |  |Webserver| :8082          |   |  |Webserver| :8083          |
  |  +---------+                |   |  +---------+                |
  |  DAGs: ./staging/dags        |   |  DAGs: ./production/dags     |
  |  Volume: staging-postgres-   |   |  Volume: production-postgres-|
  |          db-volume           |   |          db-volume           |
  +----------------------------+   +----------------------------+

  (Phase 2/3 dev environment, project "cp_project", also exists
   separately: Webserver :8081, its own Postgres volume, ./dags)

  No network connection between the three projects. No shared
  volumes. No shared credentials. Fully independent.
```

Each environment is its own Docker Compose **project** (set via the top-level `name:` field in each `docker-compose.yml`), which means Compose gives each one its own isolated network and namespaced container names/volumes automatically — `airflow-staging-*` vs `airflow-production-*` vs `cp_project-*`.
