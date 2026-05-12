---
name: ha-entity-refactor
description: Refactor Home Assistant entity references with dependency scanning.
---

# Home Assistant Entity Refactor

## Workflow

1. Search references across automations, scripts, scenes, dashboards, templates, helpers, packages, and docs.
2. Group references by entity.
3. Propose a diff before renaming or deleting anything.

## Safety

- Do not rename or delete an entity without dependency scan results and explicit approval.

