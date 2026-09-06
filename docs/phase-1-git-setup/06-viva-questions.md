# Phase 1 — Likely Viva Questions

1. Why is `.gitkeep` needed — doesn't Git track folders?
2. Why keep `staging/` and `production/` as separate folders instead of one shared Compose file with an environment variable?
3. What's the difference between `.gitignore` entries for `.env` vs `.env.example`, and why would you ever commit the latter?
4. Why is `requirements.txt` empty right now — isn't that unusual for a "setup" phase?
5. Explain trunk-based development vs. Git Flow — why did we choose short-lived feature branches into `main`?
6. What would happen if someone committed directly to `main` right now? What would happen once branch protection exists (Phase 4+)?
7. Why does `plugins/` exist separately from `dags/` in Airflow's convention?
8. What is a "root commit" and why does it matter for an audit trail?
9. If you had to undo this entire Phase 1 commit, how would you do it safely without rewriting history others depend on?
10. Why was no remote (GitHub) repository connected in this phase?
