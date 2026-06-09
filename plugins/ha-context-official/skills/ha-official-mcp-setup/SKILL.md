---
name: ha-official-mcp-setup
description: Use when setting up or repairing the official Home Assistant MCP connection in Codex or Claude Code.
graph:
  generalizes_to:
    - ha-mcp-setup
  specializes_into:
    - ha-official-mcp-context
  cross_references:
    - plugins/ha-context-official/scripts/setup_official_mcp.py
    - docs/mcp-inventory.md
---

# Official Home Assistant MCP Setup

Use this skill when the user wants to connect **Codex or Claude Code** to Home Assistant's official MCP Server integration.

## Workflow

1. Ask for the Home Assistant host if the user did not provide it.
2. Confirm whether it should use `http://host:8123` or `https://host`.
3. Confirm the target host (Codex or Claude Code); if unknown, ask.
4. Run the setup script with `uv run python`, adding `--client claude` for Claude Code.
5. Use `HOMEASSISTANT_TOKEN` as the bearer token environment variable unless the user requests another variable.
6. Tell the user to restart the host and confirm with `/mcp` (Codex: `/mcp verbose`).

## Command

Resolve the script relative to this skill's plugin root. In this repository, run:

```bash
# Codex (default): writes ~/.codex/config.toml
uv run python plugins/ha-context-official/scripts/setup_official_mcp.py homeassistant.local

# Claude Code: prints the `claude mcp add-json` command to run
uv run python plugins/ha-context-official/scripts/setup_official_mcp.py homeassistant.local --client claude
```

When the plugin is installed from the marketplace cache, locate the loaded skill path and run the sibling plugin script at `../../scripts/setup_official_mcp.py` from this skill directory.

Use flags when needed:

```bash
uv run python plugins/ha-context-official/scripts/setup_official_mcp.py ha.example.com --https
uv run python plugins/ha-context-official/scripts/setup_official_mcp.py 192.168.1.10 --port 8123
uv run python plugins/ha-context-official/scripts/setup_official_mcp.py ha.example.com --dry-run
```

The official server also supports OAuth in Claude Code; see `docs/install-claude-code.md` for that variant.

## Safety

- Do not ask the user to paste the token into chat.
- Do not write tokens into `config.toml`; write only `bearer_token_env_var` (Codex) or an env-var reference (Claude Code).
- Do not create a plugin-root `.mcp.json`; both Codex and Claude Code auto-start that file on install.
- Do not enable broad configuration or deployment MCPs as part of this setup.
