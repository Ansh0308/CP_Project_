# Phase 5 — Git Commands Used

```bash
# Connect the local repo to GitHub
git remote add origin https://github.com/Ansh0308/CP_Project_.git
git push -u origin main

# Create a feature branch off main
git checkout -b feature/add-grand-total-to-sales-pipeline

# Make a small, legitimate change to dags/sales_data_pipeline.py
# (added a grand-total sum in store_result)

git add dags/sales_data_pipeline.py
git commit -m "Add grand total calculation to sales pipeline output"

# Push the feature branch
git push -u origin feature/add-grand-total-to-sales-pipeline

# Pull Request opened on GitHub: feature/add-grand-total-to-sales-pipeline -> main
```

## Commit Message Used

```
Add grand total calculation to sales pipeline output

store_result now reports the sum across all products in addition to
the per-product breakdown, so the final output is directly useful for
a daily summary without extra downstream aggregation.
```

## The Change Itself

```diff
 def store_result(**context):
     """Simulate persisting the final result (e.g. to a database or file)."""
     totals = context["ti"].xcom_pull(key="totals", task_ids="process_data")
+    grand_total = sum(totals.values())
     print(f"Storing final sales totals: {totals}")
+    print(f"Grand total across all products: {grand_total}")
```

A small, self-contained, realistic feature addition — exactly the size of change a PR-based workflow is meant to review.
