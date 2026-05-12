# Implementation Notes

## Codex Schema Notes

Current Codex marketplace documentation says the only required plugin file is `.codex-plugin/plugin.json`. Optional bundled paths are declared from that manifest with fields such as `skills`, `mcpServers`, and `hooks`. Marketplace files live at `.agents/plugins/marketplace.json` and use `source: {"source": "local", "path": "./plugins/name"}` plus policy fields.

Current Codex source accepts marketplace authentication policies `ON_INSTALL` and `ON_USE`. The earlier prompt's `NONE` and `ON_FIRST_USE` names were normalized to current Codex values.

Codex docs show `hooks.json` at the plugin root. This repository keeps hook scripts in `plugins/ha-review-gates/hooks/` and references `./hooks/hooks.json` from the manifest.

Codex source inspection shows the plugin manifest loader also accepts `.claude-plugin/plugin.json`, and it discovers a default `skills/` directory even when the manifest does not declare a `skills` path. That makes `homeassistant-ai/skills` usable as a plugin submodule without modifying upstream files.

Codex source inspection also shows marketplace add and plugin source materialization use plain `git clone`, not recursive submodule checkout. Users cloning this marketplace from Git should run `git submodule update --init --recursive` or clone with `--recurse-submodules` if they want `plugins/homeassistant-ai-skills` populated.

Codex starts MCP servers declared through a plugin manifest. Because this scaffold intentionally ships placeholder MCP URLs and environment variables, the Home Assistant plugin manifests do not declare `mcpServers` by default. The `.mcp.json` files remain opt-in templates for users to copy into local config after replacing placeholders with real URLs, tokens, and installed server commands.

The MCP-backed plugins were bumped to `0.1.1` after removing manifest-level `mcpServers` so Codex does not reuse stale `0.1.0` plugin cache entries that still auto-started placeholder MCP servers.

Because Codex does not hydrate submodules during marketplace install, the `home-assistant-skills` marketplace entry uses a direct Git plugin source pinned to the upstream commit. The marketplace plugin name must match upstream `.claude-plugin/plugin.json` exactly, so it uses `home-assistant-skills` rather than the maintainer submodule directory name `homeassistant-ai-skills`.

## Claude Code Compatibility Notes

Claude Code is a secondary target. This scaffold provides shared skill content and Claude-oriented setup snippets, but it does not assume Codex marketplace metadata is directly installable by Claude Code.

## Upstream Conflicts Or Limits

The official Home Assistant MCP Server is context/control oriented through the Assist API and exposed entities. It is not a full configuration authoring layer.

The official Home Assistant MCP Client integration currently focuses on tools from external MCP servers; prompts, resources, sampling, and notifications may not be available depending on Home Assistant version.

The `mickek/ha-pilot` community post was available, but `https://github.com/mickek/ha-pilot.git` returned repository not found during local reference cloning. Its role is documented from the community discussion only.

Some comparative MCP servers are control-oriented or broad system-admin tools. They are not primary dependencies for this marketplace.

## Conservative Choices

No upstream code is vendored. `homeassistant-ai/skills` is exposed as a direct Git plugin source and also included as a Git submodule pinned by the superproject commit for maintainer review. `.mcp.json` files are templates and placeholders, not auto-started plugin servers. High-privilege tools are documented as opt-in and approval-gated.
