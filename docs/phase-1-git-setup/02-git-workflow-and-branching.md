# Phase 1 — Git Workflow and Branching Model

## Workflow: Trunk-based development with short-lived feature branches

- `main` is always the source of truth and (starting Phase 4) is protected — no direct pushes allowed.
- Every change — even a one-line DAG edit — happens on a feature branch (`feature/add-sales-dag`, `fix/typo-in-readme`).
- A **commit** is a snapshot with a message explaining *why*, not just *what*.
- A **Pull Request (PR)** is opened from the feature branch into `main`. This is the checkpoint where CI (later phases) runs automatically, and a human reviews the diff.
- Once CI passes and (later) a reviewer approves, the branch is merged into `main` — this merge event is what will eventually trigger auto-deploy to staging.
- After merging, the feature branch is deleted; `main` moves forward.

This gives us, for free, exactly the "Developer -> Git -> PR -> CI" part of the Phase 0 architecture — even before any CI exists.

## Why We Are Not Deploying Anything Yet

Phase 1 only establishes the container for the project — folder layout and version control discipline. There is no Airflow running, no DAG code, no tests, no CI, so there is nothing correct or valid to deploy. Deploying now would mean copying an empty shell into an environment that doesn't exist yet — deployment only becomes meaningful starting Phase 5+ (staging exists) and Phase 9+ (production exists). Building in order means each phase can be verified in isolation instead of debugging five new systems at once.
