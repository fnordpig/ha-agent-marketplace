---
name: ha-wall-panel-dashboard
description: Design wall-panel Home Assistant dashboards for glanceable control.
graph:
  generalizes_to:
    - ha-lovelace-yaml-dashboard
  specializes_into: []
  cross_references:
    - ha-helper-selection
    - ha-mcp-config-author
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/dashboard-guide.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/dashboard-cards.md
---

# HA Wall Panel Dashboard

## Guidance

- Prioritize large state, room controls, exceptions, and mode changes.
- Keep touch targets clear and stable.
- Put critical alerts above routine controls.

## Safety

- Do not expose sensitive household details on always-visible screens unless requested.

