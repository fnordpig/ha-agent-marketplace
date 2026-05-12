# Implementation Notes

## Codex Schema Notes

Current Codex marketplace documentation says the only required plugin file is `.codex-plugin/plugin.json`. Optional bundled paths are declared from that manifest with fields such as `skills`, `mcpServers`, and `hooks`. Marketplace files live at `.agents/plugins/marketplace.json` and use `source: {"source": "local", "path": "./plugins/name"}` plus policy fields.

Codex docs show `hooks.json` at the plugin root. This repository keeps hook scripts in `plugins/ha-review-gates/hooks/` and references `./hooks/hooks.json` from the manifest.

## Claude Code Compatibility Notes

Claude Code is a secondary target. This scaffold provides shared skill content and Claude-oriented setup snippets, but it does not assume Codex marketplace metadata is directly installable by Claude Code.

## Upstream Conflicts Or Limits

The official Home Assistant MCP Server is context/control oriented through the Assist API and exposed entities. It is not a full configuration authoring layer.

The official Home Assistant MCP Client integration currently focuses on tools from external MCP servers; prompts, resources, sampling, and notifications may not be available depending on Home Assistant version.

The `mickek/ha-pilot` community post was available, but `https://github.com/mickek/ha-pilot.git` returned repository not found during local reference cloning. Its role is documented from the community discussion only.

Some comparative MCP servers are control-oriented or broad system-admin tools. They are not primary dependencies for this marketplace.

## Conservative Choices

No upstream code is vendored. `.mcp.json` files are templates and placeholders. High-privilege tools are documented as opt-in and approval-gated.

