---
name: debugging-container-deployments
description: Diagnoses and resolves container deployment failures, networking issues, and healthcheck problems in podman-compose setups. Use when testing, debugging CI/CD, or troubleshooting unreachable services and ghost containers.
---

# Debugging Container Deployments (CI/CD)

This skill provides a solid, practical methodology for debugging containerized applications locally before committing to production CI/CD pipelines. It ensures stable proxy logic, resolves healthcheck failures, and clears structural deployment locks.

## When to use this skill
- A container fails to start, is stuck in a 'starting' loop, or crashes immediately.
- `podman-compose` or `docker-compose` fails to recreate a container due to "already in use" errors.
- Internal Traefik routing returns `404 Not Found` or `500 Internal Server Error` for proxied routes.
- The user requests to "test and debug" a deployment or fix a CI/CD setup.

## Core Debugging Workflow

### 1. Diagnose Container State
Always check the raw state of the containers first before guessing the issue.
```bash
# Check all containers including exited/crashed ones
podman ps -a

# Extract the tail logs of the specific crashed container
podman logs <container_name> | tail -n 50
```

### 2. Handle Schema and Healthcheck Crashes Natively
If a container like a backend or worker fails its healthcheck:
- Read the exception stack trace from the logs.
- Do **not** bypass the healthcheck. Instead, fix the underlying code or environment configuration.
- Look for circular dependencies (e.g., SQLAlchemy model imports in Python) or missing initial tables.

### 3. Resolve "Ghost Container" Storage Locks
Often, after a crash, `podman-compose up` will fail to rebuild because the previous container ID locked the static container name (e.g. `Error: creating container storage: the container name is already in use`).
To cleanly resolve ghost configurations and force a fresh CI/CD rebuild:
```bash
# 1. Bring down the full compose stack
podman-compose down

# 2. Force remove any lingering ghost container IDs matching the app
podman rm -f <stale_container_id>

# 3. Force a complete rebuild and recreation of the targeted service
podman-compose up -d --build --force-recreate <service>
```

### 4. Optimize Traefik Proxy Routing Integrity
When a reverse proxy (like Traefik via `infra-net`) is used:
- **Remove Host Port Mappings**: Unless explicitly bypassing the proxy for local host access, remove `ports: - "8000:8000"` from `docker-compose.yml`. Keep the container isolated to the `networks:` boundary.
- **Port Mapping Range**: If host exposure is required, internal application ports should remain default (e.g., `8000`), but the **host-side port** must be **greater than 20000** (e.g., `28001:8000`).
- **Align Application Routing to the Proxy**: If Traefik routes traffic via `PathPrefix('/api')`, the backend API must be natively aware of it. For example, explicitly mount FastAPI documentation relative to the proxy route:
```python
app = FastAPI(
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)
```
- **Use Relative Paths for Frontends**: Ensure frontend environment variables like `NEXT_PUBLIC_API_URL` are set to absolute-relative paths (e.g., `/api/v1`) rather than hardcoded URLs (e.g., `http://localhost:8000`). This ensures cross-origin requests work flawlessly through external Zero Trust tunnels.

### 5. Final Local Verification
Always verify the deployment passes locally *before* configuring Cloudflare Zero Trust tunnels:
```bash
# Simulate an external request hitting the internal Traefik load balancer
curl -sI -H "Host: <traefik_router_host>" http://localhost:80/ | head -n 1
```
