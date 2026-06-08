# ha-mcp Setup

This plugin references `homeassistant-ai/ha-mcp`.

## Transport Modes

`ha-mcp` is **one server that can run in two places**. Pick one mode — do not enable both unless you deliberately want two separate HA config clients. Both templates live in `docs/templates/mcp.json`.

| Mode | Template entry | Where `ha-mcp` runs | Client config | Auth env vars |
|---|---|---|---|---|
| **stdio (local)** | `home-assistant-config-uvx` | Your agent host launches it on demand via `uvx ha-mcp@latest` | `command: uvx` | `HOMEASSISTANT_URL` + `HOMEASSISTANT_TOKEN` |
| **HTTP (server)** | `home-assistant-config-http` | A long-running `ha-mcp` server — most commonly the **ha-mcp Home Assistant add-on running inside HA**, or a standalone Docker container / reverse proxy | `type: http`, `url: ${HA_MCP_URL}` | `Bearer ${HA_MCP_TOKEN}` |

### The two URLs are not the same thing

- `HOMEASSISTANT_URL` → **Home Assistant itself** (e.g. `http://homeassistant:8123`). Used **only in stdio mode**, where `ha-mcp` runs on your machine and needs to know where HA is.
- `HA_MCP_URL` → **the `ha-mcp` server's own HTTP endpoint**. Used **only in HTTP mode**. When `ha-mcp` runs as the HA add-on it is *inside* HA, so this is the add-on-generated URL — you point at the add-on, not at `:8123/api/...`.

Other install models (Docker, webhook/proxy, the companion custom component for beta filesystem/YAML tools) all reduce to one of the two modes above.

Put real `HA_MCP_URL`, `HA_MCP_TOKEN`, `HOMEASSISTANT_URL`, and `HOMEASSISTANT_TOKEN` values in local client configuration or environment, never in this repo.

### Why the template is not `.mcp.json`

The bundled file is `docs/templates/mcp.json`, not a plugin-root `.mcp.json`, because both Claude Code and Codex auto-start a root MCP file on install. Keeping it under `docs/templates/` makes connection strictly opt-in: copy the entry you want into local config after replacing placeholders.

## In-Codex Setup

Use the shared builder profile:

```text
Set up Home Assistant MCPs for http://homeassistant:8123 with the builder profile.
```

The shared `ha-mcp-setup` skill runs:

```bash
uv run python plugins/ha-foundation-skills/scripts/setup_ha_mcps.py http://homeassistant:8123 --profile builder
```

This configures `home-assistant-official` and `home-assistant-config-uvx` (**stdio mode only**). The Home Assistant URL is written as non-secret MCP environment, and the token is referenced through `HOMEASSISTANT_TOKEN`.

The script does **not** configure HTTP mode. For the ha-mcp add-on / HTTP server, copy the `home-assistant-config-http` entry from `docs/templates/mcp.json` into local config and set `HA_MCP_URL` + `HA_MCP_TOKEN` yourself (see Transport Modes above).

For Claude Code, there is no in-host setup script — use the `claude mcp add-json` snippets in `docs/install-claude-code.md` with the same two transport modes.

## Current Upstream Notes

`homeassistant-ai/ha-mcp` 7.6.0 materially expands the builder profile:

- `ha_manage_pipeline` manages Assist pipelines.
- Config subentries are folded into `ha_get_integration`, `ha_config_set_helper`, and `ha_remove_helpers_integrations`.
- `ha_search` is the consolidated search surface.
- `ha_get_dashboard_screenshot` is available as a beta dashboard review aid.
- Upstream now includes per-tool approval policies and auto-backup behavior for write/destructive tool calls.

Keep this marketplace's review skills active anyway. Upstream safety controls reduce risk, but they do not replace human approval, dependency scans, or rollback notes for destructive Home Assistant changes.

## Skill Pack Handling

`homeassistant-ai/ha-mcp` may expose `homeassistant-ai/skills` content as MCP resources or resource-reading tools. This marketplace still ships local curated skills because not every client auto-loads MCP resources. Use upstream skills as optional runtime context and keep local skills as the safety baseline.
