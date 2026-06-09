---
name: ha-mcp-setup
description: Use when setting up Home Assistant MCP profiles in Codex or Claude Code.
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

Use this skill when the user wants to configure one or more Home Assistant MCP servers. It works for both **Codex** (writes `config.toml`) and **Claude Code** (prints `claude mcp add-json` commands to run). Confirm which host you are setting up; if unknown, ask.

## Profiles

- `observer`: official HA MCP only, low-risk context/control.
- `builder`: official HA MCP plus `homeassistant-ai/ha-mcp` via `uvx`.
- `deployer`: Vibecode deployer only, high privilege.
- `full`: observer and builder by default; deployer only with `--include-deployer`.

## Command

The same script serves both hosts via `--client`. In this repository:

```bash
# Codex (default): writes ~/.codex/config.toml
uv run python plugins/ha-foundation-skills/scripts/setup_ha_mcps.py http://homeassistant:8123 --profile builder

# Claude Code: prints the `claude mcp add-json` commands to run
uv run python plugins/ha-foundation-skills/scripts/setup_ha_mcps.py http://homeassistant:8123 --profile builder --client claude
```

`--client claude` does not write any file; it emits the commands so the user can review and run them. When installed from marketplace cache, locate this skill path and run the sibling plugin script at `../../scripts/setup_ha_mcps.py` from this skill directory.

## Safety

- Do not ask the user to paste tokens into chat.
- Write only env var references, never token values.
- Do not create a plugin-root `.mcp.json`; both Codex and Claude Code auto-start that file on install.
- Do not enable deployer MCP unless the user explicitly asks for deployer/full with deployer.
- For builder setup, write the non-secret HA URL into config and require only `HOMEASSISTANT_TOKEN` in the environment after restart.
