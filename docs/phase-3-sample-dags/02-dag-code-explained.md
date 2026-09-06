# Phase 3 — DAG Code Walkthrough

File: `dags/sales_data_pipeline.py`

| Code | What it does | Why it exists |
|---|---|---|
| `ENABLE_INTENTIONAL_FAILURE = os.environ.get(...)` | Reads an env var to decide whether `validate_data` should deliberately raise an error | Lets us demonstrate a controlled failure later without editing/breaking the pipeline logic itself — flip an env var, rerun, flip it back |
| `default_args = {"owner": ..., "retries": 2, "retry_delay": ...}` | Applied to every task in the DAG unless overridden per-task | Avoids repeating `retries=2` five times; centralizes fault-tolerance policy |
| `fetch_data()` | Produces a hardcoded list simulating raw records pulled from a source system (including one deliberately messy record with `amount: None`) | Stands in for a real API/DB call; the messy record exists so `clean_data` has something real to do |
| `context["ti"].xcom_push(...)` / `xcom_pull(...)` | Airflow's XCom ("cross-communication") mechanism — lets one task pass data forward to the next | Tasks run as separate subprocesses with no shared memory; XCom is the sanctioned way to pass small data between them |
| `clean_data()` | Filters out records with `amount is None` | Demonstrates a distinct "cleaning" responsibility separate from validation |
| `validate_data()` | Enforces business rules (data must exist, amounts non-negative); raises `ValueError` on failure | This is the task intentionally broken for the Phase 3 failure demo — the natural place a real pipeline would catch bad data |
| `process_data()` | Aggregates cleaned+validated records into per-product totals | The actual business-logic step |
| `store_result()` | Prints the final totals (stand-in for writing to a DB/file/report) | Terminal step — every pipeline needs a "where does the output go" task |
| `schedule="@daily", catchup=False, tags=[...]` | Declares a realistic daily schedule with no historical backfill, tagged for the UI | Shows what a real production schedule looks like, distinct from Phase 2's manual-only sanity check DAG |
| `t1_fetch >> t2_clean >> t3_validate >> t4_process >> t5_store` | Declares the five dependencies as one linear chain | This single line is the DAG's shape — visually obvious in code |
