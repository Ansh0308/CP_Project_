from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "retries": 1,
    "retry_delay": timedelta(seconds=30),
}

with DAG(
    dag_id="hello_world",
    description="Phase 2 sanity-check DAG: proves Airflow can parse and schedule DAGs",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["phase-2", "sanity-check"],
) as dag:
    say_hello = BashOperator(
        task_id="say_hello",
        bash_command="echo 'Hello from Airflow running in Docker Compose'",

