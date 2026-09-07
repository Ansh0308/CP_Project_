# Phase 4 — Concepts

## 1. Why production should not be used for development/testing

Production runs real business workflows on real data with real consequences. Testing there risks corrupting real data, triggering false alerts, consuming production resources, or causing an actual outage, with no safety net. Every experiment must happen somewhere failure is cheap.

## 2. Why staging exists

Staging is a rehearsal environment — architecturally identical to production (same Airflow version, same executor, same DAG folder structure) but running fake/sample data with zero business consequences. It is where "works on my laptop but not for real" problems get caught before they can hurt production.

## 3. Development vs. Staging vs. Production

| | Development (Phase 2/3) | Staging | Production |
|---|---|---|---|
| Purpose | Author and iterate on DAGs | Rehearse deployment, run integration tests | Serve real business workflows |
| Data | Fake/hardcoded | Fake or masked/sample data | Real |
| Stability | Expected to break often | Should mostly work; failures are informative | Must be stable |
| Who touches it | Individual developer, whenever | CI/CD, automatically, after merge | CI/CD, only after human approval |
| Consequences of failure | None | Cheap — logged, blocks promotion | Expensive — visible, may need rollback |

## 4. Why separate metadata databases

Airflow's Postgres DB holds DAG run history, task states, connections, and variables. If staging and production shared one DB: a staging test run could pollute production's history (breaking audit trail integrity), a bad staging experiment could corrupt state production depends on, and there would be no way to wipe/reset staging without also wiping production. Isolation is what makes each environment's audit trail trustworthy.

## 5. What should be shared vs. different

| Shared | Different |
|---|---|
| Airflow image version (`apache/airflow:2.9.3`) — reproducibility | Metadata database (separate Postgres instance/volume each) |
| DAG code (same file content, once promoted) | Host ports (no collisions) |
| Compose file structure / service names (consistency) | Container/project names, DAG folder path, `.env` values |
| Executor type (`LocalExecutor`) — matching behavior | Admin credentials (never reuse passwords across environments) |

## 6. How DAG files will eventually be synchronized into both environments

Currently, DAG files are placed manually into each environment's own `dags/` folder — no automation yet. From Phase 6 onward, GitHub Actions will do this automatically: on merge to `main`, a job copies validated DAG files into staging's `dags/` folder; after human approval, the same mechanism copies them into production's `dags/` folder. Both environments read from the same Git-versioned source, just deployed to physically separate folders/environments at different times.

## 7. Why we are not connecting CI/CD yet

Automating deployment before the destinations (staging, production) reliably exist and are verified independently would mean debugging the environments and the automation at the same time. Phase 4 proves each environment works correctly in isolation, by hand — Phase 6+ will automate the exact manual steps performed in this phase.
