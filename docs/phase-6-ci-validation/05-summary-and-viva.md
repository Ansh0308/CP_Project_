# Phase 6 — Summary and Viva Questions

## What We Built

- `.github/workflows/ci.yml`: a GitHub Actions workflow ("Validate DAGs" job) running on every PR targeting `main` and every push to `main`, with three named, independently-attributable validation layers:
  1. Python syntax validation (`py_compile`)
  2. Airflow DAG import validation (`scripts/ci/check_dag_imports.py`, via `DagBag`)
  3. Custom project DAG lint rules (`scripts/ci/lint_dags.py`: naming convention, mandatory tags, required retries, required SLA for `business-pipeline`-tagged DAGs)
- Brought `hello_world` and `sales_data_pipeline` into compliance with the new rules (retries on `hello_world`, SLA on `sales_data_pipeline`).
- Opened PR #2 to dogfood the Phase 5 workflow, confirmed a real successful CI run (all three layers passed).
- Deliberately introduced and pushed three separate failures (syntax error, import error, naming-convention violation), confirmed GitHub Actions caught each one at the correct layer with clear error output, then restored the DAG to its valid state and confirmed a final successful run.
- Fixed a genuine bug in Phase 5's branch protection setup (settings were never actually persisted) and made `Validate DAGs` a required status check, then proved with a real rejected push that `main` is now actually protected, including against the repository owner.

## Why We Built It This Way

- **Three separate named steps, not one script** — so a failure is immediately attributable to exactly which kind of mistake was made, both in the Actions UI and for anyone reading the log.
- **DagBag-based checks reused across layers 2 and 3** — layer 3 trusts layer 2's successful import rather than re-parsing source text with `ast`, which is simpler and more accurate.
- **Custom lint rules kept in plain Python scripts, not a third-party linter** — the rules (naming, tags, retries, SLA) are specific to this project's conventions; a generic tool wouldn't know them, and a 100-line script is easy for a reviewer (or examiner) to read end-to-end.
- **Constraints file for the `pip install`** — mirrors Apache's own recommended install method, avoiding dependency-resolution failures in CI.

## What Is Still Not Built

- No unit tests (explicitly excluded from this phase).
- No staging or production deployment automation.
- No Git tagging, versioning, or audit log beyond what Git itself provides.
- No rollback mechanism.
- Copilot's PR review flagged two real, unaddressed gaps: (1) the `staging/` and `production/` DAG copies are not validated or kept in sync with the source `dags/` folder — a manual step until automated deployment exists; (2) the SLA lint check only verifies `sla is not None`, not that it is actually a `timedelta`. Both are left as known follow-ups, not fixed in this phase, to avoid scope creep beyond what Phase 6 asked for.

## Likely Viva Questions

1. Why does Layer 1 (syntax) run before Layer 2 (import), which runs before Layer 3 (lint) — what would be lost by reordering them?
2. What is the difference between a Python `SyntaxError` and an Airflow DAG import error — give a concrete example of code that causes one but not the other.
3. Why does `scripts/ci/lint_dags.py` skip its checks entirely if `dagbag.import_errors` is non-empty?
4. Why was `apache-airflow` installed with a `--constraint` file instead of a bare `pip install apache-airflow==2.9.3`?
5. What real bug did we find in GitHub's branch-protection settings page, how did we detect it, and how did we ultimately verify the fix actually worked (not just appeared to)?
6. Why is "the checkbox shows checked in a screenshot" not sufficient proof that a browser-based setting was saved?
7. What is the practical difference, from a CI-cost perspective, between a workflow triggering on `pull_request` versus `push` to every branch?
8. Concretely, what would have to be true for the naming-convention lint rule to reject a DAG that both Layer 1 and Layer 2 accept as completely valid?
9. Why does `sales_data_pipeline` need an SLA in `default_args` but `hello_world` does not, according to this project's own rules?
10. Two real gaps were flagged by an automated PR review (Copilot) and deliberately left unfixed in this phase — what are they, and which later phase would be the natural place to close each one?
