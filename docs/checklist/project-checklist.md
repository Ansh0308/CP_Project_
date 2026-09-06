# Final Project Checklist

- [ ] Local Airflow running via Docker Compose
- [ ] Git repo with feature-branch workflow and branch protection on `main`
- [ ] At least 2-3 sample DAGs (including one deliberately breakable for the demo)
- [ ] pytest suite covering DAG structural/unit tests
- [ ] GitHub Actions CI workflow (lint, validate, test) gating PR merges
- [ ] Staging Airflow environment (separate Docker Compose + Postgres)
- [ ] Auto-deploy-to-staging job on merge to main
- [ ] Integration test job that triggers and verifies a real staging DAG run
- [ ] Approval gate before production deploy
- [ ] Production Airflow environment (separate Docker Compose + Postgres)
- [ ] Auto-deploy-to-production job (post-approval)
- [ ] Git tagging automation on successful prod deploy
- [ ] Deployment/audit log (who/what/when/which tag)
- [ ] Manual rollback workflow (redeploy a chosen prior tag)
- [ ] Documented failure-and-recovery demo script
