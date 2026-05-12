# Marketplace MCP Inventory

This file maps marketplace plugins to canonical MCP integrations and skill-pack handling. It is the cross-check between plugin purpose, upstream inventory, and opt-in `.mcp.json` templates.

Codex starts MCP servers declared by an installed plugin manifest. The Home Assistant MCP templates in this repository contain placeholder URLs and tokens, so the plugin manifests do not declare `mcpServers` by default. Copy the relevant template into local Codex or Claude configuration only after replacing placeholders with real values.

| Plugin | Canonical MCP or pack | Opt-in template | Transport | Runtime command or endpoint | Notes |
|---|---|---|---|---|---|
| `ha-foundation-skills` | Local curated skills, inspired by `homeassistant-ai/skills` categories | None | Skill files | `plugins/ha-foundation-skills/skills/*/SKILL.md` | Local safety baseline maintained in this repository. |
| `home-assistant-skills` | Canonical upstream `homeassistant-ai/skills` pack | Direct Git plugin source plus maintainer submodule | Skill files | `https://github.com/homeassistant-ai/skills.git` at `237ff71091b5b791e869334a65cc5d98641a8376` | Upstream MIT skill pack. Codex accepts its `.claude-plugin/plugin.json` manifest and default `skills/` directory. Marketplace name matches upstream plugin manifest. |
| `ha-context-official` | Official Home Assistant MCP Server | `plugins/ha-context-official/.mcp.json` | HTTP | `${HOMEASSISTANT_URL}/api/mcp` | Canonical official endpoint. Use OAuth where client supports it; bearer-token template is for clients that support headers. Opt in only after setting an absolute URL. |
| `ha-config-ha-mcp` | `homeassistant-ai/ha-mcp` | `plugins/ha-config-ha-mcp/.mcp.json` | stdio and HTTP | `uvx ha-mcp@latest` or `${HA_MCP_URL}` | `uvx` stdio is the canonical local client template. HTTP covers add-on, web, Docker, or proxy mode. Opt in only after HA credentials are configured. |
| `ha-repo-poweruser` | Local stdlib repo scanner plus `ha-pilot` concept reference | None | Local scripts | `python3 scripts/scan_ha_entity_refs.py` | `ha-pilot` repo was unavailable to inspect; no MCP template is shipped for it. |
| `ha-deploy-vibecode` | Coolver `@coolver/home-assistant-mcp` bridge to HA Vibecode Agent | `plugins/ha-deploy-vibecode/.mcp.json` | stdio | `npx -y @coolver/home-assistant-mcp@latest` | Canonical deployer bridge uses `HA_AGENT_URL` and `HA_AGENT_KEY`. Opt in only when the HA-side agent is installed and reachable. |
| `ha-dashboard-designer` | Local dashboard skills; optional ha-mcp dashboard tools through `ha-config-ha-mcp` | None | Skill files | `plugins/ha-dashboard-designer/skills/*/SKILL.md` | Dashboard writes should go through repo files or `ha-config-ha-mcp`, not this plugin alone. |
| `ha-review-gates` | Local review skills and hook templates | None | Hooks/scripts | `plugins/ha-review-gates/hooks/hooks.json` | No MCP server; protects workflows around other plugins. |

## Skill Packs

Skill packs are handled as layered guidance, not hard dependencies.

1. The marketplace ships a small local curated pack in `ha-foundation-skills` so the scaffold is useful even without upstream checkout.
2. `homeassistant-ai/skills` is exposed to Codex as a direct Git plugin source so marketplace install does not depend on submodule hydration.
3. The repository also keeps `homeassistant-ai/skills` as a maintainer submodule at `plugins/homeassistant-ai-skills`.
4. Codex currently uses plain `git clone` for marketplace add and plugin source materialization. It does not run `git clone --recurse-submodules` or `git submodule update --init`, so the submodule is not the install path.
5. `homeassistant-ai/ha-mcp` may expose skills as MCP resources or resource-reading tools for clients that support them. Treat those as optional runtime context.
6. Local skills remain conservative safety overlays rather than trying to mirror every upstream skill.
