---
name: ha-backup-rollback
description: Require backup and rollback coverage for Home Assistant changes.
graph:
  generalizes_to:
    - ha-change-review
    - ha-vibecode-deploy
  specializes_into: []
  cross_references:
    - ha-agent-operating-model
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
- Tie rollback to the exact scope: file diff, registry change, helper/config entry, dashboard, or full deployment.
- Prefer a reversible proposal over a live write when rollback is unclear.

## Safety

- Do not perform live deploys without backup confirmation, validation result, diff summary, and rollback path.
