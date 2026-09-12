# Phase 5 — How This Workflow Prevents Direct Production Modification

The workflow built in this phase:

```
Developer -> Feature Branch -> Commit -> Push -> Pull Request -> CI -> Review -> Merge main
```

maps directly onto the Phase 0 architecture's first gate. Here is why each link matters:

1. **Feature branch, not `main`** — the developer's in-progress, possibly broken work never touches the branch that later phases will deploy from. There is nothing to accidentally deploy while work is unfinished.

2. **Pull Request required before merge** — per the branch protection rule, changes cannot become part of `main` without a PR existing. `main` is what Phase 6+ will read from to deploy to staging, and Phase 10 to deploy to production — so anything not merged to `main` can never reach either environment.

3. **Status checks required before merge** (configured now, populated in Phase 6) — once a CI workflow exists, this setting will force it to pass before the merge button even becomes clickable. A DAG with a syntax error or a failing unit test physically cannot reach `main`.

4. **Review** — a human (or automated reviewer, as seen with Copilot here) inspects the diff before merge, catching problems automated checks might miss (design questions, business-logic mistakes).

5. **Merge to `main` is the only path forward** — and `main` is the only branch anything downstream (staging deploy, then after approval, production deploy) will ever read from. A developer who wants to change production has no direct route: they must go through a branch, a PR, checks, and review first.

## Where Production Fits

Production is even further insulated: even after a change reaches `main` and auto-deploys to staging (Phase 6), a **separate human approval gate** (Phase 8) sits between staging and production. So a production change requires, at minimum: a PR + passing checks + review to reach `main`, a successful staging deployment and integration test, and a distinct approval step — never a direct push from a developer's machine.

## A UI Bug We Found (and Fixed) Along the Way

As documented in `03-github-state-and-verification.md`, our first two attempts to verify this gate found that direct pushes to `main` succeeded even with protection "enabled." The cause was not a permission gap — it was a GitHub settings-page bug where the branch protection form displayed and even briefly reported checked settings that were not actually persisted server-side. Confirmed by re-checking the real DOM state after a fresh reload, fixed by re-toggling the settings and verifying persistence the same way, and finally proven by testing the real behavior: a direct push to `main` (as the repository owner) is now genuinely rejected by GitHub itself (`GH006: Protected branch update failed`). The gate described above is confirmed to work as designed, for anyone, including the repository owner.
