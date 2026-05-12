---
name: ha-mcp-setup
description: Use when setting up Home Assistant MCP profiles in Codex.
graph:
  generalizes_to:
    - ha-marketplace-orientation
  specializes_into:
    - ha-official-mcp-setup
    - ha-official-mcp-context
    - ha-mcp-config-author
    - ha-vibecode-deploy
  cross_references:
    - docs/mcp-inventory.md
    - plugins/ha-foundation-skills/scripts/setup_ha_mcps.py
---

# Home Assistant MCP Setup

Use this skill when the user wants to configure one or more Home Assistant MCP servers without leaving Codex.

## Profiles

- `observer`: official HA MCP only, low-risk context/control.
- `builder`: official HA MCP plus `homeassistant-ai/ha-mcp` via `uvx`.
- `deployer`: Vibecode deployer only, high privilege.
- `full`: observer and builder by default; deployer only with `--include-deployer`.

## Command

In this repository:

```bash
uv run python plugins/ha-foundation-skills/scripts/setup_ha_mcps.py http://homeassistant:8123 --profile builder
```

When installed from marketplace cache, locate this skill path and run the sibling plugin script at `../../scripts/setup_ha_mcps.py` from this skill directory.

## Safety

- Do not ask the user to paste tokens into chat.
- Write only env var references, never token values.
- Do not create plugin-root `.mcp.json`; Codex auto-starts that file.
- Do not enable deployer MCP unless the user explicitly asks for deployer/full with deployer.
- For builder setup, write the non-secret HA URL into config and require only `HOMEASSISTANT_TOKEN` in the environment after restart.
