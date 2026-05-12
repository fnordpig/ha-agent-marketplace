---
name: ha-yaml-boundaries
description: Maintain clear boundaries between Home Assistant YAML and UI-managed config.
---

# HA YAML Boundaries

## Guidance

- Prefer packages, `automations/agent_*.yaml`, and YAML dashboards for agent-managed work.
- Treat UI-managed files as user-owned unless the workflow explicitly targets them.

## Safety

- Do not directly write UI-managed `automations.yaml` without user approval.

