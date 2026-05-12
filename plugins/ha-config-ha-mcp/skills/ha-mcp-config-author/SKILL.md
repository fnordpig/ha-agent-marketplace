---
name: ha-mcp-config-author
description: Author Home Assistant configuration through ha-mcp with preview-first discipline.
graph:
  generalizes_to:
    - ha-marketplace-orientation
    - ha-mcp-setup
  specializes_into:
    - ha-mcp-tool-policy
    - ha-automation-author
    - ha-helper-selection
    - ha-template-safety
    - ha-entity-refactor
    - ha-change-review
  cross_references:
    - home-assistant-best-practices
    - ha-repo-refactor
    - ha-lovelace-yaml-dashboard
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/automation-patterns.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/helper-selection.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/template-guidelines.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/safe-refactoring.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/dashboard-guide.md
---

# HA MCP Config Author

## Guidance

- Use ha-mcp for automations, scripts, helpers, dashboards, registry metadata, search, logs, traces, backups, and config checks.
- Prefer creating new agent-managed artifacts over mutating unclear legacy config.
- Always produce a diff-style summary before applying changes.

## Safety

- Treat broad write tools as high-risk.
- Do not remove devices, helpers, dashboards, or registry entries without dependency scan and explicit approval.

