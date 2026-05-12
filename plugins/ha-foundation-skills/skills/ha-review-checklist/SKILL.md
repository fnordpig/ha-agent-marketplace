---
name: ha-review-checklist
description: Review Home Assistant configuration changes before approval or deployment.
graph:
  generalizes_to:
    - ha-change-review
  specializes_into: []
  cross_references:
    - ha-backup-rollback
    - ha-entity-refactor
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/safe-refactoring.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/yaml-only-integrations.md
---

# Home Assistant Review Checklist

## Checklist

- Does the change use native HA primitives before complex templates?
- Are new files agent-managed and clearly named?
- Were entity references scanned?
- Are backups, validation, and rollback notes present?

## Safety

- Do not approve destructive changes without explicit user approval.

