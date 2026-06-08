# Vibecode Deployer Setup

This plugin references Coolver HA Vibecode Agent and `@coolver/home-assistant-mcp`.

Current upstream versions inspected from `reference/` are HA Vibecode Agent `2.10.47` and MCP bridge `3.2.31`. The agent supports two HA-side deployment modes:

- Home Assistant Supervisor add-on for HAOS/Supervised installs.
- Standalone Docker for Home Assistant Container, Proxmox, NAS, or other non-Supervisor installs.

Both modes expose the same core agent API. Supervisor-only features, such as managing Home Assistant add-ons/apps, are not expected to work from standalone Docker.

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

Never commit the real agent key. This is a high-privilege profile. The bundled MCP template lives at `docs/templates/mcp.json` and is intentionally not named `.mcp.json` at plugin root; enable it only after the HA-side Vibecode Agent is installed, reachable, and backed by an explicit deployment approval workflow.

Recent upstream capabilities include history/statistics reads, calendars, zones, repair issues, a filtered whole-home snapshot endpoint, and standalone Docker setup. These improve deployer context, but do not change this marketplace's policy: live deploy, restart, rollback, delete, and broad write operations require a human-readable plan, validation result, backup/restore path, and explicit approval.
