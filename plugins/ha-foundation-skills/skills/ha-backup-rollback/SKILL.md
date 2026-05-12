---
name: ha-backup-rollback
description: Require backup and rollback coverage for Home Assistant changes.
graph:
  generalizes_to:
    - ha-change-review
    - ha-vibecode-deploy
  specializes_into: []
  cross_references:
    - ha-live-deploy-safety
    - docs/security-model.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/safe-refactoring.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/yaml-only-integrations.md
---

# Home Assistant Backup And Rollback

## Guidance

- Identify the backup or git commit before change.
- Record validation output.
- Document how to roll back each changed file or live deployment.

## Safety

- Do not perform live deploys without backup confirmation, validation result, diff summary, and rollback path.

