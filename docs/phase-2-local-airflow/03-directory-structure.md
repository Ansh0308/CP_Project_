# Phase 2 — Directory Structure Added

```
airflow-cicd/
├── dags/
│   └── hello_world.py       # Phase 2 sanity-check DAG
├── plugins/                 # empty (.gitkeep) — no custom operators yet
├── tests/                   # empty (.gitkeep) — pytest tests start Phase 3
├── config/                  # empty (.gitkeep) — Airflow local config overrides, if ever needed
├── logs/                    # bind-mounted, git-ignored — Airflow writes task/scheduler logs here
├── docker-compose.yml       # defines postgres, airflow-init, airflow-webserver, airflow-scheduler
├── .env                     # local-only, git-ignored (AIRFLOW_UID=50000)
└── .env.example             # committed template of the above
```

`logs/` is bind-mounted from the host but is NOT meant to be committed — it is runtime output, already covered by the `.gitignore` catch-all pattern (`logs/`) from Phase 1.
