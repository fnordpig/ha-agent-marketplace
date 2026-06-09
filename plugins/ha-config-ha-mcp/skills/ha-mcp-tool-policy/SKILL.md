---
name: ha-mcp-tool-policy
description: Classify ha-mcp tools by risk before reading, writing, or deploying.
graph:
  generalizes_to:
    - ha-mcp-config-author
  specializes_into:
    - ha-change-review
    - ha-destructive-operation-review
    - ha-security-review
  cross_references:
    - ha-agent-operating-model
    - ha-semantic-home-model
    - plugins/ha-config-ha-mcp/docs/tool-policy.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/safe-refactoring.md
---

# HA MCP Tool Policy

## Risk Classes

- Read: search, list, logs, traces, history.
- Write: automations, scripts, helpers, dashboards, registry metadata, files.
- Refactor: rename, reassign, relabel, consolidate, migrate, or replace.
- Destructive: delete, remove, disable, overwrite, restore, restart, or reboot.
- Deploy: backups, restore, config check, reload, restart.

## BPMN Workflow

```mermaid
flowchart LR
  start((Tool candidate)) --> classify{Risk class}
  classify -->|Read| allow[Use read tool and report privacy-sensitive evidence carefully]
  classify -->|Write| explain[Explain intent and expected effect]
  classify -->|Refactor| scan[Build dependency graph]
  classify -->|Destructive| destructive[Require explicit approval after dependency scan]
  classify -->|Deploy| deploy[Require backup, validation, rollback, approval]
  explain --> summary[Provide diff-style summary]
  scan --> summary
  destructive --> approval{Approved?}
  deploy --> approval
  summary --> approval
  approval -->|No| stop((Stop))
  approval -->|Yes| execute[Execute smallest safe tool call]
```

## Safety

- Do not call write or deploy tools without explaining intent and expected effect.
- Do not call delete/remove tools without explicit user approval after dependency scan.
