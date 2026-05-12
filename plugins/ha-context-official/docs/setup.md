# Official Home Assistant MCP Setup

Use the Home Assistant MCP Server integration for the lowest-risk live profile.

Current HA docs describe a Streamable HTTP endpoint at:

```text
https://<your_home_assistant_url>/api/mcp
```

Authentication may use OAuth where supported or a long-lived access token. This plugin's MCP snippet lives at `docs/templates/mcp.json` and is intentionally not named `.mcp.json` at plugin root. Copy the snippet into your local `~/.codex/config.toml` only after setting an absolute URL and real authentication.

Good for reading exposed state/context and low-risk control of explicitly exposed entities. Not ideal for full configuration authoring, repo refactoring, arbitrary YAML editing, or dashboard/storage mutation.
