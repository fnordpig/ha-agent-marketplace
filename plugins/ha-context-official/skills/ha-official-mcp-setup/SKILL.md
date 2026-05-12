---
name: ha-official-mcp-setup
description: Use when setting up or repairing the official Home Assistant MCP connection in Codex.
---

# Official Home Assistant MCP Setup

Use this skill when the user wants to connect Codex to Home Assistant's official MCP Server integration.

## Workflow

1. Ask for the Home Assistant host if the user did not provide it.
2. Confirm whether it should use `http://host:8123` or `https://host`.
3. Run the setup script from inside Codex with `uv run python`.
4. Use `HOMEASSISTANT_TOKEN` as the bearer token environment variable unless the user requests another variable.
5. Tell the user to restart Codex and check `/mcp verbose`.

## Command

Resolve the script relative to this skill's plugin root. In this repository, run:

```bash
uv run python plugins/ha-context-official/scripts/setup_official_mcp.py homeassistant.local
```

When the plugin is installed from the marketplace cache, locate the loaded skill path and run the sibling plugin script at `../../scripts/setup_official_mcp.py` from this skill directory.

Use flags when needed:

```bash
uv run python plugins/ha-context-official/scripts/setup_official_mcp.py ha.example.com --https
uv run python plugins/ha-context-official/scripts/setup_official_mcp.py 192.168.1.10 --port 8123
uv run python plugins/ha-context-official/scripts/setup_official_mcp.py ha.example.com --dry-run
```

## Safety

- Do not ask the user to paste the token into chat.
- Do not write tokens into `config.toml`; write only `bearer_token_env_var`.
- Do not create plugin-root `.mcp.json`; Codex auto-starts that file.
- Do not enable broad configuration or deployment MCPs as part of this setup.
