# Phase 2 — Prerequisite: Installing Docker

Before any Phase 2 implementation could begin, we checked this machine for Docker and found neither Docker nor WSL2 installed.

## Detection Commands Run

```bash
docker --version
docker compose version
docker ps
```
Result: `docker: command not found` (both in Git Bash and PowerShell).

```powershell
wsl --status
```
Result: `The Windows Subsystem for Linux is not installed.`

## Decision

Rather than proceeding with an environment that has no container runtime, we paused implementation. Docker Desktop on Windows requires WSL2 as its backend, an admin-rights install, and at least one restart — none of which can be done by an automated agent. The user was walked through manual installation.

## Install Steps Given to the User

1. `wsl --install` (as Administrator in PowerShell) → restart machine.
2. Verify with `wsl --status` (expect `Default Version: 2`).
3. Download and install Docker Desktop for Windows from docker.com, with the WSL2 backend option enabled.
4. Restart if prompted, then launch Docker Desktop and wait for the engine to start.
5. Re-verify with `docker --version`, `docker compose version`, `docker ps` before continuing Phase 2.

## Status

**Blocked on user completing Docker Desktop installation.** Phase 2 implementation (Compose file, containers, verification) resumes once `docker ps` succeeds.
