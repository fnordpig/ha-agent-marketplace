# ha-mcp Setup

This plugin references `homeassistant-ai/ha-mcp`.

Observed install models include `uvx`, Docker, Home Assistant add-on, and a companion custom component for beta filesystem/YAML tools. Current docs use environment variables such as `HOMEASSISTANT_URL` and `HOMEASSISTANT_TOKEN` for local stdio mode, and add-on generated HTTP URLs for add-on mode.

The bundled `docs/templates/mcp.json` file includes two canonical templates. It is intentionally not named `.mcp.json` at plugin root because Codex starts root MCP files immediately:

- `home-assistant-config-uvx`: stdio launch with `uvx ha-mcp@latest`.
- `home-assistant-config-http`: HTTP/add-on/proxy endpoint using `HA_MCP_URL`.

Put real `HA_MCP_URL`, `HA_MCP_TOKEN`, `HOMEASSISTANT_URL`, and `HOMEASSISTANT_TOKEN` values in local client configuration or environment, never in this repo. Do not enable both HTTP and `uvx` entries unless you intentionally want two separate HA config MCP clients.

## In-Codex Setup

Use the shared builder profile:

```text
Set up Home Assistant MCPs for http://homeassistant:8123 with the builder profile.
```

The shared `ha-mcp-setup` skill runs:

```bash
uv run python plugins/ha-foundation-skills/scripts/setup_ha_mcps.py http://homeassistant:8123 --profile builder
```

This configures `home-assistant-official` and `home-assistant-config-uvx`. The Home Assistant URL is written as non-secret MCP environment, and the token is referenced through `HOMEASSISTANT_TOKEN`.

## Skill Pack Handling

`homeassistant-ai/ha-mcp` may expose `homeassistant-ai/skills` content as MCP resources or resource-reading tools. This marketplace still ships local curated skills because not every client auto-loads MCP resources. Use upstream skills as optional runtime context and keep local skills as the safety baseline.
