---
name: ha-destructive-operation-review
description: Review delete, remove, restart, and registry operations before execution.
graph:
  generalizes_to:
    - ha-change-review
    - ha-mcp-tool-policy
  specializes_into: []
  cross_references:
    - ha-agent-operating-model
    - ha-semantic-home-model
    - ha-entity-refactor
    - ha-live-deploy-safety
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/safe-refactoring.md
---

# HA Destructive Operation Review

## Review

- Identify the destructive operation.
- Identify affected entities, files, helpers, dashboards, and docs.
- Require explicit user approval.
- Prefer disable, hide, rename, or quarantine when deletion confidence is incomplete.
- Treat restarts, restores, registry removal, file deletion, and `.storage` edits as destructive.

## Safety

- Do not proceed on implied approval.
- Do not delete registry or `.storage` data casually.
