---
name: ha-mcp-config-author
description: Author Home Assistant configuration through ha-mcp with preview-first discipline.
graph:
  generalizes_to:
    - ha-marketplace-orientation
    - ha-mcp-setup
  specializes_into:
    - ha-mcp-tool-policy
    - ha-automation-author
    - ha-helper-selection
    - ha-template-safety
    - ha-entity-refactor
    - ha-change-review
  cross_references:
    - ha-agent-operating-model
    - ha-semantic-home-model
    - ha-voice-assist-grounding
    - home-assistant-best-practices
    - ha-repo-refactor
    - ha-lovelace-yaml-dashboard
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/automation-patterns.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/helper-selection.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/template-guidelines.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/safe-refactoring.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/dashboard-guide.md
---

# HA MCP Config Author

## Guidance

- Use ha-mcp for automations, scripts, helpers, dashboards, registry metadata, search, logs, traces, backups, and config checks.
- Classify the target object and risk before choosing a tool.
- Observe live state and existing config before proposing a write.
- Prefer creating new agent-managed artifacts over mutating unclear legacy config.
- Always produce a diff-style summary before applying changes.

## BPMN Workflow

```mermaid
flowchart LR
  start((Start)) --> classify[Classify object and risk]
  classify --> observe[Read state, config, history, logs, traces, or refs]
  observe --> primitive{Native HA primitive fits?}
  primitive -->|Yes| plan[Plan helper, script, scene, automation, dashboard, or config flow]
  primitive -->|No| justify[Justify template, YAML, or beta tool]
  plan --> diff[Produce diff-style summary]
  justify --> diff
  diff --> review{Write, refactor, or destructive?}
  review -->|No| answer[Answer with evidence]
  review -->|Yes| gate[Run tool policy and review gate]
  gate --> approval{Approval required and granted?}
  approval -->|No| stop((Stop))
  approval -->|Yes| apply[Apply supported MCP write]
  apply --> validate[Validate and report rollback]
  answer --> done((Done))
  validate --> done
```

## Safety

- Treat broad write tools as high-risk.
- Do not remove devices, helpers, dashboards, or registry entries without dependency scan and explicit approval.
