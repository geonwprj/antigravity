# Project Archive: VOD Hub

## Media Matcher Logic
- **Regex Peeling Strategy**: Progressively strip metadata (resolution, language, season) to generate multiple search candidates.
- **Improved Cleansing**: 
  - Handle complex suffixes like "有胸版", "电影版", "动态漫".
  - Aggressively peel trailing alphanumeric strings (e.g., "HERO", "game2") when concatenated with non-ASCII titles.
  - Require boundary-aware matching for `S[0-9]+` and `E[0-9]+` to avoid over-stripping.
- **"Other" Type Handling**: Categories like "短剧" (Short Drama) skip TMDB search to preserve API quota and create local placeholders instead.
- **Placeholder Upgrading**: A matching record (tv/movie) can "upgrade" an existing "other" placeholder with full TMDB metadata rather than being blocked by it.
- **Title Normalization**: Strip Roman numerals (Ⅰ-Ⅹ) and handle Traditional/Simplified Chinese variants using `LocalizationTool`.

## Sync & Task Management
- **Efficiency**: Use a `TaskManager` to track last successful runs and prevent overlap.
- **Batching**: Implement `/batch-unmatch` and `/batch-match` endpoints for high-volume operations.

## Backend Implementation
- **Initialization**: Tables initialized via FastAPI `lifespan`.
- **Database Connections in Celery**: Always use `NullPool` for SQLAlchemy `create_async_engine` when invoked inside Celery tasks (which use `asyncio.run()`). Each task spins up a new event loop, causing default connection pools to either break or aggressively exhaust Postgres connections.
- **Celery Debugging**: Verify `redis-cli ping` and check worker/beat logs if tasks fail to trigger.

## Troubleshooting & Logging
- **Testing Database Connections**: When modifying database clients or engine logic, ensure to run `pytest tests/vod_hub/clients/test_db_connections.py` to prevent regressions related to connection exhaustion.
- **Timezone Drift in Croniter**: `croniter` calculates naive cron expressions (`* * * * *`) using the *local timezone* of the system. If using UTC for database `last_run` fields, you **MUST** pass `tzinfo=timezone.utc` into `datetime.now()` and the `croniter` evaluation methods, or tasks will silently halt due to offset math errors.

## CI/CD Pipeline Requirements
- **Pre-Deployment Checks**: A `SyntaxError` inside a background worker (like Celery) will silently crash the container on startup without failing the `podman-compose build`. **Before every deployment**, you must execute `./scripts/pre_deploy_check.sh` to validate Python syntax (`py_compile`) and run fast unit tests.
# VOD Hub Development & Debugging Knowledge Base

This document distills the key technical learnings and troubleshooting steps encountered during the development and deployment of the VOD Hub project.

## 1. Infrastructure & Deployment (Podman/Compose)

### Networking & Access
*   **Internal Communication**: Containers on the same `infra-net` should communicate via service names (e.g., `http://backend:8000`).
*   **External Access (Dev)**: **CRITICAL - No Traefik Installed.** The dev environment does not run Traefik by default. You MUST use the `docker-compose.dev.yml` overlay to expose the service ports (8000, 3000) directly to your host machine.
    *   **Command**: `podman-compose -f docker-compose.yml -f docker-compose.dev.yml up -d`
*   **Port Exposure**: Ensure `ports` mappings are defined for `frontend` (3000), `backend` (8000), `db` (5432), and `redis` (6379) in the dev overlay.

### Container Management
*   **Healthchecks**: Podman's healthcheck behavior can vary. Use `podman ps --format "table {{.Names}}\t{{.Status}}"` to verify the `(healthy)` flag on critical services like `db` and `backend`.
*   **Clean Start**: When configuration changes (like port exposure) aren't reflecting, a full `down` and `up` cycle is safer than a simple `restart`.

---

## 2. Python Environment & Tooling

### `uv` Package Manager
*   **Philosophy**: Avoid `pip` and system-level Python packages. Use `uv` for all operations to ensure consistency through the `uv.lock` file.
*   **Common Commands**:
    *   `uv sync`: Synchronize the virtual environment with `pyproject.toml`.
    *   `uv run <command>`: Execute a command within the managed environment.
    *   `uv add <package>`: Add a new dependency (updates `pyproject.toml` and `uv.lock`).
*   **Host vs. Container**: If running tests locally, ensure `uv` is installed on the host and `uv sync` is executed to replicate the container's environment.

### Backend Debugging
*   **Database Initialization**: Tables are initialized via the FastAPI `lifespan` event. If migrations are needed, they should be triggered here or via a dedicated CLI.
*   **Celery Worker/Beat**: If scheduled tasks (like matching or syncing) aren't running:
    1.  Check Redis connectivity: `redis-cli ping`.
    2.  Check Worker logs: `podman logs vod_hub_worker_1`.
    3.  Check Beat logs: `podman logs vod_hub_beat_1`.

---

## 3. Matcher & Sync Logic

### Media Title Normalization
*   **Regex Ordering**: When stripping noise from titles, specific media-type suffixes (e.g., `特别篇`, `剧场版`) should be handled *prior* to general noise patterns to ensure accuracy.
*   **Chinese Media Suffixes**: Use non-capturing groups `(?:特別|特别|別|别)篇` to handle both Simplified and Traditional variants efficiently.
*   **Roman Numerals**: Stripping Roman numerals (`Ⅰ-Ⅹ`) helps align messy crawler titles with clean metadata providers like TMDB.

### Sync Efficiency
*   **Task Management**: Use a `TaskManager` to track the last successful run of a sync job. This prevents overlapping executions and excessive API calls.
*   **Batch Operations**: Implement batch endpoints (e.g., `/batch-unmatch`, `/batch-match`) to reduce frontend-to-backend roundtrips when managing large numbers of videos.

---

## 4. Web Frontend (Next.js & Tailwind)

### UI Consistency & Layout
*   **Sticky Cells**: When creating tables with sticky columns (e.g., "Actions"), ensure an explicit background color is set. Otherwise, content from scrolling rows will appear behind the sticky cell's transparent background.
*   **Sidebar Robustness**:
    *   Use `shrink-0` on icons and buttons to prevent them from compressing or wrapping in collapsed states.
    *   Use `justify-between` and conditional padding to maintain alignment across different widths.
*   **Service Indicators**: Use a dedicated `ServiceStatus` component with auto-refresh (e.g., via `SWR`) to provide real-time feedback on backend health.

### State Management
*   **SWR for Data Fetching**: Use `mutate` with key patterns (e.g., `key.startsWith('/videos')`) to trigger partial UI refreshes after batch operations without reloading the entire page.
*   **Mobile-First Design**: Implement card-based layouts for mobile views while maintaining table-based layouts for desktop to ensure usability across devices.

---

## 5. Testing Requirements

### Testing Flow and Preventing False Positives
*   **Why tests passed while sync failed**: Previous tests passed because there was zero automated test coverage for the `SyncTool` itself. Existing tests only verified the `MediaMatcher` and `TaskManager`. The `sync_categories` bug (omitting the DB save) slipped through because `test_sync_manual.py` required a human to execute and visually verify the console output.
*   **Automated Testing Flow**: To prevent this, the project now utilizes `pytest-cov` to enforce test coverage.
*   **Testing Side Effects**: For any tool performing database writes (e.g., `SyncTool`, `CategoryMapper`), ensure dedicated `pytest` tests explicitly validate the call to `db.bulk_upsert()` (either via `AsyncMock` or in an ephemeral DB context). Do not just assert that the returned object contains parsed data.
