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
    - ha-agent-operating-model
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

## BPMN Workflow

```mermaid
flowchart LR
  start((Change ready)) --> classify[Classify read/write/refactor/destructive/deploy]
  classify --> evidence[Collect files, tools, refs, validation, rollback]
  evidence --> risky{Risky or destructive?}
  risky -->|No| approve[Approve with notes]
  risky -->|Yes| specialist[Run destructive, security, or deploy review]
  specialist --> approval{Explicit approval?}
  approval -->|No| stop((Stop))
  approval -->|Yes| approve
  approve --> report[Report review result]
```

## Safety

- Do not approve live deploys without backup and validation evidence.
