# Phase 2 — Troubleshooting Log

## Issue 1: Docker/WSL2 not installed

**Symptom:** `docker: command not found` in both Git Bash and PowerShell; `wsl --status` reported WSL not installed.
**Fix:** User installed WSL2 (`wsl --install`, restart) then Docker Desktop for Windows with the WSL2 backend. Confirmed working via `docker --version`, `docker compose version`, `docker ps`.
**Documented separately in:** `docs/phase-2-local-airflow/00-prerequisite-docker-install.md`

## Issue 2: Port 8080 already in use

**Symptom:**
```
Error response from daemon: ports are not available: exposing port TCP 0.0.0.0:8080 -> 127.0.0.1:0:
listen tcp 0.0.0.0:8080: bind: Only one usage of each socket address...
```
**Diagnosis:** `Get-NetTCPConnection -LocalPort 8080` showed PID 5000 already listening; `Get-Process -Id 5000` identified it as `AgentService.exe` (MiniTool ShadowMaker, a third-party backup tool unrelated to this project).
**Decision:** rather than stopping unrelated software the user may depend on, remapped Airflow's host-side port in `docker-compose.yml` from `8080:8080` to `8081:8080`. Container-internal port stays 8080; only the host mapping changed.
**Result:** webserver started cleanly, UI reachable at `http://localhost:8081`.

## Issue 3: Scheduler container stuck "unhealthy"

**Symptom:** `docker compose ps` showed `airflow-scheduler` as `Up ... (unhealthy)` while `airflow-webserver` and `postgres` were healthy. Scheduler logs showed no errors and looked like it was running fine.
**Diagnosis:** ran the healthcheck manually: `docker compose exec airflow-scheduler curl -sf http://localhost:8974/health` returned exit code 7 (connection refused) — nothing was listening on port 8974.
**Root cause:** Airflow's scheduler only exposes a `/health` HTTP endpoint when `AIRFLOW__SCHEDULER__ENABLE_HEALTH_CHECK` is explicitly set to `true`; it is not the image's default.
**Fix:** added `AIRFLOW__SCHEDULER__ENABLE_HEALTH_CHECK: "true"` to the shared environment block in `docker-compose.yml`, then recreated the scheduler with `docker compose up -d airflow-scheduler`.
**Result:** scheduler reported `healthy` within ~40 seconds.
