---
name: system-governance
description: Framework for maintaining the 4-tier documentation system. Use to audit, rearrange, and sync Global Rules, Knowledge, Skills, and Workflows.
---

# System Governance Framework

## Overview
This skill defines the operational logic for maintaining the Antigravity 4-Tier Architecture. It ensures that the system doesn't degrade into fragmentation or redundancy over time.

## Operational Logic

### 1. The Audit Cycle
Before creating new permanent documentation, perform a cross-tier audit:
- **Check T1 (GEMINI.md)**: Is this a mandatory mandate?
- **Check T2 (Knowledge)**: Is this a static technical truth?
- **Check T3 (Skills)**: Is this a behavioral pattern or planning framework?
- **Check T4 (Workflows)**: Is this a repetitive command-line routine?

### 2. Rearrangement Rules
- **Promotion**: If a recurring pattern is found in project-specific docs, promote it to T2 (Knowledge) or T4 (Workflows).
- **Consolidation**: If multiple T2 artifacts exist for the same domain, merge them into a high-density standard file.
- **Deprecation**: Mark overlapping or outdated T3 Skills as deprecated and redirect to the newer T4 Workflows.

### 3. Synchronization (Mandatory)
Every time a document in any of the four tiers is created, modified, or deleted, you **MUST** execute the `/sync-manifest` workflow immediately.

## Key Principles
- **DRY (Don't Repeat Yourself)**: Zero tolerance for overlapping instructions across tiers.
- **High Density**: Prefer fewer, richer files over many tiny ones.
- **Searchability**: All documents must be indexed in the [System Manifest](file:///home/srvadm/.gemini/system_manifest.md).
