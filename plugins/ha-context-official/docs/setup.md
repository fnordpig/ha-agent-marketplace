# Official Home Assistant MCP Setup

Use the Home Assistant MCP Server integration for the lowest-risk live profile.

Current HA docs describe a Streamable HTTP endpoint at:

```text
https://<your_home_assistant_url>/api/mcp
```

Authentication may use OAuth where supported or a long-lived access token. This plugin's MCP snippet lives at `docs/templates/mcp.json` and is intentionally not named `.mcp.json` at plugin root. Copy the snippet into your local client config (Codex `~/.codex/config.toml`, or Claude Code via `claude mcp add-json`) only after setting an absolute URL and real authentication.

## Guided Setup

Use the shared setup workflow (works for Codex and Claude Code):

```text
Set up Home Assistant MCPs for http://homeassistant:8123 with the observer profile.
```

The shared `ha-mcp-setup` skill runs:

```bash
# Codex (default): writes ~/.codex/config.toml
uv run python plugins/ha-foundation-skills/scripts/setup_ha_mcps.py http://homeassistant:8123 --profile observer

# Claude Code: prints the `claude mcp add-json` command to run
uv run python plugins/ha-foundation-skills/scripts/setup_ha_mcps.py http://homeassistant:8123 --profile observer --client claude
```

In Codex this writes a user-level `mcp_servers.home-assistant-official` entry with `bearer_token_env_var = "HOMEASSISTANT_TOKEN"`. In Claude Code it prints a `claude mcp add-json` command with the token as an env-var reference. Either way it does not write the token value and does not create a plugin-root `.mcp.json`. The official server also supports OAuth in Claude Code; see `docs/install-claude-code.md`.

Good for reading exposed state/context and low-risk control of explicitly exposed entities. Not ideal for full configuration authoring, repo refactoring, arbitrary YAML editing, or dashboard/storage mutation.
