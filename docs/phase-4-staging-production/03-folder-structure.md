# Phase 4 — Folder Structure

```
airflow-cicd/
├── staging/
│   ├── docker-compose.yml       # name: airflow-staging
│   ├── .env                     # AIRFLOW_UID=50000 (git-ignored)
│   ├── .env.example             # committed template
│   ├── dags/
│   │   ├── hello_world.py
│   │   └── sales_data_pipeline.py
│   ├── plugins/.gitkeep
│   ├── logs/                    # git-ignored, runtime output
│   └── config/.gitkeep
│
├── production/
│   ├── docker-compose.yml       # name: airflow-production
│   ├── .env                     # AIRFLOW_UID=50000 (git-ignored)
│   ├── .env.example             # committed template
│   ├── dags/
│   │   ├── hello_world.py
│   │   └── sales_data_pipeline.py
│   ├── plugins/.gitkeep
│   ├── logs/                    # git-ignored, runtime output
│   └── config/.gitkeep
│
├── dags/                        # Phase 2/3 dev environment (unchanged)
└── docker-compose.yml           # Phase 2/3 dev environment (unchanged)
```

DAG files are currently duplicated by hand into `staging/dags/` and `production/dags/` from the top-level `dags/` folder. This manual copy is exactly what Phase 6+ automation (GitHub Actions) will replace.
