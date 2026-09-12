# Phase 6 — Project DAG Lint Rules

These are this project's own rules, enforced by `scripts/ci/lint_dags.py` (CI validation layer 3). They are not generic Airflow requirements — Airflow itself does not care about any of these — they exist so that every DAG in this repository stays consistent and safe to operate.

## 1. Naming convention

- `dag_id` must be **identical** to the DAG's filename, minus `.py` (e.g. `sales_data_pipeline.py` → `dag_id="sales_data_pipeline"`).
- `dag_id` must be **snake_case**: starts with a lowercase letter, then only lowercase letters, digits, and underscores.

**Why:** if `dag_id` and filename can drift apart, finding "which file defines this DAG" becomes a search problem instead of a lookup. Snake_case keeps naming consistent with Python module-naming conventions and Airflow's own examples.

## 2. Mandatory tags

- Every DAG must declare **at least 2 tags**.

**Why:** tags are how DAGs are filtered/organized in the Airflow UI. A DAG with zero or one tag is effectively unclassified — this project uses tags to signal phase/category (e.g. `phase-3`, `business-pipeline`, `sales`).

## 3. Required retries

- `default_args` must set `retries` to **1 or more**.

**Why:** a task with no retry policy fails permanently on the first transient error (a flaky network call, a momentary resource limit) — real pipelines need at least one automatic retry before requiring human intervention. This applies to every DAG, including the Phase 2 `hello_world` sanity-check DAG (which was updated in this phase to add `retries: 1` in order to comply).

## 4. Required SLA where applicable

- Any DAG tagged **`business-pipeline`** must define an `sla` (a `timedelta`) in `default_args`.

**Why:** "where applicable" means this rule only applies to DAGs the project has explicitly classified as business-critical via the `business-pipeline` tag — a one-off sanity-check DAG like `hello_world` has no meaningful SLA to define, but `sales_data_pipeline` (tagged `business-pipeline`) represents a real workflow whose completion time matters, so it must declare one. `sales_data_pipeline` was updated in this phase to add `"sla": timedelta(hours=1)` in order to comply.

## Enforcement

All four rules are checked in `scripts/ci/lint_dags.py`, which re-uses the DAG objects already successfully imported by layer 2 (`check_dag_imports.py`) rather than re-parsing source text — since layer 2 already proved the files import safely, inspecting the real constructed `DAG` objects (`dag.tags`, `dag.default_args`, `dag.dag_id`, `dag.fileloc`) is simpler and more accurate than re-deriving the same information from raw AST.
