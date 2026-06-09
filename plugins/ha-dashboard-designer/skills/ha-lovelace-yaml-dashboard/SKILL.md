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
    - ha-agent-operating-model
    - ha-semantic-home-model
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
- Start from the semantic home model, not a raw entity dump.
- Use history/statistics only when they inform a decision or threshold.

## BPMN Workflow

```mermaid
flowchart LR
  start((Start)) --> job[Define dashboard job and user posture]
  job --> model[Map areas, devices, helpers, scripts, scenes, exceptions]
  model --> cards[Select built-in cards and sections]
  cards --> risk{Storage-mode or risky controls?}
  risk -->|Yes| review[Run review and approval gate]
  risk -->|No| draft[Draft YAML dashboard]
  review --> draft
  draft --> validate[Validate structure or screenshot where available]
  validate --> report[Report widgets, rationale, and rollback]
```

## Safety

- Do not mutate storage-mode dashboards without supported tooling and approval.
