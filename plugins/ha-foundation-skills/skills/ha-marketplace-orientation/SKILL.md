---
name: ha-marketplace-orientation
description: Orient Home Assistant marketplace work using the local skill knowledge graph.
graph:
  generalizes_to: []
  specializes_into:
    - ha-mcp-setup
    - ha-official-mcp-context
    - ha-mcp-config-author
    - ha-repo-refactor
    - ha-lovelace-yaml-dashboard
    - ha-vibecode-deploy
    - ha-change-review
  cross_references:
    - home-assistant-best-practices
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/automation-patterns.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/helper-selection.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/safe-refactoring.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/device-control.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/dashboard-guide.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/template-guidelines.md
    - docs/skill-knowledge-graph.md
    - docs/mcp-inventory.md
    - plugins/ha-config-ha-mcp/docs/setup.md
---

# Home Assistant Marketplace Orientation

Use this skill first when the user asks what Home Assistant marketplace skill, MCP, upstream best-practice reference, or workflow applies to a task.

This is the map skill. It does not replace the narrower skills or the upstream `home-assistant-best-practices` pack; it routes to them.

## Hub Skills

| Hub | Use when | Load next | Upstream grounding |
|---|---|---|
| Setup and profile selection | Connecting Codex to Home Assistant or choosing observer/builder/deployer/full | `ha-mcp-setup` | `docs/mcp-inventory.md` |
| Live context and simple control | Reading exposed state or using Assist-oriented controls | `ha-official-mcp-context` | `device-control.md`, `domain-docs.md` |
| Config authoring through MCP | Creating or editing automations, helpers, scripts, dashboards, registry metadata, or config checks through `ha-mcp` | `ha-mcp-config-author`, then `ha-mcp-tool-policy` | `automation-patterns.md`, `helper-selection.md`, `template-guidelines.md`, `device-control.md` |
| Repo-first refactor | Working in a Git/YAML Home Assistant config repo | `ha-repo-refactor`, then `ha-dependency-graph` and `ha-yaml-boundaries` | `safe-refactoring.md`, `yaml-only-integrations.md` |
| Dashboard design | Designing Lovelace, mobile, or wall-panel dashboards | `ha-lovelace-yaml-dashboard`, `ha-mobile-dashboard`, or `ha-wall-panel-dashboard` | `dashboard-guide.md`, `dashboard-cards.md` |
| Live deployment | Deploying approved changes or using a Vibecode-style deployer | `ha-vibecode-deploy`, then `ha-live-deploy-safety` | `safe-refactoring.md`, `yaml-only-integrations.md` |
| Review and safety gates | Reviewing any write, delete, restart, registry edit, secret exposure, or deploy | `ha-change-review`, `ha-destructive-operation-review`, or `ha-security-review` | `safe-refactoring.md` |

## Upstream Subdomain Map

`home-assistant-best-practices` is a dense upstream hub, not a leaf. Route into its references when the task needs detailed grounding:

| Upstream node | Use when |
|---|---|
| `automation-patterns.md` | Native triggers, conditions, waits, automation modes, trigger IDs, disabling automations, removed person/device triggers. |
| `helper-selection.md` | Choosing min/max, statistics, derivative, threshold, utility_meter, history_stats, integration, input helpers, counters, timers, schedules, groups. |
| `safe-refactoring.md` | Entity renames, helper replacements, trigger restructuring, dashboard consumers, config-entry groups, config-entry blind spots, storage-mode dashboard references. |
| `device-control.md` | Entity ID vs device ID, service call `target`, Zigbee ZHA/Z2M button patterns, lights, climate, covers, media players, notifications, vacuums. |
| `template-guidelines.md` | When templates are appropriate, when to avoid them, defensive state access, availability, state_class, trigger-based templates, performance. |
| `dashboard-guide.md` | Dashboard structure, view types, sections, tile cards, actions, custom cards, HACS, visual iteration. |
| `dashboard-cards.md` | Card type lookup and card-specific documentation routing. |
| `yaml-only-integrations.md` | Managed YAML editing for integrations with no config flow and correct reload/restart expectations. |
| `domain-docs.md` | Official Home Assistant integration/domain documentation lookup. |

## Graph Edge Meanings

- `specializes_into`: narrower skills that provide operational detail for this skill.
- `generalizes_to`: broader skills that should be loaded first when the task is underspecified.
- `cross_references`: adjacent skills, upstream references, or docs that inform the work without being parent/child details.

## Routing Rules

1. If the user wants to connect MCPs, run the **MCP Setup Decision** elicitation below first, then use `ha-mcp-setup` (local) or the HTTP template (remote) per the result.
2. If the user wants to inspect or control exposed devices, use `ha-official-mcp-context`.
3. If the user wants to author configuration through live Home Assistant, use `ha-mcp-config-author` and classify tools with `ha-mcp-tool-policy`.
4. If the user wants to change a Home Assistant repo, use `ha-repo-refactor` before using live write tools.
5. If the user wants dashboards, route through the dashboard hub and use `ha-mcp-config-author` only when applying changes live.
6. If the user wants deployment, use deployer safety before any deploy tool.
7. If the operation deletes, removes, restarts, renames, touches registry metadata, exposes secrets, or edits `.storage`, route through review gates.

## MCP Setup Decision

Before connecting `ha-config-ha-mcp`, help the user pick a transport — don't guess. `ha-mcp` is one server with two modes: **local** (`uvx` stdio, default) or **remote** (HTTP server, usually the HA add-on). Elicit these first (Claude Code: `AskUserQuestion`; Codex: ask directly):

1. One machine/user, or several clients/people?
2. Agent on the same LAN as HA, or needs access from outside (cloud/web/mobile)?
3. Can the client run a local `uvx` command, or HTTP only?
4. Is `uv`/Python available on the agent host?
5. Need HA-host-side tools (the companion custom component's beta filesystem/YAML tools)?
6. Version: always-latest, or pinned/central?

Decide:

- **Local `uvx` stdio (default)** — one machine, same network as HA, client can run a stdio command, `uv` available. Vars `HOMEASSISTANT_URL` + `HOMEASSISTANT_TOKEN`. Route to `ha-mcp-setup`.
- **Remote HTTP / add-on** — if any apply: multiple clients/users, access from outside the LAN, HTTP-only client, no `uv` on the host, you need HA-host-side tools, or you want a pinned central version. Vars `HA_MCP_URL` + `HA_MCP_TOKEN`. No auto-setup script; copy the `home-assistant-config-http` template.

`HOMEASSISTANT_URL` is HA itself; `HA_MCP_URL` is the `ha-mcp` server (the add-on when ha-mcp runs inside HA). Full detail and the transport table: `plugins/ha-config-ha-mcp/docs/setup.md` (**Transport Modes**). The official server (`ha-official-mcp-context`) is a separate `/api/mcp` OAuth endpoint and runs alongside either mode.

## Safety

- Do not treat the graph as permission to use broader tools.
- Do not skip dependency scans for entity renames, helper deletes, dashboard rewrites, or registry operations.
- Do not mutate Home Assistant live config until the narrower skill's safety section is satisfied.
