# Implementation Notes

## Codex Schema Notes

Current Codex marketplace documentation says the only required plugin file is `.codex-plugin/plugin.json`. Optional bundled paths are declared from that manifest with fields such as `skills`, `mcpServers`, and `hooks`. Marketplace files live at `.agents/plugins/marketplace.json` and use `source: {"source": "local", "path": "./plugins/name"}` plus policy fields.

Current Codex source accepts marketplace authentication policies `ON_INSTALL` and `ON_USE`. The earlier prompt's `NONE` and `ON_FIRST_USE` names were normalized to current Codex values.

Codex docs show `hooks.json` at the plugin root. This repository keeps the hook template at `plugins/ha-review-gates/hooks/templates/hooks.json` (with the scripts in `plugins/ha-review-gates/hooks/`), and `ha-review-gates` does not declare the hooks path in either plugin manifest. The `templates/` subpath matters for Claude Code specifically: Claude Code auto-discovers and registers any `hooks/hooks.json` at a plugin root regardless of the manifest, so leaving the template at that path would silently re-enable the very hooks the opt-in design removed. Codex never auto-registers hooks not named in the manifest, so the relocation is transparent to Codex. A stale or incomplete plugin cache can otherwise make a missing hook script block every tool call before the agent can repair it. The hook template commands are fail-open for the same reason.

Codex source inspection shows the plugin manifest loader also accepts `.claude-plugin/plugin.json`, and it discovers a default `skills/` directory even when the manifest does not declare a `skills` path. That makes `homeassistant-ai/skills` usable as a plugin submodule without modifying upstream files.

Codex source inspection also shows marketplace add and plugin source materialization use plain `git clone`, not recursive submodule checkout. Users cloning this marketplace from Git should run `git submodule update --init --recursive` or clone with `--recurse-submodules` if they want `plugins/homeassistant-ai-skills` populated.

Codex starts MCP servers declared through a plugin manifest and auto-discovers a plugin-root `.mcp.json` file. Because this scaffold intentionally ships placeholder MCP URLs and environment variables, the Home Assistant plugin manifests do not declare `mcpServers`, and template files are stored under `docs/templates/mcp.json` rather than plugin root. Users copy those templates into local config after replacing placeholders with real URLs, tokens, and installed server commands.

The MCP-backed plugins were bumped to `0.1.2` after moving root `.mcp.json` templates so Codex does not reuse stale plugin cache entries that still auto-started placeholder MCP servers. `ha-context-official` was later bumped to `0.1.3` for the first in-Codex setup workflow. The canonical setup workflow now lives in `ha-foundation-skills` `0.1.1` as `ha-mcp-setup`, which can configure observer, builder, deployer, or full profiles from inside Codex.

`ha-review-gates` was bumped to `0.1.3` when hook auto-registration was removed from the manifest. The review skills remain normal plugin content; hooks remain local templates for users who explicitly opt in.

All seven local plugins were bumped one patch level when the dual-target `.claude-plugin/plugin.json` manifests were added (`ha-foundation-skills` 0.1.3, `ha-context-official` 0.1.5, `ha-config-ha-mcp` 0.1.4, `ha-repo-poweruser` 0.1.2, `ha-deploy-vibecode` 0.1.4, `ha-dashboard-designer` 0.1.2, `ha-review-gates` 0.1.4). The Codex and Claude manifests are kept at the same version per plugin; `ha-review-gates` 0.1.4 also reflects the hook-template relocation to `hooks/templates/`.

Because Codex does not hydrate submodules during marketplace install, the `home-assistant-skills` marketplace entry uses a direct Git plugin source pinned to the upstream commit. The marketplace plugin name must match upstream `.claude-plugin/plugin.json` exactly, so it uses `home-assistant-skills` rather than the maintainer submodule directory name `homeassistant-ai-skills`.

The local marketplace skills include `graph` frontmatter with `generalizes_to`, `specializes_into`, and `cross_references` edges. The upstream `home-assistant-skills` submodule is referenced as an external node but is not modified. `ha-foundation-skills` ships `/ha-marketplace-orientation` plus `ha-marketplace-orientation` as the top-level graph entry point.

## Claude Code Compatibility Notes

Claude Code is a secondary but now first-class target: the local plugins are directly installable by Claude Code, not only via shared skill content.

Two parallel catalogs are maintained, one per host, because the two tools read different files and source schemas:

- `.agents/plugins/marketplace.json` — Codex. Object-form sources (`{"source": "local", "path": "./plugins/name"}`), plus `policy`/`category` fields.
- `.claude-plugin/marketplace.json` — Claude Code. String-form relative sources, a required `owner` object, and a `metadata.description`. Validated clean by `claude plugin validate .` (one residual warning: the `homeassistant-ai-skills` submodule's own `.claude-plugin/plugin.json` has no `author`; it is upstream-pinned and intentionally not edited).

Each local plugin now ships both manifests side by side:

- `.codex-plugin/plugin.json` — Codex reads this; it carries the Codex-specific `interface` block (`capabilities`, `defaultPrompt`, display strings).
- `.claude-plugin/plugin.json` — Claude Code reads this; it is the standard Claude manifest (`name`, `version`, `description`, `author`, `license`, `keywords`). It deliberately omits `skills`/`commands` path fields and relies on Claude Code auto-discovery of the root `skills/` and `commands/` directories, since declaring a default path would risk double-registration. The two manifests are kept at the same `version`. The `homeassistant-ai-skills` plugin (the upstream submodule) already shipped only a `.claude-plugin/plugin.json`; it is unchanged.

Claude Code marketplace entries default to `strict: true`, which requires a `.claude-plugin/plugin.json` in each plugin folder. Without the per-plugin Claude manifests added here, six of the seven local plugins would fail to install under Claude Code. Codex is unaffected: it continues to read `.codex-plugin/plugin.json`, and the repo validators (`validate_marketplace.py`, `validate_plugin_manifests.py`) already accept either manifest path.

MCP servers remain opt-in templates under `docs/templates/` for both hosts; no plugin manifest declares `mcpServers`, so neither Codex nor Claude Code auto-starts a placeholder server on install. Review-gate hooks are opt-in via the `hooks/templates/` relocation described above.

## Upstream Conflicts Or Limits

The official Home Assistant MCP Server is context/control oriented through the Assist API and exposed entities. It is not a full configuration authoring layer.

The official Home Assistant MCP Client integration currently focuses on tools from external MCP servers; prompts, resources, sampling, and notifications may not be available depending on Home Assistant version.

The `mickek/ha-pilot` community post was available, but `https://github.com/mickek/ha-pilot.git` returned repository not found during local reference cloning. Its role is documented from the community discussion only.

Some comparative MCP servers are control-oriented or broad system-admin tools. They are not primary dependencies for this marketplace.

## Conservative Choices

No upstream code is vendored. `homeassistant-ai/skills` is exposed as a direct Git plugin source and also included as a Git submodule pinned by the superproject commit for maintainer review. MCP templates are placeholders under `docs/templates/`, not auto-started plugin servers. High-privilege tools are documented as opt-in and approval-gated.

## Reference Refresh 2026-06-08

The gitignored `reference/` checkouts were fast-forwarded on June 8, 2026. Material upstream changes observed:

- `homeassistant-ai/ha-mcp` advanced to 7.6.0 with per-tool approval policies, auto-backups for write/destructive calls, Assist pipeline management, config subentries folded into existing integration/helper tools, consolidated `ha_search`, dashboard screenshots, and expanded add-on/proxy setup.
- `homeassistant-ai/skills` advanced to `a695a02e18ad8e2fc45f71f6796252d32fa1dc30`; the marketplace pin and `plugins/homeassistant-ai-skills` submodule were updated to match. New guidance includes AppDaemon, helper/menu-flow, YAML-only integration, and marketplace metadata refinements.
- Coolver HA Vibecode Agent advanced to 2.10.47 and its MCP bridge to 3.2.31. The deployer docs now note standalone Docker mode and new read-context tools such as history/statistics, calendars, zones, repairs, and snapshot.
- `esphome-ratgdo` changed only in firmware startup sync/pre-commit maintenance. It is not part of the marketplace MCP inventory.
- `HA_MCP`, `hass-mcp`, and `tevonsb/homeassistant-mcp` had no new commits relative to the previous local reference snapshot.
