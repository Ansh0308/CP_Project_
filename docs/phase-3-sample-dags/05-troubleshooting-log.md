# Phase 3 — Troubleshooting Log

## Issue: `DagNotFound` immediately after adding the DAG file

**Symptom:**
```
airflow.exceptions.DagNotFound: Dag id sales_data_pipeline not found in DagModel
```
raised by both `airflow dags unpause` and `airflow dags trigger` right after the new DAG file was created.

**Diagnosis:** `airflow dags list-import-errors` showed no parse errors, meaning the file itself was valid Python/Airflow code. The issue was timing: the Scheduler's DAG file processor parses files on a polling loop (not instantly on file save), so the DAG did not yet exist as a row in the `DagModel` table when the commands were first run.

**Fix:** waited ~20-30 seconds, re-ran `airflow dags list`, confirmed `sales_data_pipeline` was now listed, then re-ran `unpause`/`trigger` successfully.

**Lesson for the project:** any automation (later, GitHub Actions deploy jobs) that deploys a DAG and then immediately tries to trigger/query it must account for this parsing delay — either by polling `airflow dags list` until the DAG appears, or by accepting an initial short wait.

## Issue: DAG run stuck in `queued` state

**Symptom:** after triggering, `airflow dags list-runs` kept showing `state: queued` with no tasks progressing for over 30 seconds.

**Diagnosis:** `airflow dags details sales_data_pipeline` revealed `is_paused: True` — an earlier `unpause` call had run before the DAG was registered (see issue above) and silently no-op'd ("No paused DAGs were found"), leaving the DAG still paused. A paused DAG's queued runs do not get their tasks scheduled.

**Fix:** re-ran `airflow dags unpause sales_data_pipeline` after confirming registration; it returned `is_paused: False`, and the queued run began executing within seconds.
