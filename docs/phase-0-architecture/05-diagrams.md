# Phase 0 — Architecture Diagrams

## Diagram 1 — System Architecture

```
                         +-----------------------------------------+
                         |              DEVELOPER MACHINE            |
                         |  edits DAG.py, runs pytest, local Airflow |
                         |        (Docker Compose, optional)         |
                         +-------------------+-----------------------+
                                              | git push
                                              v
                         +-----------------------------------------+
                         |                  GITHUB                   |
                         |   Repo (main + feature branches)          |
                         |   Pull Requests  |  Git Tags (v1.0, v1.1) |
                         +-------------------+-----------------------+
                                              | triggers on PR / push / tag
                                              v
                         +-----------------------------------------+
                         |             GITHUB ACTIONS (CI/CD)         |
                         |  +---------------+   +------------------+ |
                         |  | Lint + DAG    |   | pytest Unit Tests| |
                         |  | Validation    |   |                  | |
                         |  +---------------+   +------------------+ |
                         |  +-------------------------------------+   |
                         |  |  Deploy Job -> Staging              |   |
                         |  +-------------------------------------+   |
                         |  +-------------------------------------+   |
                         |  |  Integration Test Trigger (staging)|   |
                         |  +-------------------------------------+   |
                         |  +-------------------------------------+   |
                         |  |  Approval Gate (human required)    |   |
                         |  +-------------------------------------+   |
                         |  +-------------------------------------+   |
                         |  |  Deploy Job -> Production           |   |
                         |  |  + Git Tag + Audit Log             |   |
                         |  +-------------------------------------+   |
                         +------+-----------------------------+--------+
                                |                              |
                     deploy DAGs                deploy DAGs (after approval)
                                v                              v
        +-------------------------------+   +-------------------------------+
        |   STAGING (Docker Compose)     |   |  PRODUCTION (Docker Compose)  |
        | +---------+   +-------------+ |   | +---------+   +-------------+ |
        | |Scheduler|-->|  Postgres   | |   | |Scheduler|-->|  Postgres   | |
        | +---------+   | (staging)   | |   | +---------+   |  (prod)     | |
        | +---------+   +-------------+ |   | +---------+   +-------------+ |
        | |Webserver|                   |   | |Webserver|                   |
        | +---------+                   |   | +---------+                   |
        |  DAG = Tasks (Operators)      |   |  DAG = Tasks (Operators)      |
        +-------------------------------+   +-------------------------------+
```

## Diagram 2 — Lifecycle of One DAG Change

```
 [1] Developer edits DAG --> [2] Local pytest / local Airflow check (optional)
                                            |
                                            v
                        [3] git push feature branch -> Open PR
                                            |
                                            v
                  [4] GitHub Actions: Lint + DAG Validation + pytest
                                            |
                     +----------------------+---------------------------+
                     v FAIL                                             v PASS
        [5a] PR blocked, red status                  [5b] PR mergeable, green status
        Developer fixes -> back to [3]                          |
                                                                 v
                                         [6] PR merged into main
                                                                 |
                                                                 v
                                   [7] Auto-deploy DAG to STAGING
                                                                 |
                                                                 v
                             [8] Trigger DAG run on Staging Airflow
                                    (Integration Test)
                     +----------------------+---------------------------+
                     v FAIL                                             v PASS
        [9a] Pipeline halts, logged failure         [9b] Notify approver: staging OK
        Developer fixes -> back to [1]                          |
                                                                 v
                                        [10] Human Approval Gate
                                                                 |
                                                                 v
                                  [11] Auto-deploy DAG to PRODUCTION
                                                                 |
                                                                 v
                                [12] Git Tag created (e.g. v1.5.0)
                                     + Audit log entry written
                                                                 |
                                                                 v
                              [13] Production Scheduler runs new DAG
                     +----------------------+---------------------------+
                     v SUCCESS                                          v FAILURE
              [14a] Done - monitor normally          [14b] Trigger ROLLBACK workflow
                                                       -> checkout previous tag (v1.4.0)
                                                       -> redeploy via same deploy job
                                                       -> new audit entry logged
```
