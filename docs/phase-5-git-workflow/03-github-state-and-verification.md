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

## Correction (made during Phase 6): the Real Cause Was a UI Bug, Not Owner Bypass

We originally tested whether the rule blocks a direct push to `main`, including as the repository owner, by pushing test commits directly. Both attempts **succeeded**, and at the time we concluded this was GitHub allowing repository owners to bypass classic branch protection on personal repositories.

**That conclusion was wrong**, and the real cause was found and fixed during Phase 6. GitHub's classic branch-protection edit page has a rendering bug (observed directly, reproduced twice): the "Require a pull request before merging" and "Require status checks to pass before merging" master checkboxes can render and report as checked via the page's own visible state and even via a plain DOM query as `checked: true` shortly after being toggled — but after a full page reload, a JavaScript check of `document.querySelector('input[name="has_required_reviews"]').checked` showed the *true, persisted* value was actually `false`. In other words: our Phase 5 setup never actually saved as enabled in the first place — the pushes succeeded because the rule genuinely did not require a PR yet, not because the owner bypassed a working rule.

**How this was found and fixed (Phase 6):** while adding "Validate DAGs" as a required status check, repeated UI attempts to select it from the search dropdown appeared to work visually but did not persist. Querying the actual checkbox DOM state after a fresh reload revealed both master toggles were `false`. Toggling them again (verified with `.checked === true` immediately, *and* re-verified as still `true` after a full page reload) and then successfully adding "Validate DAGs" as a required check and saving fixed it for real.

**Proof it now works — even for the owner:**
```
$ git push origin main
remote: error: GH006: Protected branch update failed for refs/heads/main.
remote: - Changes must be made through a pull request.
remote: - Required status check "Validate DAGs" is expected.
error: failed to push some refs to 'https://github.com/Ansh0308/CP_Project_.git'
```
This is the real, correct behavior: a direct push to `main` — including by the repository owner — is now genuinely rejected, both for missing a PR and for missing the required "Validate DAGs" check.

**Lesson:** when a GitHub settings page's own UI state seems to update after an action, that is not proof the change was persisted server-side. The only reliable verification is a fresh page reload followed by re-reading the actual state (or, as here, testing the real-world behavior the setting is supposed to control).
