# ha-mcp Setup

This plugin references `homeassistant-ai/ha-mcp`.

Observed install models include `uvx`, Docker, Home Assistant add-on, and a companion custom component for beta filesystem/YAML tools. Current docs use environment variables such as `HOMEASSISTANT_URL` and `HOMEASSISTANT_TOKEN` for local stdio mode, and add-on generated HTTP URLs for add-on mode.

The bundled `.mcp.json` includes two canonical templates:

- `home-assistant-config-uvx`: stdio launch with `uvx ha-mcp@latest`.
- `home-assistant-config-http`: HTTP/add-on/proxy endpoint using `HA_MCP_URL`.

Put real `HA_MCP_URL`, `HA_MCP_TOKEN`, `HOMEASSISTANT_URL`, and `HOMEASSISTANT_TOKEN` values in local client configuration or environment, never in this repo.

## Skill Pack Handling

`homeassistant-ai/ha-mcp` may expose `homeassistant-ai/skills` content as MCP resources or resource-reading tools. This marketplace still ships local curated skills because not every client auto-loads MCP resources. Use upstream skills as optional runtime context and keep local skills as the safety baseline.
