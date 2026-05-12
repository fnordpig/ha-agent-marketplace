---
name: ha-mcp-tool-policy
description: Classify ha-mcp tools by risk before reading, writing, or deploying.
---

# HA MCP Tool Policy

## Risk Classes

- Read: search, list, logs, traces, history.
- Write: automations, scripts, helpers, dashboards, registry metadata, files.
- Deploy: backups, restore, config check, reload, restart.

## Safety

- Do not call write or deploy tools without explaining intent and expected effect.
- Do not call delete/remove tools without explicit user approval after dependency scan.

