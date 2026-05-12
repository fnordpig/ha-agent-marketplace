---
name: ha-helper-selection
description: Select Home Assistant helpers for reusable and user-visible state.
---

# Home Assistant Helper Selection

## Guidance

- Use helpers when state should be visible, reusable, persisted, or dashboard-editable.
- Prefer `input_boolean` for modes/toggles and `input_select` for named house modes.
- Keep helper names generic and documented.

## Safety

- Do not delete helpers before scanning automations, scripts, scenes, dashboards, templates, packages, and docs.

