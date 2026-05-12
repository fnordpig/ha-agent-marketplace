---
name: ha-yaml-boundaries
description: Maintain clear boundaries between Home Assistant YAML and UI-managed config.
graph:
  generalizes_to:
    - ha-repo-refactor
  specializes_into: []
  cross_references:
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

## Safety

- Do not directly write UI-managed `automations.yaml` without user approval.

