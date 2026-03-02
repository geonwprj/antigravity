---
description: Initialize a new GitHub repository with standard files and CI/CD.
---

1. **Plan & Prep**: Read [homelab_standards.md](file:///home/srvadm/.gemini/antigravity/knowledge/homelab_environment_and_preferences/artifacts/homelab_standards.md).
2. **Repo Creation**: Use `gh repo create <org>/<name> --public`.
3. **Standard Files**: Ensure `.gitignore`, `.dockerignore`, `LICENSE`, and `README.md` are present.
4. **CI/CD**: Create `.github/workflows/docker-publish.yml` following the org standard.
5. **Initial Commit**:
   ```bash
   git add .
   git commit -m "chore: initial commit"
   git push origin main
   ```
6. **Initial Release**: Trigger tag `v0.1.0` to start the build.
