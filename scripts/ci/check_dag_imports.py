"""CI validation layer 2: Airflow DAG import validation.

Loads every DAG file in dags/ the same way the real Airflow scheduler
does (via DagBag) and fails if any file raises an import error -
catching mistakes that plain Python syntax checking cannot, such as
referencing a missing Airflow operator, a bad import path, or a
DAG-construction error that only surfaces once Airflow parses the file.
"""
import sys

from airflow.models import DagBag

DAGS_FOLDER = "dags"


def main() -> int:
    dagbag = DagBag(dag_folder=DAGS_FOLDER, include_examples=False)

    if dagbag.import_errors:
        print("Airflow DAG import validation FAILED.")
        print(f"{len(dagbag.import_errors)} file(s) failed to import:\n")
        for filename, error in dagbag.import_errors.items():
            print(f"--- {filename} ---")
            print(error)
            print()
        return 1

    if not dagbag.dags:
        print("No DAGs were found in the dags/ folder - nothing to validate.")
        return 1

    print(f"Airflow DAG import validation passed: {len(dagbag.dags)} DAG(s) imported cleanly.")
    for dag_id in sorted(dagbag.dags):
        print(f"  - {dag_id}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
