---
description: Automatically synchronize and update the System Manifest (map).
---

1. **Scan Tiers**:
   - T1: `/home/srvadm/.gemini/GEMINI.md`
   - T2: `/home/srvadm/.gemini/antigravity/knowledge/homelab_environment_and_preferences/artifacts/`
   - T3: `/home/srvadm/.gemini/antigravity/skills/`
   - T4: `/home/srvadm/.agent/workflows/`

2. **Extract Intelligence**:
   - Read the `description` from Skill/Workflow frontmatter.
   - Read the `# Header` and top-level headers from Knowledge artifacts.

3. **Re-generate Manifest**:
   - Update `system_manifest.md` with current file lists.
   - Ensure all links use absolute `file:///` URIs.
   - Maintain the 🏛️ Tiered categorical structure.

// turbo
4. **Final Sync**: Verify all links in the manifest are valid using `ls` or `view_file`.
