---
name: ha-agent-operating-model
description: Run Home Assistant MCP work through a least-privilege observe-review-apply loop.
graph:
  generalizes_to:
    - ha-marketplace-orientation
  specializes_into:
    - ha-semantic-home-model
    - ha-mcp-tool-policy
    - ha-change-review
    - ha-backup-rollback
  cross_references:
    - docs/teaching-home-assistant-mcp.md
    - docs/skill-knowledge-graph.md
    - docs/mcp-inventory.md
    - docs/security-model.md
---

# HA Agent Operating Model

Use this skill when a Home Assistant request spans more than one skill, MCP, or risk boundary.

## Work In This Order

1. Classify the request as observe, author, refactor, deploy, or teach.
2. Identify the target object: area, device, entity, helper, script, scene, automation, dashboard, config entry, registry, file, or deployment.
3. Pick the least-powerful profile and MCP that can answer the question.
4. Observe live state, repo references, history, logs, traces, or docs before proposing a change.
5. Build the semantic model before touching configuration.
6. Propose the smallest change with expected effects.
7. Route risky writes through review gates.
8. Apply only after approval when approval is required.
9. Validate with the right evidence.
10. Report files changed, MCP tools used, validation result, deploy status, and rollback path.

## BPMN Workflow

```mermaid
flowchart LR
  start((Start)) --> request[Receive HA task]
  request --> classify{Classify risk}
  classify -->|Read| observe[Observe with read tools]
  classify -->|Write| model[Model home/config graph]
  classify -->|Deploy| deployGate[Require deploy gate]
  observe --> answer[Answer with evidence]
  model --> propose[Propose smallest change]
  propose --> review{Risky?}
  review -->|No| apply[Apply approved write]
  review -->|Yes| gate[Run review gate]
  gate --> approved{Explicit approval?}
  approved -->|No| stop((Stop))
  approved -->|Yes| apply
  deployGate --> backup[Confirm backup and validation]
  backup --> approved
  apply --> validate[Validate behavior]
  validate --> report[Report outcome and rollback]
  answer --> report
  report --> done((Done))
```

## Operating Rules

- Prefer skills and read tools before write tools.
- Prefer Home Assistant APIs, config flows, and helpers before raw file edits.
- Prefer semantic labels, scripts, scenes, and helpers over broad domain wildcards.
- Prefer hiding, aliasing, or documenting confusing entities before deleting them.
- Treat history as evidence that needs domain interpretation.
- Treat tool availability as capability, not permission.
- Stop when the rollback path is unknown.

## Safety

- Do not skip dependency scans, review gates, backup checks, or explicit approval because a tool is available.
- Do not collapse observe, author, and deploy into one silent step.
