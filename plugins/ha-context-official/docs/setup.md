# Official Home Assistant MCP Setup

Use the Home Assistant MCP Server integration for the lowest-risk live profile.

Current HA docs describe a Streamable HTTP endpoint at:

```text
https://<your_home_assistant_url>/api/mcp
```

Authentication may use OAuth where supported or a long-lived access token. This plugin's MCP snippet lives at `docs/templates/mcp.json` and is intentionally not named `.mcp.json` at plugin root. Copy the snippet into your local `~/.codex/config.toml` only after setting an absolute URL and real authentication.

## In-Codex Setup

Use the shared setup workflow:

```text
Set up Home Assistant MCPs for http://homeassistant:8123 with the observer profile.
```

The shared `ha-mcp-setup` skill runs:

```bash
uv run python plugins/ha-foundation-skills/scripts/setup_ha_mcps.py http://homeassistant:8123 --profile observer
```

The script writes a user-level `mcp_servers.home-assistant-official` entry with `bearer_token_env_var = "HOMEASSISTANT_TOKEN"`. It does not write the token value and does not create plugin-root `.mcp.json`.

Good for reading exposed state/context and low-risk control of explicitly exposed entities. Not ideal for full configuration authoring, repo refactoring, arbitrary YAML editing, or dashboard/storage mutation.
