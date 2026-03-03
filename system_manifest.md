# Antigravity System Manifest

This document serves as the **Index and Map** for the current documentation and behavioral architecture of the agent.

## 🏛️ Tier 1: Global Rules (Mandates)
Universal mandates that apply to every workspace.
- [GEMINI.md](file:///home/srvadm/.gemini/GEMINI.md): **Core Mandated Standards**. No localhost, accurate local timezone alignment, premium dark mode, `uv` sync, standard relative exports, and Documentation Integrity.

---

## 📚 Tier 2: Knowledge (Technical Reference)
Static technical specifications, design systems, and historical archives.
- [homelab_standards.md](file:///home/srvadm/.gemini/antigravity/knowledge/homelab_environment_and_preferences/artifacts/homelab_standards.md): **Unified Technical Manual**. UI/UX, Infrastructure, Subnets, Testing patterns.
- [reference_implementation.md](file:///home/srvadm/.gemini/antigravity/knowledge/python_project_standards/artifacts/reference_implementation.md): **Python Project Standards**. Modular configs, `LoggerClient` (with `EmojiFormatter`), `FetchClient` abstractions, explicit module exports, and strict absolute package import structure.
- [llm_integration_patterns.md](file:///home/srvadm/.gemini/antigravity/knowledge/homelab_environment_and_preferences/artifacts/llm_integration_patterns.md): Deep-dive into LLM call logic and audit schemas.
- [project_vod_hub.md](file:///home/srvadm/.gemini/antigravity/knowledge/homelab_environment_and_preferences/artifacts/project_vod_hub.md): Historical reference for successful CI/CD patterns.

---

## 🛠️ Tier 3: Skills (Behavioral Frameworks)
Logic frameworks for complex planning and decision-making.
- **project-delivery**: **The Default Workflow**. Systematic project delivery including batched clarification, planning, execution, and walkthroughs.
- **brainstorming**: EXPLORATORY WORK ONLY. Use for deep creative exploration or refining single-component behavior.
- **managing-github-repos**: Strategic repo planning and CI/CD setup.
- **planning**: Low-level TDD task generation with comprehensive implementation plans.
- **debugging-container-deployments**: specialized container recovery logic for podman-compose setups.
- **error-handling-patterns**: Best practices for resilient code and graceful degradation.
- **system-governance**: Framework for maintaining the 4-tier documentation system integrity.
- **skill-creator**: Tool for generating new behavioral frameworks following core standards.

---

## ⚡ Tier 4: Workflows (Automated Routines)
Command-heavy routines for rapid execution. Triggerable from any workspace.
- [/sync-manifest](file:///home/srvadm/.agent/workflows/sync-manifest.md): Automatically synchronize and update the System Manifest.
- [/scaffold-fastapi](file:///home/srvadm/.agent/workflows/scaffold-fastapi.md): Bootstrap a new project following all rules.
- [/init-repo](file:///home/srvadm/.agent/workflows/init-repo.md): Automatic GitHub repository and Action setup.
- [/release-service](file:///home/srvadm/.agent/workflows/release-service.md): Managed version bump, tagging, and build monitoring.
- [/fix-ghcr-403](file:///home/srvadm/.agent/workflows/fix-ghcr-403.md): Automated troubleshooting for GHCR permission errors.
- [/set-locale](file:///home/srvadm/.agent/workflows/set-locale.md): Set the system locale to en_HK.UTF-8 and enable Chinese character support.

---

## ⚖️ Assessment & Governance
This structure is maintained via the `/sync-manifest` workflow. Always follow the 4-tier compliance rule in GEMINI.md.
