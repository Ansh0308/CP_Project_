# Phase 1 — Decisions Log

- **Repo root = `E:\MU\CP\CP_Project`** (acts as `airflow-cicd/` from the target structure) rather than nesting a new subfolder, since this directory already is the project root and already held the Phase 0 `docs/`.
- **`.gitkeep` files** added to every empty directory (`dags/`, `tests/`, `plugins/`, `scripts/`, `staging/`, `production/`, `.github/workflows/`) because Git only tracks files, never empty directories.
- **`requirements.txt` left empty** (just a comment) because no code in the repo yet imports anything — adding `apache-airflow`/`pytest` now would pin dependencies nobody uses. They get added exactly when the phase that needs them arrives (Phase 2/3).
- **Files staged explicitly by name**, not `git add -A`/`git add .`, to keep visibility into exactly what enters the first commit.
- **No GitHub remote connected yet** — this phase is local-repo-only by design. Connecting to GitHub is deferred until it's actually needed (Phase 4, when GitHub Actions/PRs come into play).
- **Default branch renamed to `main`** explicitly rather than relying on local Git config defaults, so the repo is consistent regardless of the machine's `init.defaultBranch` setting.
