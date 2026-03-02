---
description: Scaffold a new FastAPI project with homelab standards.
---

1. **Prerequisites**: Check [homelab_standards.md](file:///home/srvadm/.gemini/antigravity/knowledge/homelab_environment_and_preferences/artifacts/homelab_standards.md).
// turbo
2. **Run Scaffolder**:
   ```bash
   npx gen-fastapi ./ --name <project> --port <port>
   ```
3. **Dependency Sync**:
   ```bash
   uv sync
   ```
4. **Verification**:
   - Check `docker-compose.yml`.
   - Access Swagger UI at `http://dev02.geonw.local:<port>/api/v1/docs`.
