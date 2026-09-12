# Phase 7 — Summary and Viva Questions

## What We Built

- `tests/conftest.py`: session-scoped `DagBag` fixture, per-DAG fixtures (`sales_dag`, `hello_world_dag`), and `MockTaskInstance` — a fake XCom backend so tests never touch a real database.
- `tests/test_dag_structure.py`: 18 tests covering DAG existence, DAG ID, task count, task IDs, dependency structure, no cycles, no orphan tasks, allowed operators, retries, and required configuration for both project DAGs.
- `tests/test_task_logic.py`: 8 tests covering each of `sales_data_pipeline`'s task callables in isolation (including `validate_data`'s two failure paths), plus one end-to-end test chaining all five functions through a shared mocked context.
- Wired pytest into `.github/workflows/ci.yml` as **Layer 4**, after the existing syntax/import/lint layers from Phase 6.

## Why We Built It This Way

- **DagBag-based fixtures, not hand-rolled DAG construction** — tests exercise the exact same DAG objects Airflow's own scheduler would build, so a test passing means something real, not an artifact of a simplified test-only DAG definition.
- **A hand-rolled `MockTaskInstance` instead of a mocking library's generic `Mock()`** — XCom's push/pull contract is simple enough that a tiny real (if fake) implementation is clearer to read than a generic mock's call-assertion API, while still fully satisfying "never touch the real database."
- **Structural tests and logic tests in separate files** — mirrors the conceptual split explained in `01-concepts.md`: one file asks "is the DAG shaped correctly," the other asks "does the code inside it work correctly."
- **Layer 4 placed last in CI** — cheapest/fastest checks (syntax, import, lint) still run first, so a trivial mistake fails in seconds without waiting for the full test suite, consistent with Phase 6's fail-fast design.

## What Is Still Not Built

- No integration tests (triggering a real DAG run against a live Airflow instance) — that is Phase 8+ territory per the project roadmap.
- No staging or production deployment automation.
- No tests for `hello_world`'s task logic (it has no meaningful business logic to test beyond what structural tests already cover).
- The two gaps Copilot flagged in Phase 6 (staging/production DAG drift, SLA type-checking) remain open, as decided in that phase.

## Verification

See `03-verification.md` for full detail. Summary: valid DAG produced 26/26 passing tests in 0.41s; three distinct failure scenarios (broken dependency, missing task, incorrect configuration — demonstrated twice, once caught by Layer 3 and once isolated to Layer 4) were each pushed, observed failing at exactly the expected test(s), and then reverted; final state confirmed identical to the pre-demo valid DAG and green across all four CI layers.

## Troubleshooting

See `04-troubleshooting-log.md`. Headline finding: Airflow cannot run natively on Windows at all (confirmed via two independent hard blockers — an unsatisfiable SQLite path format requirement, and a hard dependency on the POSIX-only `fcntl` module) — this is a genuine platform limitation, not a project misconfiguration, and GitHub Actions (Linux) was used as the authoritative test-running environment as a result.

## Viva Questions

1. Why can a DAG pass every Phase 6 CI check and still fail a Phase 7 unit test? Give a concrete example from this project.
2. What exactly does `MockTaskInstance` stand in for, and why must a unit test never use the real thing?
3. Why are `test_dag_structure.py` and `test_task_logic.py` kept as separate files rather than combined?
4. Explain, using `test_validate_data_raises_on_negative_amount`, how a test can assert that code is *supposed* to fail.
5. Why did removing the DAG's `sla` get caught by Layer 3 before pytest even ran, while flipping `catchup` was caught only by pytest? What does that reveal about how the four CI layers relate to each other?
6. Why is `dags/` added to `sys.path` in `conftest.py` instead of turning `dags/` into a proper Python package with an `__init__.py`?
7. What two independent, unrelated reasons make it impossible to run this project's Airflow-based tests on a bare Windows Python installation?
8. Why was `pytest==7.4.4` specifically chosen, rather than the newest available pytest release?
9. What would `test_sales_pipeline_has_no_orphan_tasks` actually catch that `test_sales_pipeline_task_count` would not?
10. If a new task were added to `sales_data_pipeline` tomorrow, list every test in this suite that would need to be updated, and explain why each one is affected.
