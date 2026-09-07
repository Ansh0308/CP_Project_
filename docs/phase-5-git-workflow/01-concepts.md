# Phase 5 — Concepts

**Repository** — the full version-controlled project: all files plus their entire commit history. Ours lives locally at the project root and remotely at `https://github.com/Ansh0308/CP_Project_`.

**Branch** — a movable pointer to a line of commits. Branches let multiple lines of work (a feature, a fix, `main`) exist side by side without interfering with each other.

**Main branch** — the branch representing the project's official, deployable state. Per the Phase 1 workflow, nothing lands here except through a reviewed Pull Request.

**Feature branch** — a short-lived branch created off `main` for one specific piece of work (e.g. `feature/add-grand-total-to-sales-pipeline`). It isolates in-progress work from the stable `main` line.

**Commit** — a saved snapshot of the repo at a point in time, with a message explaining the change. Commits are the atomic units of history.

**Push** — uploading local commits to the remote (GitHub) so they exist beyond one machine and become visible/shareable.

**Pull Request (PR)** — a formal request to merge one branch into another (feature -> main), which GitHub turns into a review surface: diff view, comments, and (once configured) required automated checks.

**Merge** — the act of combining the feature branch's commits into `main`, creating a unified history that includes the new work.

**Code review** — a human (or, as we saw, an AI reviewer like Copilot) reading the PR's diff to catch mistakes, question design decisions, or request changes before merge.

**Branch protection** — repository-level rules on `main` (e.g. "PR required," "status checks must pass") that make review/CI mandatory rather than optional. This is what makes the Phase 0 architecture's gates real instead of just a convention people can forget.
