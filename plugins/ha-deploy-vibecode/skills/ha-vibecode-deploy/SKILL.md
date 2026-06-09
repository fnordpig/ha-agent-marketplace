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
    - ha-agent-operating-model
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

## BPMN Workflow

```mermaid
flowchart LR
  start((Approved change)) --> plan[Write deploy plan]
  plan --> backup{Backup confirmed?}
  backup -->|No| stop1((Stop))
  backup -->|Yes| validation{Validation passed?}
  validation -->|No| stop2((Stop))
  validation -->|Yes| rollback{Rollback known?}
  rollback -->|No| stop3((Stop))
  rollback -->|Yes| approval{Explicit deploy approval?}
  approval -->|No| stop4((Stop))
  approval -->|Yes| deploy[Deploy through Vibecode MCP]
  deploy --> verify[Verify HA status]
  verify --> report[Report status and rollback]
```

## Safety

- Do not deploy unreviewed changes.
- Do not run destructive operations unless explicitly requested and confirmed.
