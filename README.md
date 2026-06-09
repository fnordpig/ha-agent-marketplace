# Home Assistant Agent Marketplace

`ha-agent-marketplace` is a Codex-first, Claude Code-compatible marketplace scaffold for Home Assistant configuration agents. It focuses on automations, helpers, scripts, dashboards, entity/device registry maintenance, repo refactoring, review gates, and safe deployment workflows.

It is not a casual device-control plugin pack, and it does not connect to a live Home Assistant instance by itself.

## Quick Start

For Codex, install from this repository marketplace once published:

```bash
codex plugin marketplace add fnordpig/ha-agent-marketplace --ref main
codex plugin list --marketplace ha-agent-marketplace
codex plugin add ha-foundation-skills@ha-agent-marketplace
```

For Claude Code, the plugins install natively from the `.claude-plugin/marketplace.json` catalog:

```bash
/plugin marketplace add fnordpig/ha-agent-marketplace
/plugin install ha-foundation-skills@ha-agent-marketplace
```

See `docs/install-claude-code.md` for the full flow plus MCP snippets. MCP servers and review-gate hooks are opt-in on both hosts and are not auto-started by install.

## Profiles

- Safe Observer: `ha-foundation-skills`, optional `home-assistant-skills`, `ha-context-official`
- Builder: `ha-foundation-skills`, optional `home-assistant-skills`, `ha-config-ha-mcp`, `ha-dashboard-designer`, `ha-review-gates`
- Power User: `ha-foundation-skills`, optional `home-assistant-skills`, `ha-config-ha-mcp`, `ha-repo-poweruser`, `ha-dashboard-designer`, `ha-review-gates`
- Live Deployer: `ha-foundation-skills`, optional `home-assistant-skills`, `ha-deploy-vibecode`, `ha-review-gates`
- Full Power: all plugins

## MCP And Skill Inventory

`docs/mcp-inventory.md` is the canonical mapping of each plugin to its MCP integration and skill-pack handling. The essentials:

- **No MCP server is auto-started by install.** Every MCP template lives under `docs/templates/` with placeholder URLs/tokens; copy one into your local client config after filling in real values. `ha-config-ha-mcp` ships both a `uvx ha-mcp@latest` (stdio) and an HTTP/add-on template.
- **Skills** are local curated packs plus the upstream `homeassistant-ai/skills` pack (installed as the `home-assistant-skills` plugin).

Connecting the MCPs is opt-in and per-profile, and the setup path differs by host:

- **Codex** — ask the agent in natural language, e.g. `Set up Home Assistant MCPs for http://homeassistant:8123 with the builder profile.` (drives the `ha-mcp-setup` skill and `setup_ha_mcps.py`).
- **Claude Code** — use the `claude mcp add-json` snippets and templates in `docs/install-claude-code.md`.

To choose the right plugin, MCP, skill, and safety gate for a task, the orientation command works on **both hosts**:

```text
/ha-marketplace-orientation inspect my automations for stale entity references
```

For a curriculum-style explanation of how to teach and learn these layers, see `docs/teaching-home-assistant-mcp.md`.

The `home-assistant-skills` plugin is the upstream `homeassistant-ai/skills` pack, pinned to one upstream commit. Codex installs it from a direct Git source; Claude Code installs it from the local `./plugins/homeassistant-ai-skills` submodule. To populate that submodule for local review:

```bash
git clone --recurse-submodules git@github.com:fnordpig/ha-agent-marketplace.git
```

## Environment Variables

The MCP templates reference placeholders only — set the real values in your local MCP client config and never commit them. Which variables you need depends on the profile/MCP you opt into:

| Variable | Used by | What it is |
|---|---|---|
| `HOMEASSISTANT_URL` | `ha-config-ha-mcp` — `uvx ha-mcp@latest` (stdio) | Base URL of your HA instance, e.g. `http://homeassistant:8123`. |
| `HOMEASSISTANT_TOKEN` | `ha-config-ha-mcp` — `uvx ha-mcp@latest` (stdio) | Long-lived access token (HA → your user profile → Security → Long-lived access tokens). |
| `HA_MCP_URL` | `ha-config-ha-mcp` — HTTP mode | Endpoint of the `ha-mcp` **server**, typically the ha-mcp Home Assistant add-on (ha-mcp running *inside* HA), or a standalone container/proxy. Not the same as `HOMEASSISTANT_URL`. Unused in `uvx` stdio mode. |
| `HA_MCP_TOKEN` | `ha-config-ha-mcp` — HTTP mode | Bearer token for that `ha-mcp` HTTP server. |
| `HA_AGENT_URL` | `ha-deploy-vibecode` — `@coolver/home-assistant-mcp` | URL of the Coolver HA Vibecode Agent bridge. |
| `HA_AGENT_KEY` | `ha-deploy-vibecode` — `@coolver/home-assistant-mcp` | API key for the Vibecode Agent bridge. |

`ha-mcp` (the `ha-config-ha-mcp` plugin) runs in one of two transport modes — local `uvx` stdio vs an HTTP server such as the HA add-on — and that choice determines which variables apply. See `plugins/ha-config-ha-mcp/docs/setup.md` (**Transport Modes**) for the full explanation of stdio vs HTTP and the `HOMEASSISTANT_URL` vs `HA_MCP_URL` distinction.

The official Home Assistant MCP Server (`ha-context-official`) is reached at `https://<host>/api/mcp` and authenticates via OAuth in Claude Code — it does not use these tokens. See `docs/install-claude-code.md`.

## Safety

Treat live deploy tools, registry changes, `.storage`, `secrets.yaml`, UI-managed `automations.yaml`, restarts, removals, and file deletion as sensitive. Live deployment requires backup, validation, a diff summary, rollback notes, and explicit approval.

## Validate

```bash
uv run python scripts/validate_marketplace.py
uv run python scripts/validate_plugin_manifests.py
uv run python scripts/lint_skills.py
uv run python scripts/scan_ha_entity_refs.py --root examples/ha-config-repo --summary
```
