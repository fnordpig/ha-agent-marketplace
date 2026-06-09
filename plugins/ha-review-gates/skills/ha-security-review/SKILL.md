---
name: ha-security-review
description: Review Home Assistant agent changes for secrets and privilege boundaries.
graph:
  generalizes_to:
    - ha-change-review
    - ha-mcp-tool-policy
  specializes_into: []
  cross_references:
    - ha-agent-operating-model
    - ha-semantic-home-model
    - ha-mcp-setup
    - ha-live-deploy-safety
    - docs/security-model.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/safe-refactoring.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/yaml-only-integrations.md
---

# HA Security Review

## Checklist

- No real tokens, URLs, secrets, or personal entity names are committed.
- MCP tools match the requested privilege profile.
- Sensitive files are not edited casually.
- Voice exposure avoids private, security-sensitive, diagnostic, or non-actuable entities.
- Prompts and docs do not encode household-specific secrets, schedules, or presence details.

## Safety

- Do not expose `secrets.yaml`, long-lived tokens, agent keys, or private URLs in logs or docs.
