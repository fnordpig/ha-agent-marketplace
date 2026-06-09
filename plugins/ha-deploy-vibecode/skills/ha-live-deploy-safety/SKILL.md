---
name: ha-live-deploy-safety
description: Enforce backup, validation, approval, and rollback for live HA deploys.
graph:
  generalizes_to:
    - ha-vibecode-deploy
  specializes_into:
    - ha-backup-rollback
    - ha-destructive-operation-review
  cross_references:
    - ha-agent-operating-model
    - ha-security-review
    - docs/security-model.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/safe-refactoring.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/yaml-only-integrations.md
---

# HA Live Deploy Safety

## Required Before Deploy

- Human-readable deployment plan.
- Backup confirmation.
- Config validation result.
- Rollback path.
- Explicit approval.

## Operating Rules

- Treat validation failure, missing backup, unknown rollback, or ambiguous approval as a stop condition.
- Verify the deployed behavior after the deploy tool returns success.
- Report the backup identifier or rollback source, not just "rollback available".

## Safety

- Do not restart, reboot, remove, or delete without user confirmation and dependency scan.
