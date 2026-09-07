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

## The Caveat We Found

As documented in `03-github-state-and-verification.md`, GitHub's classic branch protection cannot fully restrict the *repository owner* on a personal-account repo — only collaborators without owner/admin rights are actually blocked from bypassing it. In a real organizational setting (a team, not a solo account), this gap closes: the developer pushing changes is essentially never the account that owns repository settings, so the protection is fully effective for everyone whose work is meant to be gated. This is worth knowing precisely because it is not obvious, and a real deployment of this workflow at a company would rely on organization-level roles rather than a single personal account playing every part.
