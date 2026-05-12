# Home Assistant Agent Marketplace Design

Date: 2026-05-11
Repository: ha-agent-marketplace
Primary target: Codex plugin marketplace
Secondary target: Claude Code compatibility
License: MIT

## Goal

Create a clean, reviewable scaffold for a Home Assistant agent marketplace focused on programmatic Home Assistant configuration. The marketplace supports automations, helpers, scripts, dashboards, entity and device registry maintenance, repo refactoring, deployment review gates, and safe live deployment workflows.

The scaffold must be useful before it is connected to a live Home Assistant instance. It will include plugin manifests, skill content, MCP configuration templates, hook templates, setup documentation, safety policy, validation scripts, and a non-live example Home Assistant config repo.

## Non-Goals

The repository will not connect to a live Home Assistant instance during scaffolding.

The repository will not install third-party packages, require third-party Python dependencies, fetch runtime dependencies, or vendor upstream projects.

The marketplace is not primarily for casual device control. Official context/control integrations are documented as a low-risk observation and explicitly exposed entity-control profile, not as a full configuration-authoring layer.

The repository will not include real Home Assistant tokens, URLs, secrets, or personal entity names.

## Research Model

Before implementation, inspect the upstream projects and current Codex documentation listed in the prompt. The implementation may create a `.gitignore`d `reference/` directory and clone upstream repositories there for local inspection only. Files in `reference/` are research inputs, not vendored source, and must not be committed.

The scaffold must directly reference the MCPs and related projects affiliated with the marketplace:

- Official Home Assistant MCP Server integration for the `ha-context-official` profile.
- Official Home Assistant MCP Client integration for Home Assistant-as-client boundary documentation.
- `homeassistant-ai/ha-mcp` for the broad configuration MCP profile.
- `homeassistant-ai/skills` for optional upstream skill-pack comparison and attribution.
- Coolver Home Assistant Vibecode Agent and `Coolver/mcp-home-assistant` for the deployer profile.
- `mickek/ha-pilot` for repo-first power-user workflow ideas.
- `achetronic/hass-mcp`, `tevonsb/homeassistant-mcp`, and `mtebusi/HA_MCP` as comparative MCP architecture references.

The research output will be committed as `docs/upstream-inventory.md`. It will record each upstream's URL, purpose, install model, MCP transport, relevant capabilities, configuration-writing surface, deployment surface, safety model, license when available, and marketplace role.

If current Codex documentation differs from prompt assumptions, implementation will follow current docs and record the difference in `docs/implementation-notes.md`.

## Architecture

The repository is organized as a layered marketplace:

1. Instruction layer: Home Assistant best-practice skills for automation authoring, helper selection, template safety, entity refactors, backup/rollback thinking, and review checklists.
2. Official context layer: a low-risk official Home Assistant MCP profile for exposed state/context and Assist-oriented tools.
3. Broad configuration layer: templates and policy for a configuration-capable Home Assistant MCP server such as `homeassistant-ai/ha-mcp`.
4. Repo power-user layer: Git/YAML/repo-first workflows and stdlib scanners for serious Home Assistant configuration refactoring.
5. Dashboard layer: Lovelace/YAML dashboard skills for wall-panel and mobile layouts.
6. Deployer layer: high-privilege Vibecode-style deploy workflows with strict approval, validation, backup, and rollback requirements.
7. Review-gate layer: skills and hook templates that warn on destructive or sensitive operations.

Marketplace core metadata stays separate from upstream-specific setup. Upstream-specific examples belong in plugin-local docs, `.mcp.json` templates, and documentation snippets.

## Repository Shape

The implementation will create:

- Top-level `AGENTS.md`, `README.md`, `LICENSE`, `.gitignore`.
- Codex marketplace catalog at `.agents/plugins/marketplace.json`.
- Claude compatibility catalog at `.claude-plugin/marketplace.json`.
- Documentation under `docs/`, including architecture, security model, install guides, Home Assistant boundaries, profiles, upstream inventory, implementation notes, and example sessions.
- Validation and utility scripts under `scripts/`, using Python stdlib only.
- Seven plugin directories under `plugins/`.
- A non-live sample Home Assistant config repo under `examples/ha-config-repo`.
- Example Codex config templates under `examples/codex-config`.

## Plugins

`ha-foundation-skills` is instruction-only. It contains Home Assistant best-practice skills covering automation authoring, helper selection, template safety, entity refactors, backup/rollback, and review checklists.

`ha-context-official` documents and templates the official Home Assistant MCP Server integration. It is good for reading exposed state/context and low-risk interaction with explicitly exposed entities. It is not positioned as a full configuration authoring or repo refactoring solution.

`ha-config-ha-mcp` documents and templates a broad configuration MCP server such as `homeassistant-ai/ha-mcp`. Its skills treat broad write tools as high-risk and require diff summaries, dependency scans for destructive changes, and explicit approval before mutation.

`ha-repo-poweruser` supports Git/YAML/repo-first Home Assistant workflows. It includes stdlib scripts for entity reference scanning and proposing an agent-managed layout. It does not copy implementation from upstream projects.

`ha-deploy-vibecode` documents and templates a high-privilege deployer profile for Coolver Vibecode Agent or similar onboard deploy agents. Deploys require a human-readable plan, backup confirmation, validation result, rollback path, and explicit approval.

`ha-dashboard-designer` contains Lovelace/YAML dashboard-specific skills. It favors agent-managed YAML dashboards, mobile and wall-panel patterns, and maintainable card choices.

`ha-review-gates` contains validation/review skills and conservative hook templates. Hooks warn on sensitive operations such as direct writes to `.storage`, `secrets.yaml`, UI-managed `automations.yaml`, registry-like files, restart commands, destructive shell commands, and deploy/reboot commands.

## Codex And Claude Compatibility

Codex is the primary target. Each plugin will have `.codex-plugin/plugin.json` using fields supported by current Codex docs. If interface metadata, skills paths, MCP paths, hooks paths, capability declarations, installation policies, or authentication policies differ from prompt assumptions, implementation will use documented current values and record the difference.

Claude Code compatibility is a secondary but real target. The scaffold will include `.claude-plugin/marketplace.json`, shared `SKILL.md` content where reasonable, and Claude Code install guidance. It will not invent unsupported Claude Code behavior. Where compatibility is uncertain, docs will say so directly.

## Safety Model

The scaffold encodes these boundaries:

- Read-only state/context is lower risk but still may reveal private household information.
- Configuration authoring is write-capable and requires previews, diff summaries, and clear ownership boundaries.
- Repo editing is safer than live mutation but still requires dependency scanning and validation before deployment.
- Live deployment is high privilege and requires backup, validation, approval, deploy status, and rollback notes.
- Destructive operations require explicit user request and confirmation after dependency scanning.
- `.storage`, `secrets.yaml`, registries, config entries, UI-managed automations, dashboards in storage mode, add-ons, HACS, restart/reboot, and delete/remove operations are sensitive.

Top-level guidance will require updating security docs whenever high-privilege plugins change.

## Scripts And Validation

All scripts will use Python stdlib only.

`scripts/validate_marketplace.py` loads the Codex marketplace, checks plugin source paths, checks each plugin manifest exists, and verifies referenced skills, MCP, and hook paths.

`scripts/validate_plugin_manifests.py` checks required manifest fields, relative path conventions where documented, sensible capabilities, and write-capability justification.

`scripts/lint_skills.py` finds `SKILL.md` files, checks frontmatter includes `name` and `description`, warns on long or vague descriptions, warns on excessive length, and expects a "Do not" or "Safety" section for write-capable workflows.

`scripts/scan_ha_entity_refs.py` recursively scans YAML, JSON, Markdown, and Jinja-like files for likely Home Assistant entity IDs. It supports `--root`, `--json`, and `--summary`, avoids binary/encoding crashes, and exits nonzero only on actual script failure.

`scripts/render_tree.py` prints a useful repository tree while ignoring `.git`, `__pycache__`, `reference/`, and common temporary files.

Implementation validation must run:

```bash
uv run python scripts/validate_marketplace.py
uv run python scripts/validate_plugin_manifests.py
uv run python scripts/lint_skills.py
uv run python scripts/scan_ha_entity_refs.py --root examples/ha-config-repo --summary
```

Any failures found by these commands must be fixed before the scaffold is reported complete.

## GitHub Publishing

After implementation validates, initialize git if needed, commit the scaffold, create `fnordpig/ha-agent-marketplace` using authenticated GitHub tooling, configure the remote, and push. The process must not embed credentials, tokens, Home Assistant URLs, or SSH details in repository files.

If GitHub creation or push encounters an auth/profile ambiguity, stop with a local committed repository and report the exact blocker.

## Acceptance Criteria

The implementation is complete when:

- The requested repository tree exists.
- All seven plugins have manifests and expected content.
- Codex and Claude compatibility marketplace files exist.
- Docs describe architecture, security, install paths, profiles, Home Assistant boundaries, upstream inventory, implementation notes, and example sessions.
- Scripts are stdlib-only and executable with `uv run python`.
- The example Home Assistant config repo uses generic sample entities only.
- Validation commands pass.
- The scaffold is committed.
- The GitHub repository under `fnordpig` is created and pushed, unless blocked by an external auth/profile issue that is reported clearly.

