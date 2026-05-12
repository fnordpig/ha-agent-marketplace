---
name: ha-automation-author
description: Author maintainable Home Assistant automations using native primitives first.
graph:
  generalizes_to:
    - ha-mcp-config-author
  specializes_into:
    - ha-helper-selection
    - ha-template-safety
  cross_references:
    - home-assistant-best-practices
    - ha-yaml-boundaries
    - ha-review-checklist
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/automation-patterns.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/device-control.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/examples.yaml
---

# Home Assistant Automation Author

## Use When

Use when creating or reviewing automations.

## Guidance

- Prefer native triggers, conditions, scripts, scenes, helpers, and blueprints before complex Jinja.
- Prefer agent-managed files such as `automations/agent_*.yaml`.
- Keep aliases, IDs, descriptions, and modes explicit.

## Safety

- Do not directly edit UI-managed `automations.yaml` unless the user accepts that workflow.
- Do not deploy without backup, validation, diff summary, and rollback notes.

