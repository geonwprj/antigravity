# Global Antigravity Rules File
Global Antigravity rules define how Agent behaves across all your workspaces. Use this file to provide specific context and set specific guidelines for Agent.

# Global Customization Rules

> [!TIP]
> **System Map**: For a complete directory of all Global Rules, Knowledge Artifacts, Skills, and Workflows, refer to the [System Manifest](file:///home/srvadm/.gemini/system_manifest.md).

These rules are established for all projects in this homelab environment to ensure consistency, speed, and premium quality.

## Connectivity & Environment
- **NO LOCALHOST**: Never use `localhost` or `127.0.0.1`. The environment is accessed via SSH; always use the host IP `<HOST_IP>` or hostname `<HOST_NAME>`.
- **Timezone**: Strict use of accurate local timezone (e.g., `Asia/Hong_Kong`) for all services, databases, and logs. Pass `TZ` in `.env` and `docker-compose.yml`.

## Visual Excellence (UI/UX)
- **Dark Mode Mandatory**: All interfaces (Swagger UI, WebApps) must feature a premium dark mode as the default.
- **Premium Aesthetics**: Use curated palettes (Monokai, Obsidian, HSL). Avoid generic colors. Use smooth gradients and micro-animations.
- **Typography**: Prioritize modern fonts like Inter, Roboto, or Outfit.

## Python Development
- **Package Management**: Use `uv` exclusively. No global package installs. Use `uv sync` to align `pyproject.toml` and `uv.lock`.
- **Project Structure**: Source in `src/<project>/`, tests in `tests/`. Test case files should mirror `src/` hierarchy.
- **Testing**: Use `pytest` and `pytest-asyncio`. Run `uv run pytest` locally on host before container deployment.
- **Logic Debugging**: Write targeted unit tests/scripts for logic bugs instead of bulk processing. Use isolated CLI commands (e.g., `uv run python -m app.cli`) for single-record tracing.
- **Pydantic**: Use V2 `ConfigDict` patterns. No deprecated `class Config`.
- **Logging**: Ensure `self.logger = logging.getLogger(__name__)` initialization to avoid masking errors. Use `logger.exception` in task/worker catch blocks.
- **Pre-Response Check**: Verify logic with tests locally and final state on Podman before completion.

## Next.js Development
- **Framework**: Use Next.js App Router by default.
- **Styling**: Vanilla CSS or Tailwind CSS (if requested). Follow Premium Aesthetics rule.
- **Performance**: Optimize for fast loads. Use SWR with `mutate` patterns for partial UI refreshes.
- **Verification**: Test UI via `http://<HOST_NAME>:port` in browser tools.

## Node.js Development
- **Package Management**: Default to `npm` unless `pnpm` is present.
- **Project Structure**: `src/` for logic, `public/` for assets, `tests/` for tests.
- **Environment**: Strict `.env` management with `TZ=<TZ>`.

## General Standards
- **API**: Default prefix `/api/v1/`.
- **Security**: Always generate complex random passwords for new services.
- **Git**: Frequent commits with descriptive messages. Always ignore log files (`*.log`) and log directories (`logs/`) in `.gitignore` to prevent environment-specific pollution.
- **Releases**: For every version bump, ALWAYS create a formal GitHub Release using `gh release create` and verify that the associated container image build (GitHub Action) completes successfully (`success`) before marking the task as done.
- **Database Hygiene**: Roll back or clean up test data records after verification to prevent environment pollution.

## Documentation Integrity
- **Manifest Sync**: Any change to Global Rules, Knowledge, Skills, or Workflows MUST be followed by the `/sync-manifest` workflow to maintain the system map.
- **4-Tier Compliance**: Always categorize new information according to the Tiered Architecture (Rules, Knowledge, Skills, Workflows).

## Environment Configuration (.env)
Projects should follow the standard structure derived from the `abg` reference:
```env
# Base configuration
TZ=<TZ>
SERVER_HOST=0.0.0.0
API_PORT=8000
SERVER_MODE=production
LOG_LEVEL=INFO

# Database (Postgres/Redis)
PGSQL_USER=...
PGSQL_PASSWORD=...
PGSQL_DB=...
PGSQL_HOST=...
PGSQL_PORT=...

# External Services (LLM/SSH)
LLM_API_KEY=...
SSH_HOST=...
```
