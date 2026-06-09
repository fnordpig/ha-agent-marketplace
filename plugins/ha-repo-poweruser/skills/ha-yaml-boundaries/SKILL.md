---
name: ha-yaml-boundaries
description: Maintain clear boundaries between Home Assistant YAML and UI-managed config.
graph:
  generalizes_to:
    - ha-repo-refactor
  specializes_into: []
  cross_references:
    - ha-agent-operating-model
    - ha-semantic-home-model
    - ha-automation-author
    - ha-lovelace-yaml-dashboard
    - docs/home-assistant-boundaries.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/yaml-only-integrations.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/safe-refactoring.md
---

# HA YAML Boundaries

## Guidance

- Prefer packages, `automations/agent_*.yaml`, and YAML dashboards for agent-managed work.
- Treat UI-managed files as user-owned unless the workflow explicitly targets them.
- Use config flows or MCP config tools for helpers, groups, integrations, and registry metadata when available.
- Use managed YAML edits only for YAML-only integrations and record the reload or restart requirement.

## Safety

- Do not directly write UI-managed `automations.yaml` without user approval.
