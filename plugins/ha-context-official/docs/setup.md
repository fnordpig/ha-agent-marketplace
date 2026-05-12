# Official Home Assistant MCP Setup

Use the Home Assistant MCP Server integration for the lowest-risk live profile.

Current HA docs describe a Streamable HTTP endpoint at:

```text
https://<your_home_assistant_url>/api/mcp
```

Authentication may use OAuth where supported or a long-lived access token. This plugin's `.mcp.json` is a template. If Codex does not expand environment variables in bundled MCP URLs, copy the snippet into your local `~/.codex/config.toml` and set the real URL there.

Good for reading exposed state/context and low-risk control of explicitly exposed entities. Not ideal for full configuration authoring, repo refactoring, arbitrary YAML editing, or dashboard/storage mutation.

