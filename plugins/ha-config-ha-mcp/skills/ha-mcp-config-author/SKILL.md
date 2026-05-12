---
name: ha-mcp-config-author
description: Author Home Assistant configuration through ha-mcp with preview-first discipline.
---

# HA MCP Config Author

## Guidance

- Use ha-mcp for automations, scripts, helpers, dashboards, registry metadata, search, logs, traces, backups, and config checks.
- Prefer creating new agent-managed artifacts over mutating unclear legacy config.
- Always produce a diff-style summary before applying changes.

## Safety

- Treat broad write tools as high-risk.
- Do not remove devices, helpers, dashboards, or registry entries without dependency scan and explicit approval.

