"""Sales data pipeline: Fetch -> Clean -> Validate -> Process -> Store.

A small, realistic business DAG used to demonstrate task dependencies,
operators, retries, tags, scheduling, unit testing, integration testing,
and (via ENABLE_INTENTIONAL_FAILURE) controlled failure/rollback.
"""
from __future__ import annotations

import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

# Toggle used only for the Phase 3 failure demonstration (see docs/phase-3).
# Left as an env var (not a hardcoded True) so the failure can be turned on
# and back off without editing the pipeline logic itself.
ENABLE_INTENTIONAL_FAILURE = os.environ.get("ENABLE_INTENTIONAL_FAILURE", "false") == "true"

default_args = {
    "owner": "airflow",
    "retries": 2,
    "retry_delay": timedelta(seconds=30),
}


def fetch_data(**context):
    """Simulate pulling raw sales records from a source system."""
    raw_records = [
        {"id": 1, "product": "Widget", "amount": 100},
        {"id": 2, "product": "Gadget", "amount": 250},
        {"id": 3, "product": "Widget", "amount": None},  # missing amount, cleaned later
    ]
    context["ti"].xcom_push(key="raw_records", value=raw_records)


def clean_data(**context):
    """Drop records with missing/invalid fields."""
    raw_records = context["ti"].xcom_pull(key="raw_records", task_ids="fetch_data")
    cleaned = [r for r in raw_records if r.get("amount") is not None]
    context["ti"].xcom_push(key="cleaned_records", value=cleaned)


def validate_data(**context):
    """Fail loudly if cleaning left us with no usable data or a negative amount."""
    cleaned = context["ti"].xcom_pull(key="cleaned_records", task_ids="clean_data")

    if ENABLE_INTENTIONAL_FAILURE:
        # Deliberate, controlled failure for the Phase 3 demo: proves Airflow
        # surfaces validation errors clearly and stops downstream tasks.
        raise ValueError("Intentional failure: negative amount detected in dataset")

    if not cleaned:
        raise ValueError("Validation failed: no valid records after cleaning")
    if any(r["amount"] < 0 for r in cleaned):
        raise ValueError("Validation failed: negative amount detected")

    context["ti"].xcom_push(key="validated_records", value=cleaned)


def process_data(**context):
    """Aggregate total sales amount per product."""
    validated = context["ti"].xcom_pull(key="validated_records", task_ids="validate_data")
    totals: dict[str, float] = {}
    for record in validated:
        totals[record["product"]] = totals.get(record["product"], 0) + record["amount"]
    context["ti"].xcom_push(key="totals", value=totals)


def store_result(**context):
    """Simulate persisting the final result (e.g. to a database or file)."""
    totals = context["ti"].xcom_pull(key="totals", task_ids="process_data")
    print(f"Storing final sales totals: {totals}")


with DAG(
    dag_id="sales_data_pipeline",
    description="Fetch, clean, validate, process, and store daily sales data",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["phase-3", "business-pipeline", "sales"],
) as dag:

    t1_fetch = PythonOperator(task_id="fetch_data", python_callable=fetch_data)
    t2_clean = PythonOperator(task_id="clean_data", python_callable=clean_data)
    t3_validate = PythonOperator(task_id="validate_data", python_callable=validate_data)
    t4_process = PythonOperator(task_id="process_data", python_callable=process_data)
    t5_store = PythonOperator(task_id="store_result", python_callable=store_result)

    t1_fetch >> t2_clean >> t3_validate >> t4_process >> t5_store
