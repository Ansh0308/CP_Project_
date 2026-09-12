"""Unit tests for the individual Python callables behind sales_data_pipeline's
tasks - the actual business logic, tested in isolation with a mocked
Airflow context so no real Airflow scheduler, metadata database, or
external system is ever touched.

Note on mocking scope: this project's DAGs do not yet call a real
external API or database (fetch_data simulates a source system with a
hardcoded list, by design from Phase 3). The nearest real dependency
these task functions have is Airflow's own TaskInstance/XCom
mechanism, which in production is backed by the metadata database -
so that is what we mock here (see MockTaskInstance in conftest.py).
If a real external API or DB call is ever added to a DAG, it would be
mocked the same way: with unittest.mock.patch targeted at that
specific call, never by letting the test reach the real network/DB.
"""
from unittest.mock import patch

from sales_data_pipeline import (
    clean_data,
    fetch_data,
    process_data,
    store_result,
    validate_data,
)


def test_fetch_data_pushes_raw_records(mock_context):
    fetch_data(**mock_context)
    raw = mock_context["ti"].xcom_pull(key="raw_records")
    assert raw is not None
    assert len(raw) == 3


def test_clean_data_drops_records_with_missing_amount(mock_context):
    mock_context["ti"].xcom_push(
        key="raw_records",
        value=[
            {"id": 1, "product": "Widget", "amount": 100},
            {"id": 2, "product": "Gadget", "amount": None},
        ],
    )
    clean_data(**mock_context)
    cleaned = mock_context["ti"].xcom_pull(key="cleaned_records")
    assert cleaned == [{"id": 1, "product": "Widget", "amount": 100}]


def test_validate_data_passes_through_valid_records(mock_context):
    mock_context["ti"].xcom_push(
        key="cleaned_records",
        value=[{"id": 1, "product": "Widget", "amount": 100}],
    )
    validate_data(**mock_context)
    validated = mock_context["ti"].xcom_pull(key="validated_records")
    assert validated == [{"id": 1, "product": "Widget", "amount": 100}]


def test_validate_data_raises_on_empty_dataset(mock_context):
    mock_context["ti"].xcom_push(key="cleaned_records", value=[])
    try:
        validate_data(**mock_context)
        assert False, "Expected ValueError for empty dataset"
    except ValueError as exc:
        assert "no valid records" in str(exc)


def test_validate_data_raises_on_negative_amount(mock_context):
    mock_context["ti"].xcom_push(
        key="cleaned_records",
        value=[{"id": 1, "product": "Widget", "amount": -50}],
    )
    try:
        validate_data(**mock_context)
        assert False, "Expected ValueError for negative amount"
    except ValueError as exc:
        assert "negative amount" in str(exc)


def test_process_data_aggregates_totals_per_product(mock_context):
    mock_context["ti"].xcom_push(
        key="validated_records",
        value=[
            {"id": 1, "product": "Widget", "amount": 100},
            {"id": 2, "product": "Widget", "amount": 50},
            {"id": 3, "product": "Gadget", "amount": 250},
        ],
    )
    process_data(**mock_context)
    totals = mock_context["ti"].xcom_pull(key="totals")
    assert totals == {"Widget": 150, "Gadget": 250}


def test_store_result_prints_totals(mock_context):
    """Mocks the 'destination' of store_result (currently stdout, standing
    in for a future real database/report write) so the test can assert
    exactly what would be persisted, without depending on captured
    stdout formatting."""
    mock_context["ti"].xcom_push(key="totals", value={"Widget": 100, "Gadget": 250})

    with patch("builtins.print") as mock_print:
        store_result(**mock_context)

    printed_lines = [call.args[0] for call in mock_print.call_args_list]
    assert any("Widget" in line and "100" in line and "Gadget" in line and "250" in line
                for line in printed_lines)


def test_full_pipeline_logic_end_to_end_with_mocked_context(mock_context):
    """Chains all five callables through one shared mocked context, proving
    the XCom hand-offs work together exactly as they would inside a real
    DAG run - without needing a real DAG run."""
    fetch_data(**mock_context)
    clean_data(**mock_context)
    validate_data(**mock_context)
    process_data(**mock_context)

    with patch("builtins.print") as mock_print:
        store_result(**mock_context)

    printed_lines = [call.args[0] for call in mock_print.call_args_list]
    assert any("Widget" in line and "Gadget" in line for line in printed_lines)
