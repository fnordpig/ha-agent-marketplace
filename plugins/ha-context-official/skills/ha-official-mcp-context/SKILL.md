---
name: ha-official-mcp-context
description: Use the official Home Assistant MCP Server for exposed context and Assist tools.
graph:
  generalizes_to:
    - ha-marketplace-orientation
    - ha-mcp-setup
  specializes_into: []
  cross_references:
    - ha-agent-operating-model
    - ha-semantic-home-model
    - ha-voice-assist-grounding
    - ha-mcp-config-author
    - docs/home-assistant-boundaries.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/device-control.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/domain-docs.md
---

# Official Home Assistant MCP Context

## Good For

- Reading exposed state and context.
- Assist-oriented tools and low-risk control of explicitly exposed entities.
- Checking what a voice/Assist-facing client can see.

## Not Ideal For

- Full configuration authoring.
- Repo refactoring.
- Arbitrary YAML or dashboard mutation.

## BPMN Workflow

```mermaid
flowchart LR
  start((Start)) --> exposed[Inspect exposed context]
  exposed --> enough{Question answerable from exposed context?}
  enough -->|Yes| answer[Answer or control exposed target]
  enough -->|No| escalate[Route to semantic model or ha-mcp config author]
  answer --> sensitive{Security-sensitive?}
  sensitive -->|Yes| confirm[Require confirmation or report limitation]
  sensitive -->|No| report[Report result]
  confirm --> report
  escalate --> report
```

## Safety

- Do not assume hidden entities are available.
- Do not use this profile as proof that configuration files are safe to edit.
