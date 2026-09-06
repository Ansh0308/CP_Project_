# Phase 0 — Lifecycle of a DAG Change

## Developer Changes One DAG — Step by Step

1. Developer edits `dags/my_pipeline.py` on a feature branch.
2. Writes/updates a pytest unit test for it (locally, optionally runs Airflow via Docker Compose to eyeball it).
3. Pushes branch, opens a PR into `main`.
4. GitHub Actions fires automatically: lint → DAG validation (import check, cycle check) → pytest unit tests.
5. Results post back to the PR as a status check.

## What Happens When Validation Fails

- The GitHub Actions job exits non-zero.
- The PR shows a **red status check** — branch protection rules block merging.
- Developer sees the failure log directly in the PR, fixes the DAG, pushes again — CI reruns automatically.
- Nothing ever reaches staging or production. This is the cheapest place to fail.

## What Happens When Staging Fails

- This means it passed CI (syntax/unit tests) but the merge-to-main deploy job pushed it to staging, and either:
  - the DAG fails to parse/appear correctly in the staging Scheduler, or
  - a triggered integration test run fails (task errors, wrong output, timeout).
- The pipeline halts before production deploy — the "promote to production" step is never triggered/never becomes available for approval.
- This is logged (failed staging run in Airflow UI + failed GitHub Actions job) so the team can diagnose. Developer fixes and repeats the cycle from step 1 (new commit → new PR or push to main, depending on your branching model).

## What Happens After Approval

- A designated approver (e.g., tech lead) reviews the PR diff *and* the staging integration test results.
- They approve via GitHub's PR review feature and/or a GitHub Environments "required reviewer" gate on the production deployment job.
- This unblocks the `deploy-to-production` job, which was waiting/paused.

## What Happens After Production Deployment

1. GitHub Actions copies the validated DAG files into the production Airflow `dags/` folder.
2. Production Scheduler picks up the new/changed DAG on its next parse cycle.
3. GitHub Actions creates and pushes a **Git tag** (e.g., `v1.5.0`) at the deployed commit.
4. A deployment record is logged (who deployed, when, which commit/tag, link to the Actions run) — this is the audit trail entry.

## What Happens When Production Fails

- Failure detected via: Airflow UI showing failed DAG runs/tasks, alerting (email/Slack from Airflow), or manual observation.
- Team decides: hotfix forward, or **rollback**.
- If rollback: no code is "reverted and re-reviewed" under time pressure — instead, the *previous known-good tag* is redeployed as-is.

## How Rollback Works Conceptually

- Because every production deployment is tagged, rollback = "check out Git tag `v1.4.0`, redeploy those exact DAG files to production," bypassing the need to re-derive what the previous state was.
- This can be a manual-trigger GitHub Actions workflow: input = tag name → checkout that tag → run the *same* deploy job used for normal releases, pointed at that commit instead of `main`'s tip.
- Ideally rollback reuses the identical deploy job as forward-deploys (not a special bespoke script) — this guarantees rollback is just as tested/reliable as forward deployment.
- After rollback, this too is logged (a new audit entry: "rolled back from v1.5.0 to v1.4.0, reason: X").
