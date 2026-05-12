---
name: ha-vibecode-deploy
description: Deploy approved Home Assistant changes through a Vibecode-style agent.
graph:
  generalizes_to:
    - ha-marketplace-orientation
    - ha-mcp-setup
  specializes_into:
    - ha-live-deploy-safety
    - ha-backup-rollback
    - ha-change-review
  cross_references:
    - docs/security-model.md
    - plugins/ha-deploy-vibecode/docs/rollback.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/safe-refactoring.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/yaml-only-integrations.md
---

# HA Vibecode Deploy

## Workflow

1. Summarize the approved change.
2. Confirm backup and validation.
3. Request explicit deploy approval.
4. Deploy through the configured MCP only after approval.
5. Report status and rollback path.

## Safety

- Do not deploy unreviewed changes.
- Do not run destructive operations unless explicitly requested and confirmed.

