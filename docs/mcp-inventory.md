# Marketplace MCP Inventory

This file maps marketplace plugins to canonical MCP integrations and skill-pack handling. It is the cross-check between plugin purpose, upstream inventory, and opt-in MCP templates.

Codex starts MCP servers declared by an installed plugin manifest and also auto-discovers a root `.mcp.json` file. The Home Assistant MCP templates in this repository contain placeholder URLs and tokens, so they live under `docs/templates/` instead of plugin root. Copy the relevant template into local Codex or Claude configuration only after replacing placeholders with real values.

| Plugin | Canonical MCP or pack | Opt-in template | Transport | Runtime command or endpoint | Notes |
|---|---|---|---|---|---|
| `ha-foundation-skills` | Local curated skills, inspired by `homeassistant-ai/skills` categories | Shared setup script | Skill files and local script | `plugins/ha-foundation-skills/scripts/setup_ha_mcps.py` | Local safety baseline and canonical in-Codex setup for observer, builder, deployer, and full profiles. |
| `home-assistant-skills` | Canonical upstream `homeassistant-ai/skills` pack | Direct Git plugin source plus maintainer submodule | Skill files | `https://github.com/homeassistant-ai/skills.git` at `237ff71091b5b791e869334a65cc5d98641a8376` | Upstream MIT skill pack. Codex accepts its `.claude-plugin/plugin.json` manifest and default `skills/` directory. Marketplace name matches upstream plugin manifest. |
| `ha-context-official` | Official Home Assistant MCP Server | `plugins/ha-context-official/docs/templates/mcp.json` | HTTP | `home-assistant-official` at `http(s)://<host>/api/mcp` | Canonical official endpoint. Configure through the shared `ha-mcp-setup` workflow. |
| `ha-config-ha-mcp` | `homeassistant-ai/ha-mcp` | `plugins/ha-config-ha-mcp/docs/templates/mcp.json` | stdio and HTTP | `uvx ha-mcp@latest` or `${HA_MCP_URL}` | `uvx` stdio is the canonical local client template. The shared builder profile writes the HA URL and references `HOMEASSISTANT_TOKEN`; HTTP/add-on remains a manual template. |
| `ha-repo-poweruser` | Local stdlib repo scanner plus `ha-pilot` concept reference | None | Local scripts | `uv run python scripts/scan_ha_entity_refs.py` | `ha-pilot` repo was unavailable to inspect; no MCP template is shipped for it. |
| `ha-deploy-vibecode` | Coolver `@coolver/home-assistant-mcp` bridge to HA Vibecode Agent | `plugins/ha-deploy-vibecode/docs/templates/mcp.json` | stdio | `npx -y @coolver/home-assistant-mcp@latest` | Canonical deployer bridge uses `HA_AGENT_URL` and `HA_AGENT_KEY`. Opt in only when the HA-side agent is installed and reachable. |
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
