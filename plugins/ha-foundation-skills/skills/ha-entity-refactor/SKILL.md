---
name: ha-entity-refactor
description: Refactor Home Assistant entity references with dependency scanning.
graph:
  generalizes_to:
    - ha-mcp-config-author
    - ha-repo-refactor
  specializes_into:
    - ha-dependency-graph
  cross_references:
    - ha-agent-operating-model
    - ha-semantic-home-model
    - home-assistant-best-practices
    - ha-destructive-operation-review
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/safe-refactoring.md
---

# Home Assistant Entity Refactor

## Workflow

1. Search references across automations, scripts, scenes, dashboards, templates, helpers, packages, and docs.
2. Inspect device siblings and config-entry consumers before deciding scope.
3. Group references by entity.
4. Classify the operation as rename, hide, relabel, migrate, or delete.
5. Propose a diff before renaming or deleting anything.

## Operating Rules

- Prefer hide or alias when the target is uncertain.
- Rename all relevant device siblings together when identity changes.
- Re-scan old and new identifiers after the change.

## Safety

- Do not rename or delete an entity without dependency scan results and explicit approval.
