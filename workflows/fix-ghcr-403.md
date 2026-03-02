---
description: Resolve GHCR 403 Forbidden/Permission Denied errors.
---

1. **Verify Error**: Check GitHub Actions logs for `403 Forbidden` on push.
2. **Identify Package**: Determine the package name and organization (e.g., `geonwprj/scape-novels`).
3. **Delete Ghost Package**:
   - Go to GitHub Org -> Packages.
   - Find the package.
   - Delete the entire package (mandatory if it wasn't linked properly).
4. **Re-run Action**: Re-run the failed GitHub Action job to re-create the package with correct permissions.
5. **Verify**: Ensure the image is now visible in the registry and the build PASSED.
