# Phase 4 — Troubleshooting Log

## Issue: Production webserver crashed with `OSError: [Errno 12] Cannot allocate memory`

**Symptom:** after starting staging (3 containers) and production (3 containers) while the Phase 2/3 dev environment (3 more containers) was still running, `airflow-production-airflow-webserver-1` failed to boot:
```
OSError: [Errno 12] Cannot allocate memory: '/opt/airflow/dags'
...
ERROR - No response from gunicorn master within 120 seconds
ERROR - Shutting down webserver
```

**Diagnosis:** running three full Airflow stacks simultaneously means 3x Postgres + 3x Scheduler + 3x Webserver (each webserver spawning 4 Gunicorn worker processes) — 9 containers and ~12+ Python processes total. WSL2's allocated memory to Docker Desktop was insufficient to boot a 4th set of Gunicorn workers under that load.

**Fix:** stopped the Phase 2/3 dev environment (`docker compose stop` from the repo root) — it was not required to be running simultaneously for this phase's goal (staging and production must work, and be independent of *each other*, not necessarily coexist with a third unrelated environment). Restarted the production webserver, which then booted cleanly and reported healthy.

**Follow-up finding:** when the dev environment was later restarted to check three-way coexistence, its webserver again failed to reach a healthy state under the combined load, confirming this is a genuine host resource ceiling (not a one-off fluke). Decision: for this project, run at most two Airflow stacks at a time on this machine (e.g. staging + production for a promotion demo, or dev alone for DAG authoring) rather than all three concurrently.

**Why this doesn't block the project:** the requirement was that staging and production each work correctly and are logically independent of one another — verified by stopping/starting one without affecting the other. Real-world staging/production environments also normally run on separate physical or cloud infrastructure rather than colocated on one machine, for this exact reason (resource isolation, blast-radius containment) — this local finding actually reinforces that architectural principle rather than undermining it.
