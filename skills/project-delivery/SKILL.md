---
name: project-delivery
description: "Systematic project delivery## Workflow
1.  **Read Rules**: Read `GEMINI.md` and [homelab_standards.md](file:///home/srvadm/.gemini/antigravity/knowledge/homelab_environment_and_preferences/artifacts/homelab_standards.md).
2.  **Define Project**: Determine Project Name, Port Mapping (>20000), and primary Tech Stack.
3.  **Run Scaffolder**: Use the `/scaffold-fastapi` workflow for automated generation.
4.  **Verify**: Run `uv sync` and verify the `docker-compose.yml` and Swagger UI setup.
hroughs."
---

# Project Delivery Workflow

## Overview

A structured workflow for delivering projects and features efficiently. The core insight: **clarify all ambiguities upfront in a single batch, write a decision-oriented plan for user approval, then build and document**.

This skill replaces slow iterative questioning with focused, batched clarification — saving multiple round-trips while still ensuring complete alignment.

## When to Use This Skill
- Initiating a new project (FastAPI/Next.js) or a major feature.
- Ensuring a new service complies with [homelab_standards.md](file:///home/srvadm/.gemini/antigravity/knowledge/homelab_environment_and_preferences/artifacts/homelab_standards.md) (ports > 20000, `infra-net`).
- Setting up LLM audit logging or standardized project structures from Day 1.
- Any work where premature execution wastes time.

---

## Phase 1: Requirement Clarification

### Goal
Resolve all ambiguities **before** writing the plan. One focused message, not iterative back-and-forth.

### Process

1. **Research first** — Read the codebase, existing patterns, KIs, and user rules before asking anything
2. **Identify decision points** — List every ambiguity that would change the implementation:
   - Technology choices (framework, database, tools)
   - Architecture decisions (monolith vs. microservice, storage strategy)
   - Feature scope (what's in v1, what's deferred)
   - Configuration (ports, domains, auth)
3. **Batch all questions into one message** — Group related questions, use numbered list
4. **Use multiple-choice format** — For each question:
   - Provide 2-3 concrete options with labels (a, b, c)
   - Lead with the recommended option and a brief rationale
   - Include trade-offs so the user can make an informed choice
   - Allow open-ended input where choices can't be predetermined

### Question Design Principles

- **Multiple-choice > open-ended** — Faster for the user to respond
- **Independent questions only** — Don't ask Q2 if it depends on Q1's answer
- **Research-backed options** — Check existing codebase patterns before proposing alternatives
- **Actionable choices** — Each option should map to a clear implementation path
- **No more than 5-6 questions** — Prioritize; defer minor decisions to plan review

### Example Format

```
Before I draft the implementation plan, a few clarifying questions:

1. **Host mapping** — What host port? (MUST be > 20000, e.g. `28010:8000`)
2. **Frontend framework** — Would you prefer:
   - **(a) Next.js** — richer interactivity, aligned with `homelab_standards`
   - **(b) Jinja2 templates** — simpler, single-service deployment
3. **Storage** — For the data, would you prefer:
   - **(a) SQLite** — queryable, consistent with other projects
   - **(b) JSON files** — simpler, human-editable directly
4. **LLM Auditing** — If this uses LLMs, should I include the standard audit schema (Day 1 compliance)?
```

> [!TIP]
> **New Project Initialization**: If starting from scratch, use the `/scaffold-fastapi` workflow as your first execution step after the plan is approved.

---

## Phase 2: Implementation Plan

### Goal
A decision-oriented document that gives the user confidence to approve. **Not** a step-by-step executor script.

### Document Structure

```markdown
# [Goal Description]

Brief description of the problem, context, and what the change accomplishes.

## User Review Required

> [!IMPORTANT]
> Critical architecture decisions or breaking changes that need explicit approval.

> [!WARNING]
> Risks, limitations, or scope boundaries.

## Proposed Changes

### [Component Name 1]

Summary of what changes in this component.

#### [MODIFY/NEW/DELETE] [file.ext](file:///absolute/path/to/file.ext)
What this file does and why it's being changed.

---

### [Component Name 2]

...

---

## Verification Plan

### Automated Tests
- Exact commands to run
- Expected results

### Browser Verification
- URLs to check
- What to look for

### Manual Verification
- Steps for the user
```

### Writing Principles

- **Group by component** — Not by file type. "Backend", "Frontend", "Infra" > "Models", "Views", "Templates"
- **Dependencies first** — Order components so dependencies come before dependents
- **File links are mandatory** — Every file reference must be a clickable `[name](file:///path)` link
- **Use [NEW], [MODIFY], [DELETE] tags** — Immediately clear what's being created vs changed
- **User Review section only when needed** — Omit if there are no critical decisions
- **Alerts for critical items** — Use `> [!IMPORTANT]` and `> [!WARNING]` sparingly for things that genuinely need user attention
- **Tables for structured data** — API endpoints, file inventories, configuration values
- **Verification plan must be concrete** — Exact commands, exact URLs, expected output

### Anti-Patterns

- ❌ Don't write TDD step-by-step instructions (that's the executor's job)
- ❌ Don't include full code in the plan (it's a decision document, not a codebase)
- ❌ Don't explain basic concepts the user already knows
- ❌ Don't pad with obvious sub-steps ("Step 1: Create file. Step 2: Write code. Step 3: Save file.")
- ❌ Don't write the plan before clarifying ambiguities

---

## Phase 3: Execution

Not covered by this skill — use standard development practices. Key checkpoint:

- **If you discover unexpected complexity during execution**, return to Phase 2 and update the plan before continuing.

---

## Phase 4: Walkthrough Documentation

### Goal
Document what was accomplished with proof of work. Written **after** verification, not before.

### Document Structure

```markdown
# [Project Name] — Walkthrough

## Overview
One paragraph: what was built, tech stack, key ports/URLs.

## Architecture
Mermaid diagram showing component relationships and data flow.

## What Was Built

### [Component Name]
| File | Purpose |
|------|---------|
| [file.ext](file:///path) | Brief description |

### API Endpoints (if applicable)
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/v1/... | ... |

## Testing

### Unit Tests — N/N passed ✅
Summary of test coverage and results.

### Browser Verification ✅
Screenshots embedded via carousel:
- Swagger UI / API docs
- Frontend pages
- Key user flows

## How to Run

### Development (local)
Exact commands to start all services.

### Production
Exact commands for container deployment.

### Tests
Exact test command.
```

### Writing Principles — Visual-First Documentation

Follow the global **Homelab UI/UX** — **Consistency**: Follow [homelab_standards.md](file:///home/srvadm/.gemini/antigravity/knowledge/homelab_environment_and_preferences/artifacts/homelab_standards.md) for UI spacing, colors, and layouts.
hroughs specifically:

- **Architecture diagram is mandatory** — Use Mermaid for component relationships. Never describe architecture in prose.
- **File tables > file lists** — Two columns minimum: File (clickable link) + Purpose
- **Embed screenshots as proof** — Use `![caption](file:///path)` or carousels for multiple. Don't write "I verified that..." — show the screenshot instead.
- **Embed recordings** — If browser verification was recorded, include the `.webp`
- **Exact commands** — Copy-paste ready, no placeholders
- **Test results are numbers** — Show `26/26 passed ✅`, not "all tests passed"
- **Concise** — Skip narrative; this is a reference document, not a story

### What to Use Instead of Prose

| ❌ Don't write this | ✅ Use this instead |
|---------------------|---------------------|
| "The API server connects to the frontend which then..." | Mermaid `graph LR` diagram |
| "The project contains models.py for the database, engine.py for scraping, and..." | File table with `\| File \| Purpose \|` |
| "I verified the Swagger UI loads correctly with dark theme" | `![Swagger UI](file:///path/to/screenshot.png)` |
| "The following endpoints are available: GET profiles..." | API table with `\| Method \| Path \| Description \|` |
| "Run the following command to start the server" | Fenced code block with exact command |
| "All tests passed successfully" | `### Unit Tests — 26/26 passed ✅` |

---

## Complete Workflow Checklist

```markdown
## Phase 1: Clarify
- [ ] Research codebase, KIs, existing patterns
- [ ] Identify all decision points
- [ ] Batch questions into one focused message
- [ ] Wait for user input

## Phase 2: Plan
- [ ] Write implementation plan with proposed changes
- [ ] Include User Review section for critical decisions
- [ ] Include concrete verification plan
- [ ] Submit for user approval
- [ ] Incorporate feedback, re-submit if needed

## Phase 3: Execute
- [ ] Build components in dependency order
- [ ] Run tests continuously
- [ ] Return to Phase 2 if unexpected complexity found

## Phase 4: Document
- [ ] Run all verification (tests + browser)
- [ ] Write walkthrough with architecture diagram
- [ ] Embed screenshots/recordings as proof
- [ ] Deliver to user
```
