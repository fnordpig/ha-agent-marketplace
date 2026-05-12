# Marketplace MCP Inventory

This file maps marketplace plugins to canonical MCP integrations and skill-pack handling. It is the cross-check between plugin purpose, upstream inventory, and bundled `.mcp.json` templates.

| Plugin | Canonical MCP or pack | Bundled template | Transport | Runtime command or endpoint | Notes |
|---|---|---|---|---|---|
| `ha-foundation-skills` | Local curated skills, inspired by `homeassistant-ai/skills` categories | None | Skill files | `plugins/ha-foundation-skills/skills/*/SKILL.md` | No upstream skills are copied. Upstream pack is optional reference. |
| `ha-context-official` | Official Home Assistant MCP Server | `plugins/ha-context-official/.mcp.json` | HTTP | `${HOMEASSISTANT_URL}/api/mcp` | Canonical official endpoint. Use OAuth where client supports it; bearer-token template is for clients that support headers. |
| `ha-config-ha-mcp` | `homeassistant-ai/ha-mcp` | `plugins/ha-config-ha-mcp/.mcp.json` | stdio and HTTP | `uvx ha-mcp@latest` or `${HA_MCP_URL}` | `uvx` stdio is the canonical local client template. HTTP covers add-on, web, Docker, or proxy mode. |
| `ha-repo-poweruser` | Local stdlib repo scanner plus `ha-pilot` concept reference | None | Local scripts | `python3 scripts/scan_ha_entity_refs.py` | `ha-pilot` repo was unavailable to inspect; no MCP template is shipped for it. |
| `ha-deploy-vibecode` | Coolver `@coolver/home-assistant-mcp` bridge to HA Vibecode Agent | `plugins/ha-deploy-vibecode/.mcp.json` | stdio | `npx -y @coolver/home-assistant-mcp@latest` | Canonical deployer bridge uses `HA_AGENT_URL` and `HA_AGENT_KEY`. |
| `ha-dashboard-designer` | Local dashboard skills; optional ha-mcp dashboard tools through `ha-config-ha-mcp` | None | Skill files | `plugins/ha-dashboard-designer/skills/*/SKILL.md` | Dashboard writes should go through repo files or `ha-config-ha-mcp`, not this plugin alone. |
| `ha-review-gates` | Local review skills and hook templates | None | Hooks/scripts | `plugins/ha-review-gates/hooks/hooks.json` | No MCP server; protects workflows around other plugins. |

## Skill Packs

Skill packs are handled as layered guidance, not hard dependencies.

1. The marketplace ships a small local curated pack in `ha-foundation-skills` so the scaffold is useful offline and without upstream installation.
2. `homeassistant-ai/skills` is documented as the canonical upstream Home Assistant skill pack. It is not vendored.
3. `homeassistant-ai/ha-mcp` may expose skills as MCP resources or resource-reading tools for clients that support them. Treat those as optional runtime context, not a replacement for the local curated skills.
4. If a user installs an upstream skill pack separately, local skills should remain conservative safety overlays rather than trying to mirror every upstream skill.

