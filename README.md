# Home Assistant Agent Marketplace

`ha-agent-marketplace` is a Codex-first, Claude Code-compatible marketplace scaffold for Home Assistant configuration agents. It focuses on automations, helpers, scripts, dashboards, entity/device registry maintenance, repo refactoring, review gates, and safe deployment workflows.

It is not a casual device-control plugin pack, and it does not connect to a live Home Assistant instance by itself.

## Quick Start

For Codex, install from this repository marketplace once published:

```bash
npx codex-marketplace add fnordpig/ha-agent-marketplace --plugins --project
```

For Claude Code, use the shared `SKILL.md` content and the MCP snippets in `docs/install-claude-code.md`. Claude compatibility is documented conservatively; unsupported Claude plugin behavior is not assumed.

## Profiles

- Safe Observer: `ha-foundation-skills`, optional `home-assistant-skills`, `ha-context-official`
- Builder: `ha-foundation-skills`, optional `home-assistant-skills`, `ha-config-ha-mcp`, `ha-dashboard-designer`, `ha-review-gates`
- Power User: `ha-foundation-skills`, optional `home-assistant-skills`, `ha-config-ha-mcp`, `ha-repo-poweruser`, `ha-dashboard-designer`, `ha-review-gates`
- Live Deployer: `ha-foundation-skills`, optional `home-assistant-skills`, `ha-deploy-vibecode`, `ha-review-gates`
- Full Power: all plugins

## MCP And Skill Inventory

See `docs/mcp-inventory.md` for the canonical mapping between plugins and MCPs. The `ha-config-ha-mcp` plugin includes both `uvx ha-mcp@latest` and HTTP/add-on templates, but MCP templates are opt-in and are not auto-started by plugin install. Skill packs are handled as local curated skills plus the upstream `homeassistant-ai/skills` submodule.

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
python3 scripts/validate_marketplace.py
python3 scripts/validate_plugin_manifests.py
python3 scripts/lint_skills.py
python3 scripts/scan_ha_entity_refs.py --root examples/ha-config-repo --summary
```
