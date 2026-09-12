# Phase 6 — Branch Protection Fix and Making "Validate DAGs" Required

## Goal

Fulfill the "configure the repository so we can later add required CI checks" groundwork from Phase 5, now that a real check (`Validate DAGs`) exists to require.

## What We Found

While adding `Validate DAGs` as a required status check on the `main` branch protection rule, we discovered that Phase 5's branch protection settings had never actually been saved, despite the settings page appearing to show them as enabled at the time.

**Root cause:** GitHub's classic branch-protection edit page has a rendering bug. The "Require a pull request before merging" and "Require status checks to pass before merging" checkboxes could be toggled and would report `checked: true` immediately (both visually and via a JavaScript DOM query) — but after a full page reload, a fresh JavaScript check of the same DOM property showed the real, persisted value was `false`. The page's own visible/immediate state was not reliable evidence of what the server had actually saved.

**How this was caught:** repeated attempts to select `Validate DAGs` from the required-status-checks search dropdown appeared to work in the UI, but the "Status checks that are required" list kept reverting to "No required checks" after any reload. Querying the checkbox DOM state directly (`document.querySelector('input[name="has_required_reviews"]').checked`) after a fresh page load confirmed both master toggles were actually `false`.

## The Fix

1. Toggled `has_required_reviews` and `has_required_statuses` on again.
2. Verified `checked === true` immediately, then reloaded the page fresh and verified `checked === true` again (persistence check) before proceeding.
3. Added `Validate DAGs` as a required status check via the search box, confirmed it appeared under "Status checks that are required".
4. Clicked "Save changes".
5. Reloaded fresh one more time and re-verified via JavaScript that `has_required_reviews`, `has_required_statuses`, and `enforce_all_for_admins` were all `true`, and that "Validate DAGs" appeared on the page as a required check.

## Proof It Now Works — Including for the Repository Owner

```
$ git push origin main
remote: error: GH006: Protected branch update failed for refs/heads/main.
remote: - Changes must be made through a pull request.
remote: - Required status check "Validate DAGs" is expected.
error: failed to push some refs to 'https://github.com/Ansh0308/CP_Project_.git'
```

A direct push to `main`, attempted as the repository owner, is now genuinely rejected — for two independent reasons (no PR, and the missing required check). This corrects Phase 5's original (incorrect) conclusion that GitHub allows repository owners to bypass classic branch protection unconditionally; the real cause was this unsaved-settings bug, not a permissions gap. Phase 5's documentation has been updated to reflect this.

## Lesson

A settings page appearing to reflect a change — even a JavaScript-verified `checked: true` moments after clicking — is not proof the change was persisted server-side. The only reliable verification is either (a) a fresh reload followed by re-reading the real state, or (b) testing the actual real-world behavior the setting is supposed to control. This project now does both wherever a setting matters for correctness.
