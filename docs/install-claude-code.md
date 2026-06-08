# Install With Claude Code

This marketplace ships a Claude Code catalog at `.claude-plugin/marketplace.json`, and every local plugin carries a `.claude-plugin/plugin.json` alongside its Codex manifest. The plugins install natively in Claude Code; Codex remains the primary author target but is no longer the only installable one.

## Add the marketplace and install plugins

From a clone of this repository (local source), or by repo reference once published:

```bash
# Local clone
/plugin marketplace add /path/to/ha-agent-marketplace
# or, once published to GitHub
/plugin marketplace add fnordpig/ha-agent-marketplace

/plugin marketplace list        # confirm "ha-agent-marketplace-claude-compat" is present
/plugin                         # browse the 8 plugins interactively
/plugin install ha-foundation-skills@ha-agent-marketplace-claude-compat
```

Restart Claude Code after installing so skills, commands, and any hooks are picked up.

Notes specific to Claude Code:

- Skills and the `/ha-marketplace-orientation` command are auto-discovered from each plugin's `skills/` and `commands/` directories.
- No plugin auto-starts an MCP server. MCP setup is opt-in via the templates in `docs/templates/` and the snippets below.
- `ha-review-gates` ships its warning hooks as an opt-in template at `hooks/templates/hooks.json`; Claude Code does **not** auto-register them. To use them, wire that file into your own hook configuration after confirming the referenced scripts exist.
- `home-assistant-skills` is the upstream `homeassistant-ai/skills` submodule; clone with `--recurse-submodules` if you install it from the local source.

## MCP server snippets

For the official Home Assistant MCP Server, current Home Assistant docs show Claude Code can add a remote HTTP MCP server with OAuth:

```bash
claude mcp add-json "HA" '{
  "type": "http",
  "url": "https://<your_home_assistant_url>/api/mcp",
  "oauth": {
    "clientId": "http://localhost:12345",
    "callbackPort": 12345
  }
}' --client-secret
```

For `homeassistant-ai/ha-mcp`, follow its current setup docs and use `HOMEASSISTANT_URL` and `HOMEASSISTANT_TOKEN` only in local client config.

For Coolver Vibecode, current bridge docs use `npx -y @coolver/home-assistant-mcp@latest` with `HA_AGENT_URL` and `HA_AGENT_KEY`.

