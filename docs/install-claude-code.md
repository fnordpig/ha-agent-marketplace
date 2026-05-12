# Install With Claude Code

Claude Code compatibility is provided through shared `SKILL.md` content and documented MCP snippets. Codex marketplace metadata is the primary format.

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

