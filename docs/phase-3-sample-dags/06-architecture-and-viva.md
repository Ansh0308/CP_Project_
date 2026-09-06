# Phase 3 — DAG Architecture and Viva Questions

## Architecture of `sales_data_pipeline`

```
fetch_data --> clean_data --> validate_data --> process_data --> store_result
```

- Linear chain, 5 `PythonOperator` tasks, no branching or parallelism (deliberately simple).
- `default_args`: `retries=2`, `retry_delay=30s` applied to every task.
- `schedule="@daily"`, `catchup=False`.
- `tags=["phase-3", "business-pipeline", "sales"]`.
- Data passed task-to-task via XCom (`xcom_push`/`xcom_pull`), not shared Python variables.
- `ENABLE_INTENTIONAL_FAILURE` env var toggles a deliberate `ValueError` inside `validate_data` for controlled failure testing, without touching pipeline code.

## Final DAG Code

See `dags/sales_data_pipeline.py` in the repository.

## What This DAG Is Designed to Later Demonstrate

- **Task dependencies**: the `>>` chain.
- **Operators**: `PythonOperator` usage.
- **Retries**: `default_args["retries"]`, exercised in the failure demo (3 total attempts before failing).
- **Tags**: filterable in the Airflow UI.
- **Scheduling**: `@daily` cron-style schedule vs. Phase 2's manual-only DAG.
- **Unit tests** (Phase 3+/4): individual functions (`clean_data`, `validate_data`, etc.) are plain Python functions, testable in isolation with pytest without a running Airflow instance.
- **Integration tests** (Phase 7): triggering the DAG against a live Airflow instance and asserting the run succeeds, as done manually in this phase.
- **Intentional failure / rollback** (Phase 3 demo, later formalized): the `ENABLE_INTENTIONAL_FAILURE` flag already proves the failure path; later phases will formalize "rollback" as redeploying a previous known-good DAG version via Git tags.

## Likely Viva Questions

1. Why does `clean_data` exist as a separate task from `validate_data` instead of combining them?
2. What is XCom, and why can't tasks just share a Python variable directly?
3. Why does `process_data` never run when `validate_data` fails, even though it doesn't call `validate_data` directly?
4. What is the difference between a task's `state=failed` and `state=upstream_failed`?
5. Why does `retries=2` result in 3 total execution attempts, not 2?
6. Why was an environment variable used to trigger the intentional failure instead of hardcoding `raise Exception(...)` into the code and later removing it?
7. What would happen if `schedule="@daily"` were used with `catchup=True` instead of `False`?
8. Why is `PythonOperator` a reasonable choice here versus, say, `BashOperator`?
9. What does "acyclic" in Directed Acyclic Graph actually forbid, concretely, in this DAG's structure?
10. How does the Airflow UI know a task failed — what is it actually reading to render that red cell?
