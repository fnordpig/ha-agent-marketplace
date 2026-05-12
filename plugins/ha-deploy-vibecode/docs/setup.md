# Vibecode Deployer Setup

This plugin references Coolver HA Vibecode Agent and `@coolver/home-assistant-mcp`.

Current bridge docs use:

```json
{
  "mcpServers": {
    "home-assistant": {
      "command": "npx",
      "args": ["-y", "@coolver/home-assistant-mcp@latest"],
      "env": {
        "HA_AGENT_URL": "http://<home-assistant-host>:8099",
        "HA_AGENT_KEY": "your_api_key_here"
      }
    }
  }
}
```

Never commit the real agent key. This is a high-privilege profile. The bundled `.mcp.json` is intentionally not auto-declared by the plugin manifest; enable it only after the HA-side Vibecode Agent is installed, reachable, and backed by an explicit deployment approval workflow.
