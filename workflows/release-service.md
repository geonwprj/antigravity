---
description: Release a new version of a service with mandatory verification.
---

1. **Pre-Release**:
   ```bash
   ./scripts/pre_deploy_check.sh
   ```
2. **Versioning**: Update `pyproject.toml` or `package.json`.
3. **Commit & Tag**:
   ```bash
   git add . && git commit -m "feat: <desc>" && git push origin main
   git tag v0.x.x && git push origin v0.x.x
   ```
4. **GitHub Release**:
   - Use `gh release create v0.x.x --notes "Changelog"`.
// turbo
5. **Monitor Build**: Poll Actions API for completion.
6. **Verify GHCR**: Ensure `v0.x.x` and `latest` tags are present.
