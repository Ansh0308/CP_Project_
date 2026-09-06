# Phase 1 — Commands Run (Reference)

All commands run from the repo root: `E:\MU\CP\CP_Project`

```bash
# Create the folder skeleton
mkdir -p dags tests plugins scripts staging production .github/workflows

# Add placeholders so empty folders are tracked by git
touch dags/.gitkeep tests/.gitkeep plugins/.gitkeep scripts/.gitkeep \
      staging/.gitkeep production/.gitkeep .github/workflows/.gitkeep

# Initialize git and set default branch name
git init
git branch -m main

# Inspect what's untracked before staging
git status

# Stage everything explicitly (not git add -A)
git add dags tests plugins scripts staging production .github docs \
        .gitignore README.md requirements.txt

# Create the initial commit
git commit -m "Initial repo structure for Airflow CI/CD project"
```

## Verification

```bash
git branch          # expect: * main
git log --oneline   # expect: one commit
git status          # expect: "nothing to commit, working tree clean"
git remote -v       # expect: empty (no remote connected yet)
```
