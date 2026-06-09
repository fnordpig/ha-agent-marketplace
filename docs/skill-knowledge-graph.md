# Skill Knowledge Graph

This graph covers the total marketplace skill surface: local marketplace skills, the upstream `home-assistant-best-practices` skill, and the upstream reference files inside `plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/`.

The graph uses the same three edge families as the `swarm-orchestration` skill frontmatter:

- `specializes_into`: a broader hub points at narrower operational details.
- `generalizes_to`: a narrower detail points back to broader entry points.
- `cross_references`: adjacent skills, docs, or upstream references that ground the work without being a parent/detail relation.

The upstream submodule is not edited. Local skills carry `graph` frontmatter; upstream detail nodes are represented here and linked from local cross references.

## Total Hub Topology

```text
ha-marketplace-orientation
├── ha-mcp-setup
│   ├── ha-official-mcp-setup
│   ├── ha-official-mcp-context
│   │   └── upstream: device-control.md, domain-docs.md
│   ├── ha-mcp-config-author
│   └── ha-vibecode-deploy
├── ha-mcp-config-author
│   ├── ha-mcp-tool-policy
│   ├── ha-automation-author
│   │   └── upstream: automation-patterns.md, device-control.md, examples.yaml
│   ├── ha-helper-selection
│   │   └── upstream: helper-selection.md
│   ├── ha-template-safety
│   │   └── upstream: template-guidelines.md
│   ├── ha-entity-refactor
│   │   └── upstream: safe-refactoring.md
│   └── ha-change-review
├── ha-repo-refactor
│   ├── ha-dependency-graph
│   ├── ha-yaml-boundaries
│   │   └── upstream: yaml-only-integrations.md
│   ├── ha-entity-refactor
│   └── ha-review-checklist
├── ha-lovelace-yaml-dashboard
│   ├── ha-mobile-dashboard
│   ├── ha-wall-panel-dashboard
│   └── upstream: dashboard-guide.md, dashboard-cards.md, safe-refactoring.md
├── ha-vibecode-deploy
│   ├── ha-live-deploy-safety
│   ├── ha-backup-rollback
│   └── ha-change-review
└── ha-change-review
    ├── ha-review-checklist
    ├── ha-backup-rollback
    ├── ha-destructive-operation-review
    └── ha-security-review
```

## Upstream Detail Nodes

| Upstream node | Generalizes to | Specializes into | Cross references |
|---|---|---|---|
| `home-assistant-best-practices` | `ha-marketplace-orientation` | `automation-patterns.md`, `helper-selection.md`, `safe-refactoring.md`, `device-control.md`, `template-guidelines.md`, `dashboard-guide.md`, `dashboard-cards.md`, `yaml-only-integrations.md`, `domain-docs.md`, `examples.yaml` | All local authoring, dashboard, refactor, and review skills |
| `automation-patterns.md` | `home-assistant-best-practices`, `ha-automation-author`, `ha-mcp-config-author` | native conditions, trigger types, waits, modes, repeats, trigger IDs, disabling automations | `device-control.md`, `template-guidelines.md`, `safe-refactoring.md` |
| `helper-selection.md` | `home-assistant-best-practices`, `ha-helper-selection`, `ha-mcp-config-author` | numeric aggregation, rate/change, utility meters, state storage, counters/timers, schedules, groups | `template-guidelines.md`, `safe-refactoring.md`, `dashboard-guide.md` |
| `safe-refactoring.md` | `home-assistant-best-practices`, `ha-entity-refactor`, `ha-repo-refactor`, `ha-change-review` | entity renames, helper replacements, trigger restructuring, config-entry groups, config-entry data, storage dashboards | `dashboard-guide.md`, `yaml-only-integrations.md`, `ha-dependency-graph` |
| `device-control.md` | `home-assistant-best-practices`, `ha-automation-author`, `ha-official-mcp-context` | entity vs device IDs, service targets, ZHA/Z2M remotes, lights, climate, covers, media, notifications, vacuums | `automation-patterns.md`, `domain-docs.md` |
| `template-guidelines.md` | `home-assistant-best-practices`, `ha-template-safety` | appropriate template uses, native alternatives, template sensors, automation templates, error handling, performance | `helper-selection.md`, `automation-patterns.md` |
| `dashboard-guide.md` | `home-assistant-best-practices`, `ha-lovelace-yaml-dashboard` | structure, views, sections, cards, features, actions, custom cards, HACS, visual iteration | `dashboard-cards.md`, `safe-refactoring.md`, `ha-yaml-boundaries` |
| `dashboard-cards.md` | `home-assistant-best-practices`, `ha-lovelace-yaml-dashboard` | card-type lookup and card docs routing | `dashboard-guide.md`, `domain-docs.md` |
| `yaml-only-integrations.md` | `home-assistant-best-practices`, `ha-yaml-boundaries`, `ha-repo-refactor` | YAML-only integration types, reload vs restart expectations | `template-guidelines.md`, `ha-live-deploy-safety` |
| `domain-docs.md` | `home-assistant-best-practices` | official domain/integration docs lookup | `device-control.md`, `dashboard-cards.md` |
| `examples.yaml` | `home-assistant-best-practices` | compound examples | `automation-patterns.md`, `device-control.md`, `helper-selection.md` |

## Semantic Hubs

| Hub | Dense because | Novelty / obscurity / grounding |
|---|---|---|
| Device and service control | Crosses official MCP context, `ha_call_service`, stable `entity_id` targeting, ZHA/Z2M remotes, domain-specific service data. | `device_id` instability, ZHA `device_ieee`, Z2M exceptions, `color_temp_kelvin`, `vacuum.clean_area` all require upstream grounding. |
| Automation authoring | Connects native triggers/conditions, helper choices, templates, device control, modes, waits, and review. | Many wrong answers look plausible; upstream docs encode subtle HA version changes and behavioral differences. |
| Helper/modeling choice | Determines whether state belongs in helpers, template helpers, YAML, groups, schedules, timers, or dashboards. | High utility because it prevents unnecessary Jinja and makes dashboard/user control possible. |
| Safe refactoring | Connects repo scans, live MCP search, entity registry changes, dashboards, config-entry groups, and rollback. | Obscure and high-risk because HA registry renames do not update all consumers. |
| Dashboard design | Connects local dashboard skills, upstream card/view docs, storage/YAML boundaries, and visual iteration. | Dense because layout choices, card features, HACS, and storage-mode mutation are separate risk surfaces. |
| YAML boundary management | Connects repo-first work, UI-managed config, YAML-only integrations, reload/restart expectations, and deployment gates. | Grounding prevents agents from writing YAML for UI-configured integrations or editing `.storage`. |
| Review/deploy safety | Connects tool policy, backup/rollback, destructive operations, secrets, restart/reload, and Vibecode deploy. | Cross-cutting; every write path eventually routes here when risk increases. |
| MCP profile setup | Connects observer, builder, deployer, and full profiles to actual Codex and Claude Code config behavior. | Prevents placeholder MCP auto-starts and accidental high-privilege deployer enablement. |

## Local Skill To Upstream Grounding

| Local skill | Primary upstream grounding | Notes |
|---|---|---|
| `ha-automation-author` | `automation-patterns.md`, `device-control.md`, `examples.yaml` | Use before writing triggers/actions/modes. |
| `ha-helper-selection` | `helper-selection.md` | Use before choosing templates or new helpers. |
| `ha-template-safety` | `template-guidelines.md`, `helper-selection.md` | Use to justify templates only after native/helper alternatives. |
| `ha-entity-refactor` | `safe-refactoring.md` | Use before rename/delete/reference migration. |
| `ha-mcp-config-author` | `automation-patterns.md`, `helper-selection.md`, `safe-refactoring.md`, `dashboard-guide.md` | Live config authoring hub; classify tools first. |
| `ha-mcp-tool-policy` | `safe-refactoring.md` | Risk classification is a gate, not approval. |
| `ha-official-mcp-context` | `device-control.md`, `domain-docs.md` | Good for exposed context/control; not config authoring. |
| `ha-repo-refactor` | `safe-refactoring.md`, `yaml-only-integrations.md` | Repo work needs dependency scans and correct YAML boundaries. |
| `ha-yaml-boundaries` | `yaml-only-integrations.md`, `safe-refactoring.md` | Distinguish YAML-only config from UI/config-entry state. |
| `ha-dependency-graph` | `safe-refactoring.md` | Local scanner supports upstream consumer-search workflow. |
| `ha-lovelace-yaml-dashboard` | `dashboard-guide.md`, `dashboard-cards.md` | Use card/view docs for concrete dashboard structure. |
| `ha-mobile-dashboard` | `dashboard-guide.md`, `dashboard-cards.md` | Specializes dashboard ergonomics for phone workflows. |
| `ha-wall-panel-dashboard` | `dashboard-guide.md`, `dashboard-cards.md` | Specializes dashboard ergonomics for always-visible displays. |
| `ha-change-review` | `safe-refactoring.md`, `yaml-only-integrations.md` | Evidence gate across repo/live/deploy paths. |
| `ha-destructive-operation-review` | `safe-refactoring.md` | Required for delete/remove/registry/restart risk. |
| `ha-security-review` | `safe-refactoring.md`, `yaml-only-integrations.md` | Secrets and internal-state boundary review. |
| `ha-vibecode-deploy` | `safe-refactoring.md`, `yaml-only-integrations.md` | Deploy only after review, validation, backup, rollback. |
| `ha-live-deploy-safety` | `yaml-only-integrations.md`, `safe-refactoring.md` | Reload vs restart expectations matter here. |

## Use Pattern

1. Start with `ha-marketplace-orientation` when the task is broad or ambiguous.
2. Pick one semantic hub.
3. Load the local hub skill.
4. Read the upstream reference node that grounds the subtle part of the task.
5. Follow `specializes_into` for operational detail.
6. Follow `cross_references` only when the task touches an adjacent concern.
7. For risky writes, route through `ha-change-review` or a narrower review gate.
