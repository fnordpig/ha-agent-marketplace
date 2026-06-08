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
/plugin install ha-foundation-skills@ha-agent-marketplace-claude-compat
```

See `docs/install-claude-code.md` for the full flow plus MCP snippets. MCP servers and review-gate hooks are opt-in on both hosts and are not auto-started by install.

## Profiles

- Safe Observer: `ha-foundation-skills`, optional `home-assistant-skills`, `ha-context-official`
- Builder: `ha-foundation-skills`, optional `home-assistant-skills`, `ha-config-ha-mcp`, `ha-dashboard-designer`, `ha-review-gates`
- Power User: `ha-foundation-skills`, optional `home-assistant-skills`, `ha-config-ha-mcp`, `ha-repo-poweruser`, `ha-dashboard-designer`, `ha-review-gates`
- Live Deployer: `ha-foundation-skills`, optional `home-assistant-skills`, `ha-deploy-vibecode`, `ha-review-gates`
- Full Power: all plugins

## MCP And Skill Inventory

See `docs/mcp-inventory.md` for the canonical mapping between plugins and MCPs. The `ha-config-ha-mcp` plugin includes both `uvx ha-mcp@latest` and HTTP/add-on templates, but MCP templates are opt-in and are not auto-started by plugin install. Skill packs are handled as local curated skills plus the upstream `homeassistant-ai/skills` submodule.

To connect Home Assistant MCPs from inside Codex, ask:

```text
Set up Home Assistant MCPs for http://homeassistant:8123 with the builder profile.
```

To choose the right plugin, MCP, skill, and safety gate for a task, use the orientation graph:

```text
/ha-marketplace-orientation inspect my automations for stale entity references
```

`homeassistant-ai/skills` is installed by Codex as a direct Git plugin source, pinned to the same upstream commit tracked by the maintainer submodule. The submodule at `plugins/homeassistant-ai-skills` is for local review and maintainer workflows. Clone with submodules when you want that local checkout populated:

```bash
git clone --recurse-submodules git@github.com:fnordpig/ha-agent-marketplace.git
```

## Environment Variables

Templates reference placeholders only:

- `HOMEASSISTANT_URL`
- `HOMEASSISTANT_TOKEN`
- `HA_MCP_URL`
- `HA_MCP_TOKEN`
- `HA_AGENT_URL`
- `HA_AGENT_KEY`

Never commit real values.

## Safety

Treat live deploy tools, registry changes, `.storage`, `secrets.yaml`, UI-managed `automations.yaml`, restarts, removals, and file deletion as sensitive. Live deployment requires backup, validation, a diff summary, rollback notes, and explicit approval.

## Validate

```bash
uv run python scripts/validate_marketplace.py
uv run python scripts/validate_plugin_manifests.py
uv run python scripts/lint_skills.py
uv run python scripts/scan_ha_entity_refs.py --root examples/ha-config-repo --summary
```
