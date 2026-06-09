---
name: ha-repo-refactor
description: Refactor Home Assistant YAML repos with git-first reviewable changes.
graph:
  generalizes_to:
    - ha-marketplace-orientation
  specializes_into:
    - ha-dependency-graph
    - ha-yaml-boundaries
    - ha-entity-refactor
    - ha-review-checklist
  cross_references:
    - ha-agent-operating-model
    - ha-semantic-home-model
    - ha-mcp-config-author
    - plugins/ha-repo-poweruser/scripts/scan_ha_entity_refs.py
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/safe-refactoring.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/yaml-only-integrations.md
---

# HA Repo Refactor

## Guidance

- Work in agent-managed files where possible.
- Keep YAML includes obvious and documented.
- Run entity reference scans before moving or renaming entities.
- Treat repo state as incomplete when integrations are UI-managed or storage-backed.

## BPMN Workflow

```mermaid
flowchart LR
  start((Start)) --> scope[Identify repo-owned files and live-owned state]
  scope --> scan[Scan entity references]
  scan --> boundary{YAML-managed?}
  boundary -->|No| route[Route to UI/API/MCP config-flow path]
  boundary -->|Yes| plan[Plan reviewable file diff]
  route --> plan
  plan --> review[Review references, validation, rollback]
  review --> edit[Edit repo files]
  edit --> validate[Run repo and HA validation]
  validate --> report[Report files, references, and deploy readiness]
```

## Safety

- Do not edit secrets or `.storage`.
- Do not reload or deploy from repo work without validation and approval.
