---
name: ha-lovelace-yaml-dashboard
description: Design maintainable Home Assistant Lovelace YAML dashboards.
graph:
  generalizes_to:
    - ha-marketplace-orientation
  specializes_into:
    - ha-mobile-dashboard
    - ha-wall-panel-dashboard
  cross_references:
    - ha-mcp-config-author
    - ha-yaml-boundaries
    - home-assistant-best-practices
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/dashboard-guide.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/dashboard-cards.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/safe-refactoring.md
---

# HA Lovelace YAML Dashboard

## Guidance

- Prefer YAML dashboards for agent-managed dashboards.
- Organize around rooms, people, modes, and exceptions.
- Avoid exotic custom cards unless the user asks for them.

## Safety

- Do not mutate storage-mode dashboards without supported tooling and approval.

