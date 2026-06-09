---
name: ha-template-safety
description: Review Home Assistant templates for maintainability and failure behavior.
graph:
  generalizes_to:
    - ha-automation-author
    - ha-mcp-config-author
  specializes_into: []
  cross_references:
    - ha-agent-operating-model
    - ha-semantic-home-model
    - home-assistant-best-practices
    - ha-helper-selection
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/template-guidelines.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/helper-selection.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/automation-patterns.md
---

# Home Assistant Template Safety

## Guidance

- Prefer native Home Assistant features before Jinja.
- Keep templates short, readable, and defensive about missing states.
- Use helpers or scripts when logic should be inspectable by users.
- Use templates for dynamic service data, messages, raw data transformation, or trigger context.
- Do not use templates to replace native numeric/state/time conditions, groups, threshold helpers, min/max helpers, schedules, or utility meters.
- Put persistent or dashboard-editable state into helpers, not template-local variables.

## Safety

- Do not introduce templates that hide destructive service calls or depend on undocumented entity names.
