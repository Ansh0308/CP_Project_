# Phase 6 — Workflow File Explained

File: `.github/workflows/ci.yml`

| Section | What it does | Why |
|---|---|---|
| `on: pull_request: branches: [main]` | Triggers the workflow whenever a PR targeting `main` is opened or updated | This is the actual CI gate Phase 5's branch protection rule requires — it's what runs before a PR is allowed to merge |
| `on: push: branches: [main]` | Also triggers on every push directly to `main` | Safety net — Phase 5 showed the repository owner can bypass the PR requirement; this ensures even a direct push to `main` still gets validated (after the fact) rather than silently passing unchecked |
| `jobs.validate-dags.runs-on: ubuntu-latest` | Requests a fresh, disposable Ubuntu VM (a "runner") from GitHub to execute the job | Every run starts from a clean, identical environment — no leftover state from a previous run can hide a problem |
| `actions/checkout@v4` | Clones the repository's code onto the runner at the exact commit being validated | Without this step, the runner is an empty VM with no access to our DAG files at all |
| `actions/setup-python@v5` (`python-version: "3.12"`, `cache: "pip"`) | Installs Python 3.12 (matching the `apache/airflow:2.9.3` image's Python version) and caches pip downloads between runs | Version parity with our actual Airflow environments; caching speeds up repeated CI runs |
| `pip install --constraint ... -r requirements.txt` | Installs `apache-airflow==2.9.3` using Apache's official constraints file for Python 3.12 | Installing Airflow without a constraints file is unreliable (dependency resolution can pick incompatible versions) — this is Apache's own recommended install method |
| **Layer 1: Python syntax validation** (`python -m py_compile dags/*.py`) | Compiles every DAG file to bytecode without executing it | Fastest possible check — catches typos/syntax errors in seconds, before spending time installing/running Airflow at all |
| **Layer 2: Airflow DAG import validation** (`airflow db migrate` + `check_dag_imports.py`) | Initializes a throwaway SQLite metadata DB, then loads every DAG via Airflow's own `DagBag`, exactly as the real scheduler would | Catches errors syntax-checking cannot: a missing operator import, a bad argument to `DAG(...)`, a broken cross-file import |
| **Layer 3: Custom DAG lint rules** (`lint_dags.py`) | Re-uses the successfully-imported DAG objects to check project-specific rules: naming convention, mandatory tags, required retries, required SLA for business-critical DAGs | Airflow itself doesn't enforce any of these — they are this project's own quality bar, documented in `03-lint-rules.md` |
| `env: AIRFLOW_HOME`, `AIRFLOW__CORE__LOAD_EXAMPLES`, `AIRFLOW__CORE__DAGS_FOLDER` | Points Airflow at a CI-local home directory and our `dags/` folder, and disables bundled example DAGs | Keeps the CI run isolated to only our own DAGs, with no dependency on any pre-existing Airflow installation |

## Why Three Separate Steps Instead of One Script

Each layer is a distinct CI step (not one combined script) so that a failure is immediately attributable: the GitHub Actions UI shows exactly which named step failed ("Layer 1", "Layer 2", or "Layer 3"), which matters for quickly diagnosing *what kind* of mistake was made without reading through interleaved output.
