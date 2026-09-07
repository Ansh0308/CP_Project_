# Phase 5 — Expected/Verified GitHub State

## Pull Request

- **URL:** `https://github.com/Ansh0308/CP_Project_/pull/1`
- **Title:** "Add grand total calculation to sales pipeline output"
- **State:** Open
- **Base <- Head:** `main` <- `feature/add-grand-total-to-sales-pipeline`
- **Commits:** 1
- **Files changed:** 1 (`dags/sales_data_pipeline.py`)
- **Checks:** 0 (no CI configured yet — expected at this phase)
- **Reviewers:** Copilot code review auto-requested by repository default settings

Verified by reading the PR page directly (`get_page_text`): the page confirmed "wants to merge 1 commit into main from feature/add-grand-total-to-sales-pipeline", "Open", "Commits 1", "Files changed 1", and the Copilot review session line.

## Branch Protection Rule on `main`

Configured at `https://github.com/Ansh0308/CP_Project_/settings/branches`:

- Branch name pattern: `main`
- **Require a pull request before merging**: enabled
- **Require status checks to pass before merging**: enabled (no specific check selected yet — there is no CI to require until Phase 6)
- **Do not allow bypassing the above settings**: enabled

Confirmed via the Branches settings page: "main — Currently applies to 1 branch."

## Important Real Finding: Owner Bypass on Personal Repositories

We deliberately tested whether the rule actually blocks a direct push to `main`, including as the repository owner, by:
1. Checking out `main` locally, committing a trivial test line directly (no PR), and pushing — **this succeeded**, even with "Require a pull request before merging" enabled.
2. Editing the rule to also enable "Do not allow bypassing the above settings" and repeating the test — **it still succeeded**.

Both test commits were cleanly reverted with forward `git revert` commits (not force-push/history rewrite) immediately after, so `main`'s content is unaffected; the attempts remain visible in history as an honest record.

**Conclusion:** on a personal (non-organization) GitHub repository, the repository **owner** account retains the ability to push directly to a "protected" branch regardless of classic branch-protection settings — there is no lower permission role to demote the owner to. This is a platform limitation, not a misconfiguration on our part; the settings themselves were confirmed correctly saved. In a real team setting (organization-owned repo, or the developer pushing is *not* the owner/an admin), the exact same rule would correctly block the push and force a Pull Request. This is documented here rather than hidden, because it's a genuinely useful, non-obvious thing to know about how GitHub's protection model works.
