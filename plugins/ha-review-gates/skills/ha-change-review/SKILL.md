---
name: ha-change-review
description: Review Home Assistant changes for validation, dependency, and rollback coverage.
graph:
  generalizes_to:
    - ha-marketplace-orientation
  specializes_into:
    - ha-review-checklist
    - ha-backup-rollback
    - ha-destructive-operation-review
    - ha-security-review
  cross_references:
    - ha-mcp-tool-policy
    - ha-repo-refactor
    - ha-vibecode-deploy
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/safe-refactoring.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/yaml-only-integrations.md
---

# HA Change Review

## Checklist

- Files changed are listed.
- Entity references were scanned where relevant.
- Validation command is identified.
- Rollback path is documented.

## Safety

- Do not approve live deploys without backup and validation evidence.

