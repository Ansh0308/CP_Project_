# Phase 0 — Terminology Clarified

| Term | Meaning here | Not to be confused with |
|---|---|---|
| **CI** | Automatically *checking* a change (lint, validate, unit test) before merge | Not deployment |
| **CD** | Automatically *shipping* a validated change to an environment (staging or, after approval, production) | Not testing |
| **Validation** | Structural check: does the DAG file parse, import, have no cycles, follow naming conventions | Not "does it produce correct output" |
| **Unit Testing** | Testing DAG *code* in isolation (e.g. with pytest) without a running Airflow instance | Not testing task execution |
| **Integration Testing** | Actually running the DAG inside a live Airflow (staging) and checking real execution behavior | Not just import checks |
| **Staging** | A safe, production-like environment for rehearsal — mistakes here are cheap | Not "a second production" |
| **Production** | The real environment whose failures have real consequences | — |
| **Deployment** | The mechanical act of placing DAG files into an environment's DAG folder | Not "promotion" (see below) |
| **Promotion** | The *decision/process* of moving a specific validated version from staging to production | Deployment is the mechanism; promotion is the workflow concept wrapping it |
| **Rollback** | Redeploying a previously tagged good version in response to a failure | Not "undo the git commit" — the commit history stays intact, you just redeploy an older artifact |
