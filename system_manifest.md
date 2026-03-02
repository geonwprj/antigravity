# Antigravity System Manifest

This document serves as the **Index and Map** for the current documentation and behavioral architecture of the agent.

## 🏛️ Tier 1: Global Rules (Mandates)
Universal mandates that apply to every workspace.
- [GEMINI.md](file:///home/srvadm/.gemini/GEMINI.md): **Core Mandated Standards**. No localhost, accurate local timezone alignment, premium dark mode, `uv` sync, and Documentation Integrity.

---

## 📚 Tier 2: Knowledge (Technical Reference)
Static technical specifications, design systems, and historical archives.
- [homelab_standards.md](file:///home/srvadm/.gemini/antigravity/knowledge/homelab_environment_and_preferences/artifacts/homelab_standards.md): **Unified Technical Manual**. UI/UX, Infrastructure, Subnets, Testing patterns.
- [llm_integration_patterns.md](file:///home/srvadm/.gemini/antigravity/knowledge/homelab_environment_and_preferences/artifacts/llm_integration_patterns.md): Deep-dive into LLM call logic and audit schemas.
- [project_vod_hub.md](file:///home/srvadm/.gemini/antigravity/knowledge/homelab_environment_and_preferences/artifacts/project_vod_hub.md): Historical reference for successful CI/CD patterns.

---

## 🛠️ Tier 3: Skills (Behavioral Frameworks)
Logic frameworks for complex planning and decision-making.
- **project-delivery**: **The Default Workflow**. Batched clarification -> Planning -> Execution -> Walkthrough.
- **brainstorming**: Exploratory creative work and component refinement.
- **managing-github-repos**: Strategic repo planning and CI/CD setup.
- **planning**: Low-level TDD task generation.
- **debugging-container-deployments**: specialized container recovery logic.
- **error-handling-patterns**: Best practices for resilient code.
- **system-governance**: Framework for maintaining the 4-tier system integrity.

---

## ⚡ Tier 4: Workflows (Automated Routines)
Command-heavy routines for rapid execution. Triggerable from any workspace.
- `/sync-manifest`: Automatically synchronize and update this System Manifest.
- `/scaffold-fastapi`: Bootstrap a new project following all rules.
- `/init-repo`: Automatic GitHub repository and Action setup.
- `/release-service`: Managed version bump, tagging, and build monitoring.
- `/fix-ghcr-403`: Automated troubleshooting for GHCR permission errors.

---

## ⚖️ Assessment & Governance
This structure is maintained via the `/sync-manifest` workflow. Always follow the 4-tier compliance rule in GEMINI.md.
