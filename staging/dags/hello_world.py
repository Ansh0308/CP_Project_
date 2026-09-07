from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="hello_world",
    description="Phase 2 sanity-check DAG: proves Airflow can parse and schedule DAGs",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["phase-2", "sanity-check"],
) as dag:
    say_hello = BashOperator(
        task_id="say_hello",
        bash_command="echo 'Hello from Airflow running in Docker Compose'",
    )
