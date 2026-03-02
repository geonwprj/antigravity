---
name: managing-github-repos
description: "Strategic planning for GitHub repositories (visibility, licensing, CI/CD strategy). For actual execution, use `/init-repo` or `/fix-ghcr-403` workflows."
---

# Managing GitHub Repositories and Actions

## When to use this skill
- Planning the organization and CI/CD strategy for a new repository.
- Deciding on visibility, licensing, and metadata structures.
- For the actual **execution** of repo creation, use the `/init-repo` workflow.

## Workflow
For the step-by-step automated execution, refers to the following workflows:
- **Initialize Repo**: Use [init-repo.md](file:///home/srvadm/app/.agent/workflows/init-repo.md)
- **Fix GHCR 403**: Use [fix-ghcr-403.md](file:///home/srvadm/app/.agent/workflows/fix-ghcr-403.md)

### 1. Mandatory Metadata Standards
When planning a repo, ensuring the following:
- Organization: `geonwprj`
- Visibility: `Private`
- Essential Files: `.gitignore`, `.dockerignore`, `LICENSE`, `README.md`.

### 4. Verification & Metadata Reference
- [ ] **Authentication**: Use the PAT token from `~/app/.env` (variable `GITHUB_PAT`) for authentication if `gh` is not available.
    - [ ] Configure git to use the token: `git remote set-url origin https://genwch:<TOKEN>@github.com/geonwprj/<repo_name>.git`
- [ ] **Crucial Step**: If a repository name is being **reused**, check the **Packages** tab of the organization.
- [ ] If an existing package with the same name exists but is linked to a different (deleted) repo ID, it **MUST be manually deleted** before the first push.
- [ ] If 403 persists, check "Package creation" permissions in Organization Settings to ensure "Private" packages are enabled.

### 5. Mandatory Build Verification (CRITICAL)
- **NEVER** assume a release is successful just because the API call returned 201.
- **Verification Rule**: You MUST verify that the GitHub Action has started and reached a `success` state before notifying the user.
- **Anti-Hold Protocol (NO HANGS)**:
    - **Synchronous Checks Only**: NEVER background `curl` or `gh` commands for API lookups. Set `WaitMsBeforeAsync` to 10000 (10s) to force the tool to wait for completion.
    - **Proper Quoting**: Always quote URLs in `curl` (e.g., `curl "https://..."`) to prevent shell globbing of `?` or `&`.
    - **Timeouts**: Always use `--max-time 30` in `curl` to prevent hanging processes.
    - **Status Polling**: If a run is `in_progress`:
        1. Run the check once using a discrete `run_command` call (not `command_status` polling on the same ID, as the output is static).
        2. If still in progress, pause (using a no-op command or just waiting for the next turn) and then **re-issue** a new `run_command` to get the fresh status.
        3. Do NOT exceed 3 minutes of total blocked time without providing a progress update to the user.
    - **Dockerignore Check**: If the build fails with "file not found", check `.dockerignore` immediately for `uv.lock` or `pyproject.toml` exclusions.

## Instructions

### Handling 403 Forbidden Errors
When pushing to GHCR from an Action:
1.  **Orphaned Packages**: If you see `HEAD request to ...: 403 Forbidden`, it usually means the package name exists but is owned by a different internal repository ID.
    - **Fix**: Delete the package in the Web UI: `Organization -> Packages -> [Package Name] -> Settings -> Delete this package`.
2.  **Explicit Lowercase**: Always force the registry path to lowercase in the workflow:
    ```yaml
    images: ghcr.io/${{ github.repository }}
    ```
3.  **Permissions**: Ensure the job has `packages: write` in its `permissions` block.

### Standard Template Reference
Always refer to the successful `vod_hub` CI/CD structure. Documentation of this pattern can be found in `homelab_environment_and_preferences/artifacts/project_vod_hub.md`.

## Resources
- [Workflow Template](resources/github-actions-template.yml)
- [Dockerignore Template](resources/dockerignore-template)
- [License Template](resources/license-template)
- [README Template](resources/readme-template.md)
- [Managing Packages Help](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
