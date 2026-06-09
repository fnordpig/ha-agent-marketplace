---
name: ha-mobile-dashboard
description: Design mobile Home Assistant dashboards for fast repeated use.
graph:
  generalizes_to:
    - ha-lovelace-yaml-dashboard
  specializes_into: []
  cross_references:
    - ha-agent-operating-model
    - ha-semantic-home-model
    - ha-helper-selection
    - ha-mcp-config-author
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/dashboard-guide.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/dashboard-cards.md
---

# HA Mobile Dashboard

## Guidance

- Use compact views for modes, rooms, people, and exceptions.
- Keep common actions reachable without raw entity dumps.
- Put high-frequency controls first and diagnostics behind navigation.
- Prefer scripts/scenes for multi-step mobile actions.

## Safety

- Do not add high-risk service buttons without confirmation flows or clear labels.
