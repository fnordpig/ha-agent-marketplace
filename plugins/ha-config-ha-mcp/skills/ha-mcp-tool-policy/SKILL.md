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
    - plugins/ha-config-ha-mcp/docs/tool-policy.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/safe-refactoring.md
---

# HA MCP Tool Policy

## Risk Classes

- Read: search, list, logs, traces, history.
- Write: automations, scripts, helpers, dashboards, registry metadata, files.
- Deploy: backups, restore, config check, reload, restart.

## Safety

- Do not call write or deploy tools without explaining intent and expected effect.
- Do not call delete/remove tools without explicit user approval after dependency scan.

