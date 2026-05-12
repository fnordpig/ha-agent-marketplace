---
name: ha-dependency-graph
description: Build dependency context before changing Home Assistant entities.
---

# HA Dependency Graph

## Guidance

- Scan references across YAML, JSON, Markdown, and templates.
- Report entity, file path, line number, and excerpt.
- Use findings to sequence safe changes.

## Safety

- Do not delete referenced entities or helpers without a migration plan.

