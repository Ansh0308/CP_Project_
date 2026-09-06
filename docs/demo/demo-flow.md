# Expected Final Demo Flow

1. Show a healthy DAG passing through the whole pipeline: PR -> CI green -> merge -> staging deploy -> integration test pass -> approval -> production deploy -> tag `v1.x` created.
2. Introduce a **broken DAG change** (e.g., syntax error) - show it caught at CI, PR blocked, nothing deployed.
3. Introduce a DAG that **passes CI but fails integration testing** on staging - show pipeline halts before production, no approval gate even reached.
4. Deploy a DAG that **passes everything but fails at runtime in production** (e.g., a task that errors only under prod-like data/conditions) - show the failure in the production Airflow UI.
5. Trigger the **rollback workflow**, selecting the last known-good tag - show production DAGs revert and start succeeding again.
6. Show the **audit trail**: Git tag history + GitHub Actions run history narrating the full story (deploy -> failure -> rollback).
