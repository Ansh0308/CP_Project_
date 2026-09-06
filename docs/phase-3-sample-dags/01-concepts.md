# Phase 3 — Core Concepts

1. **DAG (Directed Acyclic Graph)** — a Python-defined workflow describing a set of tasks and the order they must run in. "Acyclic" means no task can depend on itself, directly or through a loop — the workflow only ever moves forward.

2. **Task** — a single unit of work inside a DAG (e.g. "fetch data"). Each task run for a specific DAG execution is a "task instance," with its own status (queued, running, success, failed, retrying, upstream_failed).

3. **Operator** — a template/class defining what kind of work a task performs. A task is an instantiated operator. This DAG uses `PythonOperator` throughout (runs a Python function) — realistic for fetch/clean/validate/process/store business logic.

4. **Task dependencies** — the edges of the DAG graph, declared with `>>`. They tell the scheduler "don't start B until A has succeeded." This is how a multi-step pipeline enforces its order.

5. **DAG scheduling** — the `schedule` parameter tells Airflow when to automatically create new DAG runs (daily, hourly, cron, or `None` for manual-only). `sales_data_pipeline` uses `schedule="@daily"` to demonstrate a realistic production schedule (Phase 2's `hello_world` used `None` as a bare sanity check).

6. **Retries** — per-task fault tolerance: if a task fails, Airflow can automatically re-attempt it a configured number of times with a delay in between (`retries`, `retry_delay`) before marking it failed. Useful for transient issues, not for a task that is fundamentally broken (as the failure demo shows — retries do not help a real validation error).

7. **DAG tags** — labels shown in the UI (`phase-3`, `business-pipeline`, `sales`) purely for organization/filtering — no functional effect on execution.

8. **How Airflow executes the DAG** — the Scheduler parses the DAG file, sees which tasks are ready to run (all upstream dependencies succeeded), and hands them to the Executor (`LocalExecutor`), which runs each task as a subprocess. Task state transitions are written to the Postgres metadata DB, and the Webserver reads that same DB to render the UI live.
