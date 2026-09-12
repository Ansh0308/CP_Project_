"""Shared pytest fixtures for DAG unit tests.

Loads every DAG in dags/ exactly once per test session via Airflow's
own DagBag - the same mechanism the real scheduler uses - so every
test file works against the actual, constructed DAG objects rather
than re-parsing source text by hand.
"""
import os
import sys

import pytest
from airflow.models import DagBag

DAGS_FOLDER = "dags"

# dags/ is a plain folder (not a package, matching Airflow convention),
# so add it to sys.path directly to let tests import DAG modules as
# top-level modules, e.g. `from sales_data_pipeline import clean_data`.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", DAGS_FOLDER))


@pytest.fixture(scope="session")
def dagbag() -> DagBag:
    return DagBag(dag_folder=DAGS_FOLDER, include_examples=False)


@pytest.fixture()
def sales_dag(dagbag: DagBag):
    dag = dagbag.get_dag("sales_data_pipeline")
    assert dag is not None, "sales_data_pipeline DAG failed to load"
    return dag


@pytest.fixture()
def hello_world_dag(dagbag: DagBag):
    dag = dagbag.get_dag("hello_world")
    assert dag is not None, "hello_world DAG failed to load"
    return dag


class MockTaskInstance:
    """A lightweight stand-in for Airflow's real TaskInstance/XCom.

    In production, xcom_push/xcom_pull are backed by the Airflow
    metadata database. A unit test must never touch that real
    database (slow, stateful, and not what we're testing) - so this
    fake keeps XCom values in a plain in-memory dict instead.
    """

    def __init__(self):
        self._xcom_data: dict[str, object] = {}

    def xcom_push(self, key: str, value: object) -> None:
        self._xcom_data[key] = value

    def xcom_pull(self, key: str, task_ids: str | None = None) -> object:
        return self._xcom_data.get(key)


@pytest.fixture()
def mock_context():
    """A fake Airflow task context built around MockTaskInstance."""
    return {"ti": MockTaskInstance()}
