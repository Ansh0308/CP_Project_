# Phase 4 — Summary and Viva Questions

## What We Built

Two additional, fully independent Docker Compose–based Airflow environments — `staging/` and `production/` — each with:
- Its own Postgres metadata database (separate named volume)
- Its own admin user/credentials
- Its own host port for the webserver (8082 staging, 8083 production; dev remains 8081)
- Its own `dags/`, `plugins/`, `logs/`, `config/` folders
- The same Airflow image version, executor, and Compose service structure as each other and as the dev environment

Both were started, verified healthy, logged into with their own distinct credentials, and confirmed to contain the same sample DAGs (`hello_world`, `sales_data_pipeline`) as the dev environment.

## Why We Built It This Way

- **Separate Compose `name:` per environment** — the cleanest way to get isolated networks, volumes, and container names from Compose without manual `-p` flags every time.
- **Identical image/executor/structure, different identity (ports, credentials, DB)** — staging must resemble production closely enough to be a meaningful rehearsal, while remaining impossible to confuse with it or accidentally cross-contaminate.
- **Manual DAG copying (for now)** — deliberately not automated yet; Phase 4's job is to prove the destinations work, not to build the pipe that fills them.

## What Is Still Not Built

- No automatic DAG synchronization/deployment (Phase 6 for staging, Phase 10 for production).
- No GitHub Actions / CI pipeline (Phase 4→ next is actually numbered Phase 5+ in some plans, but per this project's roadmap: CI comes next).
- No approval gate.
- No Git tagging / versioning / audit log.
- No rollback mechanism.

## Likely Viva Questions

1. Why does each environment need its own Postgres volume instead of one shared database with a `staging`/`production` schema split?
2. What real-world problem does the memory issue encountered in this phase illustrate about running staging and production "too close together"?
3. Why was `AIRFLOW__WEBSERVER__EXPOSE_CONFIG` disabled specifically for production?
4. If staging and production run the exact same DAG file, what's actually different about how it behaves in each?
5. What does the Compose top-level `name:` field control, and what would happen without it if you ran `docker compose up` in both `staging/` and `production/` from folders with the same basename?
6. Why did logging into production with staging's credentials fail — what does that prove about the two environments?
7. What manual step in this phase is Phase 6+ going to automate, and why wasn't it automated now?
8. Why is it acceptable (or even expected) that both environments' DAGs show zero run history at this point?
9. What would you have to change to add a third environment (e.g. "QA") following this same pattern?
10. Why is `LocalExecutor` still appropriate for both staging and production here, given the earlier discussion of production needing to be "stable"?
