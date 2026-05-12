---
name: ha-helper-selection
description: Select Home Assistant helpers for reusable and user-visible state.
graph:
  generalizes_to:
    - ha-automation-author
    - ha-mcp-config-author
  specializes_into: []
  cross_references:
    - home-assistant-best-practices
    - ha-entity-refactor
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/helper-selection.md
---

# Home Assistant Helper Selection

## Guidance

- Use helpers when state should be visible, reusable, persisted, or dashboard-editable.
- Prefer `input_boolean` for modes/toggles and `input_select` for named house modes.
- Keep helper names generic and documented.

## Safety

- Do not delete helpers before scanning automations, scripts, scenes, dashboards, templates, packages, and docs.

