"""CI validation layer 3: custom project DAG lint rules.

These rules are specific to this project (not generic Airflow checks)
and are documented in docs/phase-6-ci-validation/03-lint-rules.md.
Each DAG that Airflow successfully imported is checked against:

  1. Naming convention: dag_id must equal its filename (without .py)
     and be snake_case (lowercase letters, digits, underscores only).
  2. Mandatory tags: at least 2 tags must be declared.
  3. Required retries: default_args must set retries >= 1.
  4. Required SLA where applicable: any DAG tagged "business-pipeline"
     must define an sla in default_args.

This intentionally reuses DagBag (rather than re-parsing with ast)
because layer 2 already proved these files import safely - at this
point we are inspecting the real, constructed DAG objects, which is
both simpler and more accurate than re-deriving the same information
by hand from source text.
"""
import re
import sys

from airflow.models import DagBag

DAGS_FOLDER = "dags"
NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
MIN_TAGS = 2
SLA_REQUIRED_FOR_TAG = "business-pipeline"


def check_naming(dag) -> list[str]:
    errors = []
    expected_id = dag.fileloc.split("/")[-1].removesuffix(".py")
    if dag.dag_id != expected_id:
        errors.append(
            f"dag_id '{dag.dag_id}' does not match its filename-derived id "
            f"'{expected_id}' (dag_id must equal the filename, minus .py)"
        )
    if not NAME_PATTERN.match(dag.dag_id):
        errors.append(
            f"dag_id '{dag.dag_id}' is not snake_case "
            "(must start with a lowercase letter and use only a-z, 0-9, _)"
        )
    return errors


def check_tags(dag) -> list[str]:
    errors = []
    tags = dag.tags or []
    if len(tags) < MIN_TAGS:
        errors.append(f"must declare at least {MIN_TAGS} tags, found {len(tags)}: {tags}")
    return errors


def check_retries(dag) -> list[str]:
    errors = []
    retries = (dag.default_args or {}).get("retries")
    if retries is None or retries < 1:
        errors.append(
            "default_args must set 'retries' to 1 or more "
            f"(found: {retries!r})"
        )
    return errors


def check_sla(dag) -> list[str]:
    errors = []
    tags = dag.tags or []
    if SLA_REQUIRED_FOR_TAG in tags:
        sla = (dag.default_args or {}).get("sla")
        if sla is None:
            errors.append(
                f"DAGs tagged '{SLA_REQUIRED_FOR_TAG}' must set an 'sla' "
                "(timedelta) in default_args"
            )
    return errors


def main() -> int:
    dagbag = DagBag(dag_folder=DAGS_FOLDER, include_examples=False)

    if dagbag.import_errors:
        print("Skipping lint: DAG import validation must pass first.")
        return 1

    violations: dict[str, list[str]] = {}
    for dag_id, dag in dagbag.dags.items():
        errors = []
        errors += check_naming(dag)
        errors += check_tags(dag)
        errors += check_retries(dag)
        errors += check_sla(dag)
        if errors:
            violations[dag_id] = errors

    if violations:
        print("Custom DAG lint rules FAILED.\n")
        for dag_id, errors in violations.items():
            print(f"--- {dag_id} ---")
            for error in errors:
                print(f"  - {error}")
            print()
        return 1

    print(f"Custom DAG lint rules passed for {len(dagbag.dags)} DAG(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
