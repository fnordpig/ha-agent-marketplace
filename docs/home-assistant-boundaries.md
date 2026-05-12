# Home Assistant Boundaries

UI-managed `automations.yaml` is not a casual editing target. Prefer agent-managed files such as `automations/agent_*.yaml` and explicit includes.

YAML dashboards are better for agent-managed dashboard work because changes are reviewable. Storage-mode dashboards may live under `.storage` and should not be mutated unless a supported MCP tool exists and the user approves.

Config entries are integration-owned state. Prefer Home Assistant UI/API workflows over direct file edits.

Entity and device registries affect references across automations, scripts, dashboards, templates, packages, and docs. Scan dependencies before renaming or deleting entities.

`.storage` is internal Home Assistant state. Treat it as sensitive because malformed edits can break UI-managed configuration.

