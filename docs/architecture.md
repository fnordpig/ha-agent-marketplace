# Architecture

This marketplace is layered so users can choose the least privilege profile that fits the job.

1. Skills provide Home Assistant configuration judgment: native primitives first, helper selection, template safety, dependency scanning, and review checklists.
2. `ha-context-official` uses the official Home Assistant MCP Server boundary for exposed state/context and Assist-oriented tools.
3. `ha-config-ha-mcp` references `homeassistant-ai/ha-mcp` for broad configuration authoring, search, logs, traces, backups, and config checks.
4. `ha-repo-poweruser` supports repo-first YAML workflows with local stdlib scanners and layout helpers.
5. `ha-deploy-vibecode` references Coolver Vibecode Agent and its MCP bridge for high-privilege onboard deployment.
6. `ha-dashboard-designer` isolates dashboard design guidance.
7. `ha-review-gates` provides validation skills and conservative hook templates.

Upstream projects are integration references. They are not vendored.

