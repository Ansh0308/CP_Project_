# Phase 5 — Viva Questions

1. Why is a feature branch created from `main` rather than working directly on `main`?
2. What is the practical difference between `git push` and `git push -u` (`--set-upstream`)?
3. What does a Pull Request actually change about how code reaches `main`, technically speaking (i.e. what does GitHub enforce that plain `git merge` locally would not)?
4. Why did enabling "Require status checks to pass before merging" with zero checks actually selected still matter for this phase?
5. What did our experiment reveal about branch protection and repository ownership on GitHub, and why does that gap not matter in a real company/organization setting?
6. Why was `git revert` used to undo the accidental direct-push test commits instead of `git reset --hard` + force-push?
7. What is the difference between "Require a pull request before merging" and "Require status checks to pass before merging" — what does each independently prevent?
8. If a second developer wanted to contribute to this project, what is the exact sequence of Git/GitHub actions they would need to take, from cloning the repo to having their change appear in `main`?
9. Why does the PR page show "Copilot code review requested" without us configuring anything for it in this phase?
10. How does today's Pull Request (still open, not merged) connect to what Phase 6 (CI) and Phase 8 (approval) will later require before it can be merged?
