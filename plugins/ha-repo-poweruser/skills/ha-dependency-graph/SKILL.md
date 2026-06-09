---
name: ha-dependency-graph
description: Build dependency context before changing Home Assistant entities.
graph:
  generalizes_to:
    - ha-repo-refactor
    - ha-entity-refactor
  specializes_into: []
  cross_references:
    - ha-agent-operating-model
    - ha-semantic-home-model
    - plugins/ha-repo-poweruser/scripts/scan_ha_entity_refs.py
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/safe-refactoring.md
---

# HA Dependency Graph

## Guidance

- Scan references across YAML, JSON, Markdown, and templates.
- Report entity, file path, line number, and excerpt.
- Use findings to sequence safe changes.
- Combine local scans with live MCP searches when UI-managed dashboards, config entries, or registry metadata may contain references.
- Treat zero local references as incomplete evidence when the object is integration-owned or UI-managed.

## Safety

- Do not delete referenced entities or helpers without a migration plan.
