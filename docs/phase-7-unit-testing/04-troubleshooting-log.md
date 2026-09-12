# Phase 7 — Troubleshooting Log

## Issue 1: Docker Desktop hung/unresponsive for an extended period

**Symptom:** `docker ps` consistently failed with `failed to connect to the docker API at npipe:...`, even after `Start-Process "Docker Desktop.exe"` and long waits. `wsl -l -v` showed the `docker-desktop` WSL distro as `Stopped` despite Docker Desktop GUI processes appearing to be running.

**Diagnosis:** checking process start times revealed the running processes were stale (hours old, from earlier in the session) rather than a fresh launch — Docker Desktop was stuck in a non-responsive state rather than genuinely starting.

**Fix attempted:** `wsl --shutdown`, force-killed all Docker Desktop/backend processes, relaunched fresh. Confirmed via new process start times that a genuine fresh instance launched, but the `docker-desktop` WSL VM still did not come up within a reasonable wait. Ultimately not resolved within this session's time budget.

**Workaround:** used a native Windows Python 3.11 virtual environment as a first fallback (see Issue 2), and GitHub Actions (Linux runners) as the authoritative verification environment (see `03-verification.md`).

## Issue 2: `apache-airflow` cannot run natively on Windows

**Symptom 1 — SQLite path rejected:**
```
airflow.exceptions.AirflowConfigException: Cannot use relative path: `sqlite:///C:/temp_airflow_home/airflow.db`
to connect to sqlite. Please use absolute path such as `sqlite:////tmp/airflow.db`.
```
**Root cause:** Airflow's `configure_orm()` requires the SQLite connection string to start with exactly `sqlite:////` (four slashes, POSIX-absolute style). The SQLAlchemy-correct Windows format (`sqlite:///C:/path`, three slashes plus a drive letter) fails this check, and there is no Windows-correct string that satisfies it and is also a valid path sqlite3 can open (confirmed: `sqlite:////c:/temp_airflow_home/airflow.db` passes Airflow's check but then fails with `sqlite3.OperationalError: unable to open database file`, since `/c:/...` is not a path Windows/sqlite3 can resolve).

**Symptom 2 — missing POSIX module:**
```
ModuleNotFoundError: No module named 'fcntl'
```
raised when importing `airflow.operators.python` (which `PythonOperator` requires). `fcntl` is a POSIX-only standard library module with no Windows equivalent; nothing at the pip/dependency level can fix this.

**Conclusion:** this is a hard, well-known Airflow platform limitation (Airflow's own package prints a `RuntimeWarning` on import stating it is only regularly tested on Linux/macOS, with Windows support tracked as a low-priority open issue). It is not a project misconfiguration. This is consistent with Phase 2's original finding that this project requires Docker specifically because Airflow cannot run natively on Windows — Phase 7 re-confirms the same limitation at the Python-dependency level, one layer deeper than Phase 2's Docker-Desktop-focused framing.

**Resolution:** abandoned native Windows execution entirely; used GitHub Actions (Linux) as the real, authoritative "run pytest" environment for this phase, as documented in `03-verification.md`.

## Issue 3: `pytest==8.3.3` conflicted with Airflow's constraints file

**Symptom:**
```
ERROR: Cannot install pytest==8.3.3 because these package versions have conflicting dependencies.
The conflict is caused by: The user requested pytest==8.3.3, The user requested (constraint) pytest==7.4.4
```
**Diagnosis:** Apache Airflow's official constraints file for 2.9.3 (used by both local install attempts and CI's `pip install --constraint ...`) pins `pytest==7.4.4` as a transitive dev-dependency version. Requesting a newer pytest in `requirements.txt` directly conflicts with that pin.

**Fix:** pinned `pytest==7.4.4` in `requirements.txt` to match the constraints file exactly. Caught locally before ever reaching CI, avoiding a wasted CI run.

## Issue 4: `from dags.sales_data_pipeline import ...` failed

**Symptom:** `dags/` is a plain folder (matching Airflow's convention), not a Python package (no `__init__.py`), so importing it as `dags.sales_data_pipeline` in `tests/test_task_logic.py` would fail.

**Fix:** in `tests/conftest.py`, added `dags/` directly to `sys.path`, allowing test files to import DAG modules as top-level modules (`from sales_data_pipeline import clean_data`) without needing to turn `dags/` into a package (which could have unintended effects on how Airflow itself scans that folder).

## Issue 5: A demo scenario didn't isolate the layer it was meant to

**Symptom:** the first "incorrect configuration" demo (removing the required `sla`) was caught by **Layer 3** (custom lint) before pytest (**Layer 4**) ever ran, since both layers independently enforce the same SLA rule and the workflow stops at the first failing step.

**Resolution:** not a bug — this is the CI pipeline correctly failing fast. To additionally produce a demonstration isolated to pytest specifically, a second variant was used (flipping `catchup` to `True`, a rule Layer 3 does not check), which failed cleanly and only at Layer 4. Both pieces of evidence are kept in `03-verification.md` since they illustrate two real, useful things: defense-in-depth (two layers independently catching the same class of mistake) and fail-fast pipeline behavior.
