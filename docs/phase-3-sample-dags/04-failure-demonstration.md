# Phase 3 — Controlled Failure Demonstration

## Goal

Prove that Airflow correctly detects, reports, and contains a business-logic failure — without editing the pipeline's actual code.

## Mechanism

`dags/sales_data_pipeline.py` reads an environment variable, `ENABLE_INTENTIONAL_FAILURE`, inside `validate_data()`. When set to `"true"`, the task immediately raises:
```python
raise ValueError("Intentional failure: negative amount detected in dataset")
```

## Steps Taken

1. Added `ENABLE_INTENTIONAL_FAILURE: "true"` to the `airflow-scheduler` service's environment in `docker-compose.yml`.
2. Recreated the scheduler: `docker compose up -d airflow-scheduler`.
3. Triggered the DAG: `docker compose exec airflow-scheduler airflow dags trigger sales_data_pipeline`.
4. Waited through the retry cycle (`retries: 2`, `retry_delay: 30s` → up to ~90s+ before final failure).

## Result

Run `manual__2026-09-06T10:08:47+00:00` finished with **state: failed**. Per-task states:

| Task | State |
|---|---|
| fetch_data | success |
| clean_data | success |
| validate_data | **failed** (after 3 total attempts: 1 initial + 2 retries) |
| process_data | upstream_failed (never executed) |
| store_result | upstream_failed (never executed) |

The task log for `validate_data`'s final attempt confirmed the exact error:
```
raise ValueError("Intentional failure: negative amount detected in dataset")
ValueError: Intentional failure: negative amount detected in dataset
```

The Airflow UI Grid view showed this visually: green cells for `fetch_data`/`clean_data`, a red cell for `validate_data`, and orange (`upstream_failed`) cells for `process_data`/`store_result`, with the DAG summary reporting "Total success: 2, Total failed: 1" across all runs to date.

## What This Demonstrates

- **Retries have a limit and a purpose**: 3 total attempts were made (matching `retries: 2`) before Airflow gave up and marked the task failed — retries protect against transient failures, not deterministic logic errors like this one.
- **Downstream containment**: `process_data` and `store_result` never ran once their upstream dependency failed — exactly the behavior a real pipeline needs to avoid processing/storing bad or incomplete data.
- **Auditability**: the failed run remains permanently visible in DAG run history alongside successful runs — nothing was hidden or silently retried away.

## Restoration

1. Removed `ENABLE_INTENTIONAL_FAILURE` from `docker-compose.yml`.
2. Recreated the scheduler again: `docker compose up -d airflow-scheduler`.
3. Waited for the scheduler container to report `healthy`.
4. Triggered a fresh run: it completed with **state: success** (run `manual__2026-09-06T10:12:36+00:00`), while the earlier failed run remains untouched in history — proving the fix was to the environment/flag, not a rewrite of the pipeline's actual logic.
