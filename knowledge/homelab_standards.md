# Homelab Development & Infrastructure Standards

This document is the unified source of truth for general technical standards in this environment.

## 1. Visual System (UI/UX)
- **Theme**: Premium Dark Mode is mandatory for all interfaces.
- **Palette**: Curated HSL/Monokai/Obsidian colors. No basic primary colors.
- **Typography**: Modern fonts (Inter, Roboto, Outfit).
- **Interactions**: Smooth gradients and micro-animations (e.g., `scale(1.02)` on hover).
- **Layout (Desktop Sidebar)**: Expanded: 205px | Collapsed: 80px | Toggle: Flat icon button (`⟪` / `⟫`).
- **Standard Gutters**: 1.5rem (24px) padding.

### Framework-Specific UI
- **FastAPI (Swagger)**: Use `fastapi-swagger-ui-theme` (Theme: `obsidian`).
- **Next.js**: SWR with `mutate()` for optimistic updates. Mobile-first card-to-table transitions.

## 2. Infrastructure & Networking
- **Subnets**:
  - Server: `10.0.99.0/24` (Host: `10.0.99.118`)
  - Client: `10.0.100.0/24` | IoT: `172.20.0.0/16` | DNS: `10.0.5.0/24`
- **DNS & Domains**:
  - Internal: `geonw.local` (Technitium CNAMEs).
  - Public: `geow.uk` (Cloudflare Zero Trust).
  - **Prohibited**: Never use `localhost` or `127.0.0.1`.
- **Port Management**: Host-side mappings MUST be **> 20000**.
- **Environments**:
  - Production: LXC-hosted, Podman isolation.
  - Development: LXC-hosted, `uv` (host) + Podman (integration) coexistence.
  - **Locale**: Mandatory use of `en_HK.UTF-8` as the default system locale to ensure Chinese character support across all services, databases, and logs.

## 3. Development Patterns
- **Python (uv)**:
  - Exclusive use of `uv` for isolation and dependency syncing.
  - V2 Pydantic (`model_config`).
  - Isolated unit tests or CLI commands for logic debugging.
- **Web Frontend**:
  - `shrink-0` on sidebars; explicit backgrounds for sticky elements.
  - Defensive normalization for JSON imports.
- **Persistence**: Store data in `./data` at project root. Clean up test records after verification.

## 4. Testing & Verification
- **Workflow Coverage**: Minimum one E2E integration test per service.
- **LLM Mocking**: MANDATORY. Mock internal `_call_llm` to return response sequences.
- **CLI Verification**: Test entry points using `pytest` and `patch`.
- **Pre-Deployment**: `./scripts/pre_deploy_check.sh` is the source of truth for readiness.

## 5. Collaboration & Safety
- **Avoid Guesswork**: Provide 3 distinct style options if UI feedback is needed.
- **Passwords**: Always generate complex, unique random strings for new services.
- **Releases**: Monitor GitHub Actions for build integrity before marking a release as complete.
- **Documentation**: Use Mermaid diagrams, Tables, and clickable file links `[basename](file:///path)`.
