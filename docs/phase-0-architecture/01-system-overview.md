# Phase 0 — System Overview

## What the Complete System Looks Like

This is a **GitOps pipeline for Airflow DAGs** — the same discipline used for application code, applied to workflow definitions. The core idea: a DAG file is never trusted just because someone wrote it. It must survive a gauntlet of automated checks before it's allowed anywhere near production, and every version that ever ran is recorded so you can always go back.

There are three "worlds" the DAG file travels through:

1. **Developer's machine** — where the DAG is written and first tested.
2. **CI world** (GitHub Actions) — where the DAG is validated and unit-tested, but never actually run against real Airflow.
3. **Runtime world** — Staging Airflow (a rehearsal environment) and Production Airflow (the real one), each with their own Docker Compose stack, scheduler, database, and workers.

The pipeline's job is to move a DAG safely left-to-right through these worlds, and to make right-to-left movement (rollback) just as easy.
