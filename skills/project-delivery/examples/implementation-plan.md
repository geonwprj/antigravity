# Example: Implementation Plan

This is a real example showing the structure of an effective implementation plan from the Scrape Tools project.

---

## Key Elements That Make It Effective

### 1. Context Block (2-3 sentences)
```markdown
# Scrape Tools — Web Scraping Platform

A FastAPI backend + Next.js frontend project for configurable web scraping via CSS selectors.
Users maintain profiles (JSON rule sets keyed by root URL), then scrape pages either ad-hoc
or by referencing a profile+function.
```

### 2. User Review Section (only when needed)
```markdown
## User Review Required

> [!IMPORTANT]
> **Single Podman pod**: Both services run in one pod. Frontend connects via localhost:8000.

> [!WARNING]
> **No authentication** in v0.1.0. Private homelab use only.
```

### 3. Proposed Changes by Component
```markdown
### Backend — FastAPI (`src/scrape_tools/`)

#### [NEW] [models.py](file:///absolute/path/to/models.py)
SQLAlchemy ORM: Profile → Function → Selector with cascading deletes.

#### [NEW] [engine.py](file:///absolute/path/to/engine.py)
Core scraping logic: fetch, parse, replace, URL build.

---

### Frontend — Next.js (`web/`)

#### [NEW] [web/](file:///absolute/path/to/web/)
Pages: Dashboard, Profile list, Profile editor with live preview.
```

### 4. Tables for Structured Data
```markdown
| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | List all profiles |
| POST | `/` | Create profile |
| GET | `/{name}` | Get profile |
```

### 5. Concrete Verification Plan
```markdown
## Verification Plan

### Automated Tests
- `uv run pytest -v` (engine tests + API integration tests)

### Browser Verification
- Swagger UI at `http://<HOST_NAME>:28002/docs`
- Frontend at `http://<HOST_NAME>:28003`

### Manual Verification
- `podman-compose up -d` then check health
```

## Anti-Patterns to Avoid

| ❌ Don't | ✅ Do Instead |
|----------|---------------|
| Include full code blocks | Describe what each file does |
| Write TDD step-by-step | Describe components and their purpose |
| Ask "should I proceed?" | Submit plan for review with specific decisions |
| List files alphabetically | Group by component, dependencies first |
| Skip verification section | Always include exact test commands + URLs |
