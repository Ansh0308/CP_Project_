# Phase 3 — Verification (Normal Run)

## Commands Run

```bash
docker compose exec airflow-scheduler airflow dags list-import-errors
docker compose exec airflow-scheduler airflow dags unpause sales_data_pipeline
docker compose exec airflow-scheduler airflow dags trigger sales_data_pipeline
docker compose exec airflow-scheduler airflow dags list-runs -d sales_data_pipeline
docker compose exec airflow-scheduler airflow tasks states-for-dag-run sales_data_pipeline <run_id>
```

## Results

- `list-import-errors` → `No data found` (clean parse, no syntax errors).
- Manual trigger run `manual__2026-09-06T10:04:09+00:00` → **success**.
- The automatically-created `@daily` run `scheduled__2026-09-05T00:00:00+00:00` (created on unpause) → **success**.
- All 5 tasks (`fetch_data`, `clean_data`, `validate_data`, `process_data`, `store_result`) showed green in both the Grid and Graph views of the UI.
- `store_result` task log confirmed correct business logic end-to-end:
  ```
  Storing final sales totals: {'Widget': 100, 'Gadget': 250}
  ```
  This proves the record with `amount: None` from `fetch_data` was correctly dropped by `clean_data`, and the remaining two records were correctly aggregated by `process_data`.

## Note on a Race Condition Hit During Verification

The first `airflow dags unpause` + `airflow dags trigger` attempt failed with `DagNotFound: Dag id sales_data_pipeline not found in DagModel`. This happened because the scheduler's file-parsing loop had not yet registered the newly-added DAG file into the metadata database at the moment those commands ran. Waiting ~20-30 seconds for the next parse cycle and re-running `airflow dags list` confirmed registration, after which `unpause` and `trigger` worked normally. This is expected Airflow behavior, not a bug — DAG files are picked up on a polling interval, not instantly.
