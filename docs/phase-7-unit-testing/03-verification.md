# Phase 7 — Verification

## Valid DAG -> Tests Pass

CI run #8 (PR #3, commit `6c7f104`): **26 passed in 0.41s**, all four CI layers (syntax, import, lint, pytest) green.

## Broken Dependency -> Tests Fail

Commit `1635f10`: swapped `validate_data` and `process_data` in the chain (`fetch -> clean -> process -> validate -> store`). Still a valid, importable DAG — layers 1-3 passed. Result:
```
tests/test_dag_structure.py::test_sales_pipeline_dependency_chain FAILED
```
All other 25 tests still passed — the failure was fully isolated to the one test checking exact dependency order.

## Missing Task -> Tests Fail

Commit `5ca1c01`: removed the `process_data` task entirely, wiring `validate_data` directly to `store_result`. Still a valid, importable 4-task DAG — layers 1-3 passed. Result:
```
tests/test_dag_structure.py::test_sales_pipeline_task_count FAILED    (assert 4 == 5)
tests/test_dag_structure.py::test_sales_pipeline_task_ids FAILED
tests/test_dag_structure.py::test_sales_pipeline_dependency_chain FAILED
```
Three related tests failed together, each describing a different facet of the same real problem — task count, task identity, and dependency shape.

## Incorrect Configuration -> Tests Fail

Two variants were demonstrated:

1. **Commit `2c675a1`**: removed the required `sla` from `default_args` on the `business-pipeline`-tagged DAG. This was actually caught by **Layer 3** (`scripts/ci/lint_dags.py`) before pytest even ran, since both layers enforce the same SLA rule — the pipeline fails fast at the first layer that catches a problem.
2. **Commit `9fc7c3e`**: to isolate a configuration failure that *only* pytest checks, flipped `catchup` to `True` (a rule Layer 3's script does not check at all). Layers 1-3 passed; pytest failed cleanly:
   ```
   tests/test_dag_structure.py::test_sales_pipeline_required_configuration FAILED
   AssertionError: DAG must explicitly disable catchup
   assert True is False
    +  where True = <DAG: sales_data_pipeline>.catchup
   ```

## Restoration

Commit `ddb0e61` restored `dags/sales_data_pipeline.py` to be byte-for-byte identical to `main`'s valid version (confirmed via `git diff main` showing no differences). Final CI run on this commit: **all 4 layers green**, PR #3 shows "Ready to merge".

## Local Execution Attempted (and Why CI Was Used as the Authoritative Run)

This session attempted to run pytest locally in three ways, in order:
1. **Docker Compose** (the project's established local environment since Phase 2) — Docker Desktop was unavailable/hung for an extended period this session (see troubleshooting log).
2. **A native Windows Python 3.11 virtual environment** — got as far as installing `apache-airflow==2.9.3` successfully, but hit two separate, confirmed platform incompatibilities (Airflow's SQLite path validation rejects Windows drive-letter paths; `airflow.operators.python` imports the POSIX-only `fcntl` module, which does not exist on Windows at all). This is a hard blocker, not a configuration mistake — Airflow's own startup warning states it is not supported natively on Windows.
3. **GitHub Actions (Linux runners)** — used as the actual "run tests" verification for this phase, since it is a genuine Linux environment (Airflow's supported platform) and produces real, reproducible pass/fail evidence, shown throughout this document.
