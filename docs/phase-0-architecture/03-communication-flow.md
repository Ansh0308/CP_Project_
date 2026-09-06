# Phase 0 — How Components Communicate

- **Developer → Git**: `git commit`, `git push` to a feature branch.
- **Git → GitHub**: push updates the remote repo.
- **GitHub → PR**: opening a PR against `main` creates a review/discussion object referencing the branch diff.
- **GitHub → GitHub Actions**: PR events (opened, synchronize) and push-to-main events trigger workflow runs via webhooks.
- **GitHub Actions → CI tools**: the workflow YAML invokes `pytest`, DAG parsing scripts, linters — these run inside ephemeral GitHub-hosted runners.
- **GitHub Actions → Staging Airflow**: on merge to main, a deploy job copies DAG files into staging (via SSH/rsync, Docker volume mount, S3 sync, or `git pull` on the staging host — mechanism TBD in later phase) and/or restarts staging containers.
- **Staging Airflow (Scheduler) → PostgreSQL (staging)**: scheduler writes DAG run/task state.
- **GitHub Actions → Staging Airflow API/CLI**: to trigger a test DAG run and poll its result (integration testing).
- **Human approver → GitHub**: approves the PR or approves a "deployment" gate (GitHub Environments support required reviewers).
- **GitHub Actions → Production Airflow**: after approval, same deploy mechanism as staging, but pointed at the prod host/containers.
- **GitHub Actions → Git tags**: on successful production deploy, a tag is created and pushed, recording "this commit = this deployed version."
- **Audit trail**: lives in two places — Git history/tags (what was deployed and when) and GitHub Actions run logs (who approved, what tests passed).
