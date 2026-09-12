# Phase 6 — Concepts

**CI (Continuous Integration)** — the practice of automatically building/checking every change (on every push or PR) rather than trusting a developer's local testing. It converts "should work" into "verified to work, every single time."

**GitHub Actions** — GitHub's built-in automation engine. It watches for repository events (a PR opened, a push to a branch) and, when one matches a rule you define, spins up a fresh virtual machine to run whatever checks you specify.

**Workflow** — a single YAML file (`.github/workflows/ci.yml`) describing "on these events, run these jobs." A repo can have multiple workflows for different purposes.

**Job** — a group of steps that all run together on the same runner (same VM). A workflow can have multiple jobs; by default they run in parallel unless one is made to depend on another.

**Step** — one command or action inside a job (e.g. "check out the code," "install Python," "run this script"). Steps in a job run sequentially, in order, on the same machine, sharing filesystem state.

**Runner** — the actual virtual machine that executes a job. GitHub provides free hosted runners (`ubuntu-latest` here) — a clean, disposable Linux VM spun up just for that job and destroyed after.

**Why validation happens before merge** — this is the Phase 0 architecture's CI gate. Catching a broken DAG before it becomes part of `main` is nearly free (reject the PR, developer fixes it, nobody else is affected). Catching the same mistake after merge means it is already in the branch staging/production deploy from — now it's incident response instead of a code review comment. The Phase 5 branch protection rule ("require status checks to pass") is what turns this from "nice to have" into "physically impossible to skip" for anyone but the repository owner (see Phase 5's documented bypass caveat).
