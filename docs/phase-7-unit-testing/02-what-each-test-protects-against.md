# Phase 7 — What Each Test Protects Against

## `tests/test_dag_structure.py`

| Test | Protects against |
|---|---|
| `test_no_import_errors` | A DAG file broken badly enough that it can't even load — the base assumption every other test relies on |
| `test_expected_dags_exist` | A DAG silently disappearing (renamed, deleted, moved) without anyone noticing |
| `test_*_dag_id` | The `dag_id` drifting from what deployment/scheduling tooling expects it to be |
| `test_*_task_count` | A task being accidentally added or removed during a refactor |
| `test_*_task_ids` | A task being renamed without updating anything that depends on its exact ID (XCom keys, external triggers, monitoring) |
| `test_sales_pipeline_dependency_chain` | Tasks being wired in the wrong order — e.g. `process_data` running before `validate_data`, silently processing unvalidated data |
| `test_*_has_no_cycles` | A dependency loop that would make the DAG un-schedulable (a second safety net beyond Airflow's own import-time check) |
| `test_sales_pipeline_has_no_orphan_tasks` | A task accidentally left disconnected from the pipeline — it would exist but never actually run in sequence with the others |
| `test_*_uses_only_allowed_operators` | An unapproved/deprecated operator being introduced without review |
| `test_*_has_retries_configured` | A DAG shipping with no fault tolerance — the first transient error would fail the pipeline permanently |
| `test_*_required_configuration` | A business-critical DAG missing its description, an accidental backfill (`catchup=True`), missing tags, or (for `business-pipeline` DAGs) missing SLA |

## `tests/test_task_logic.py`

| Test | Protects against |
|---|---|
| `test_fetch_data_pushes_raw_records` | The data source simulation silently returning nothing or the wrong shape |
| `test_clean_data_drops_records_with_missing_amount` | A regression in the cleaning filter — e.g. keeping records that should be dropped |
| `test_validate_data_passes_through_valid_records` | Validation incorrectly rejecting good data |
| `test_validate_data_raises_on_empty_dataset` | Validation silently accepting an empty dataset instead of failing loudly |
| `test_validate_data_raises_on_negative_amount` | Validation silently accepting a negative amount instead of catching a real data-quality problem |
| `test_process_data_aggregates_totals_per_product` | An aggregation bug — the exact kind of business-logic error CI's structural checks can never catch |
| `test_store_result_prints_totals` | The final output step silently producing wrong or incomplete results |
| `test_full_pipeline_logic_end_to_end_with_mocked_context` | A break in how the XCom hand-offs chain together across all five functions, even though each function passes its own isolated test |

## Why These Tests Are Useful

Every test here runs in well under a second, requires no Airflow scheduler, no database, and no network access — so they can run on every commit, every PR, as many times as needed, at zero marginal cost. They catch an entire category of mistake (wrong business logic, wrong DAG shape) that Phase 6's CI validation was never designed to catch, and they catch it at the moment a developer opens a PR — not after a real Airflow run fails in staging or production.
