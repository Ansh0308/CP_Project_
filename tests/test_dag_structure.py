"""Structural unit tests for every DAG in dags/.

These tests protect the DAG's *shape* (existence, ids, task graph,
configuration) - distinct from Phase 6's CI validation, which only
proves a DAG file is well-formed enough to parse. A DAG can pass
every Phase 6 check and still have the wrong number of tasks, a
disconnected task, a missing retry policy, or a dependency wired
backwards - these tests catch exactly that class of regression.
"""
from airflow.exceptions import AirflowDagCycleException
from airflow.models import DagBag

ALLOWED_OPERATORS = {"PythonOperator", "BashOperator"}

EXPECTED_DAG_IDS = {"hello_world", "sales_data_pipeline"}

SALES_PIPELINE_EXPECTED_TASKS = [
    "fetch_data",
    "clean_data",
    "validate_data",
    "process_data",
    "store_result",
]


# ---------------------------------------------------------------------------
# DAG existence
# ---------------------------------------------------------------------------


def test_no_import_errors(dagbag: DagBag):
    """Every DAG file must import cleanly (mirrors CI layer 2, re-asserted
    here because these tests must never build on a DAG that failed to load)."""
    assert dagbag.import_errors == {}, f"DAG import failures: {dagbag.import_errors}"


def test_expected_dags_exist(dagbag: DagBag):
    """Both project DAGs must actually be present in the DagBag."""
    assert EXPECTED_DAG_IDS.issubset(set(dagbag.dags.keys()))


# ---------------------------------------------------------------------------
# DAG ID
# ---------------------------------------------------------------------------


def test_sales_pipeline_dag_id(sales_dag):
    assert sales_dag.dag_id == "sales_data_pipeline"


def test_hello_world_dag_id(hello_world_dag):
    assert hello_world_dag.dag_id == "hello_world"


# ---------------------------------------------------------------------------
# Task count and task IDs
# ---------------------------------------------------------------------------


def test_sales_pipeline_task_count(sales_dag):
    assert len(sales_dag.tasks) == 5


def test_sales_pipeline_task_ids(sales_dag):
    assert set(sales_dag.task_ids) == set(SALES_PIPELINE_EXPECTED_TASKS)


def test_hello_world_task_count(hello_world_dag):
    assert len(hello_world_dag.tasks) == 1


def test_hello_world_task_ids(hello_world_dag):
    assert hello_world_dag.task_ids == ["say_hello"]


# ---------------------------------------------------------------------------
# Dependency structure
# ---------------------------------------------------------------------------


def test_sales_pipeline_dependency_chain(sales_dag):
    """Verifies the exact linear chain: fetch -> clean -> validate -> process -> store."""
    for upstream_id, downstream_id in zip(
        SALES_PIPELINE_EXPECTED_TASKS, SALES_PIPELINE_EXPECTED_TASKS[1:]
    ):
        upstream_task = sales_dag.get_task(upstream_id)
        assert downstream_id in upstream_task.downstream_task_ids, (
            f"Expected '{upstream_id}' >> '{downstream_id}', "
            f"but downstream is {upstream_task.downstream_task_ids}"
        )

    first_task = sales_dag.get_task(SALES_PIPELINE_EXPECTED_TASKS[0])
    last_task = sales_dag.get_task(SALES_PIPELINE_EXPECTED_TASKS[-1])
    assert first_task.upstream_task_ids == set()
    assert last_task.downstream_task_ids == set()


# ---------------------------------------------------------------------------
# No cycles
# ---------------------------------------------------------------------------


def test_sales_pipeline_has_no_cycles(sales_dag):
    """Airflow refuses to build a cyclic DAG at parse time, so a real cycle
    would already show up as an import error - this test re-asserts it
    explicitly via the DAG's own topological sort as a second safety net."""
    try:
        sales_dag.topological_sort()
    except AirflowDagCycleException:
        assert False, "sales_data_pipeline contains a cycle"


def test_hello_world_has_no_cycles(hello_world_dag):
    try:
        hello_world_dag.topological_sort()
    except AirflowDagCycleException:
        assert False, "hello_world contains a cycle"


# ---------------------------------------------------------------------------
# No orphan tasks
# ---------------------------------------------------------------------------


def test_sales_pipeline_has_no_orphan_tasks(sales_dag):
    """In a multi-task DAG, every task must connect to at least one other
    task - a task with zero upstream AND zero downstream links is dead
    weight that never actually joins the pipeline."""
    for task in sales_dag.tasks:
        is_connected = bool(task.upstream_task_ids) or bool(task.downstream_task_ids)
        assert is_connected, f"Task '{task.task_id}' is disconnected from the DAG"


# ---------------------------------------------------------------------------
# Required operators
# ---------------------------------------------------------------------------


def test_sales_pipeline_uses_only_allowed_operators(sales_dag):
    for task in sales_dag.tasks:
        assert task.task_type in ALLOWED_OPERATORS, (
            f"Task '{task.task_id}' uses disallowed operator '{task.task_type}'"
        )


def test_hello_world_uses_only_allowed_operators(hello_world_dag):
    for task in hello_world_dag.tasks:
        assert task.task_type in ALLOWED_OPERATORS


# ---------------------------------------------------------------------------
# Retries
# ---------------------------------------------------------------------------


def test_sales_pipeline_has_retries_configured(sales_dag):
    retries = (sales_dag.default_args or {}).get("retries")
    assert retries is not None and retries >= 1


def test_hello_world_has_retries_configured(hello_world_dag):
    retries = (hello_world_dag.default_args or {}).get("retries")
    assert retries is not None and retries >= 1


# ---------------------------------------------------------------------------
# Required configuration
# ---------------------------------------------------------------------------


def test_sales_pipeline_required_configuration(sales_dag):
    assert sales_dag.description, "DAG must have a non-empty description"
    assert sales_dag.catchup is False, "DAG must explicitly disable catchup"
    assert len(sales_dag.tags) >= 2, "DAG must declare at least 2 tags"
    assert "business-pipeline" in sales_dag.tags
    sla = (sales_dag.default_args or {}).get("sla")
    assert sla is not None, "business-pipeline DAGs must declare an SLA"


def test_hello_world_required_configuration(hello_world_dag):
    assert hello_world_dag.description
    assert hello_world_dag.catchup is False
    assert len(hello_world_dag.tags) >= 2
