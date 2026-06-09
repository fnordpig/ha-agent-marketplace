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
    - ha-agent-operating-model
    - ha-semantic-home-model
    - ha-voice-assist-grounding
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
- Choose `restart` for re-triggered timers, `queued` for ordered device sequences, and `parallel` for independent per-target actions.
- Use `entity_id` or area targets for durable automations; use `device_id` only when the upstream device trigger pattern requires it.
- Represent reusable human intents as scripts or scenes before wiring them to voice or dashboards.

## Safety

- Do not directly edit UI-managed `automations.yaml` unless the user accepts that workflow.
- Do not deploy without backup, validation, diff summary, and rollback notes.
