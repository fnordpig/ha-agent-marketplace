# Home Assistant Agent Marketplace Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and publish a stdlib-only Codex-first, Claude Code-compatible Home Assistant agent marketplace scaffold.

**Architecture:** Create a layered marketplace: shared Home Assistant skills, official context MCP profile, broad configuration MCP profile, repo-first power-user tools, dashboard skills, Vibecode deployer profile, and review gates. Keep upstream projects as inspected references only; commit docs, templates, manifests, scripts, and examples.

**Tech Stack:** Markdown, JSON, TOML text templates, YAML examples, Python 3 stdlib, Git/GitHub CLI.

---

## File Map

- `AGENTS.md`: repository operating rules for agents.
- `README.md`, `LICENSE`, `.gitignore`: public project shell.
- `.agents/plugins/marketplace.json`: primary Codex marketplace catalog.
- `.claude-plugin/marketplace.json`: Claude Code compatibility catalog.
- `docs/*.md`: architecture, security, installs, profiles, HA boundaries, upstream inventory, implementation notes.
- `docs/examples/*.md`: example user sessions.
- `scripts/*.py`: root validation, tree rendering, and entity reference scanning.
- `plugins/*/.codex-plugin/plugin.json`: plugin manifests.
- `plugins/*/skills/*/SKILL.md`: skill content.
- `plugins/*/.mcp.json`: MCP templates where applicable.
- `plugins/*/docs/*.md`: plugin-local setup and policy docs.
- `plugins/ha-repo-poweruser/scripts/*.py`: plugin-local repo workflow helpers.
- `plugins/ha-review-gates/hooks/*`: conservative hook templates.
- `examples/codex-config/*.config.toml`: profile config examples.
- `examples/ha-config-repo/*`: non-live Home Assistant config sample.

## Task 1: Upstream And Codex Research

**Files:**
- Create during research only: `reference/`
- Create: `docs/upstream-inventory.md`
- Create: `docs/implementation-notes.md`

- [ ] **Step 1: Create ignored research workspace**

Run: `mkdir -p reference`

Expected: local `reference/` directory exists and remains untracked after `.gitignore` is added.

- [ ] **Step 2: Inspect current upstream docs and repos**

Use web and local `reference/` clones as needed for:

```text
https://www.home-assistant.io/integrations/mcp_server/
https://www.home-assistant.io/integrations/mcp/
https://github.com/homeassistant-ai/ha-mcp
https://homeassistant-ai.github.io/ha-mcp/
https://github.com/homeassistant-ai/skills
https://github.com/Coolver/home-assistant-vibecode-agent
https://coolver.github.io/home-assistant-vibecode-agent/
https://github.com/Coolver/mcp-home-assistant
https://github.com/mickek/ha-pilot
https://community.home-assistant.io/t/claude-code-plugin-for-home-assistant-ai-assisted-automation-management/977939
https://github.com/achetronic/hass-mcp
https://github.com/tevonsb/homeassistant-mcp
https://github.com/mtebusi/HA_MCP
```

Expected: enough information to populate URL, purpose, install model, MCP transport, capabilities, config-writing capability, deployment capability, safety model, license, and marketplace role.

- [ ] **Step 3: Inspect current Codex plugin documentation**

Check current Codex documentation or local examples for:

```text
.codex-plugin/plugin.json
.agents/plugins/marketplace.json
.mcp.json
skills/SKILL.md
hooks/hooks.json
AGENTS.md behavior
```

Expected: manifest/catalog fields are based on current docs or local observed examples, not stale assumptions.

- [ ] **Step 4: Write upstream inventory**

Create `docs/upstream-inventory.md` with a concise table:

```markdown
# Upstream Inventory

| Name | URL | Purpose | Install model | MCP transport | Configuration capability | Deployment capability | Safety model | License | Marketplace role |
|---|---|---|---|---|---|---|---|---|---|
```

Expected: one row per upstream named in the spec.

- [ ] **Step 5: Write implementation notes**

Create `docs/implementation-notes.md` with sections:

```markdown
# Implementation Notes

## Codex Schema Notes

## Claude Code Compatibility Notes

## Upstream Conflicts Or Limits

## Conservative Choices
```

Expected: records any schema mismatch, unsupported field, abandoned/narrow/control-oriented upstream, or conservative choice.

## Task 2: Repository Shell And Catalogs

**Files:**
- Create: `AGENTS.md`
- Create: `README.md`
- Create: `LICENSE`
- Create: `.gitignore`
- Create: `.agents/plugins/marketplace.json`
- Create: `.claude-plugin/marketplace.json`

- [ ] **Step 1: Add repository shell files**

Create `.gitignore` containing at least:

```gitignore
.DS_Store
__pycache__/
*.pyc
.pytest_cache/
reference/
*.bak
```

Create `LICENSE` with MIT license text and copyright holder `fnordpig`.

Expected: public project metadata exists and `reference/` is ignored.

- [ ] **Step 2: Add top-level agent guidance**

Create `AGENTS.md` with rules from the spec: stdlib-only scripts, no real tokens/secrets/personal entities, docs/templates over live mutation, update security docs for high-privilege changes, validate before final response, no vendoring upstreams, document ambiguous schemas.

Expected: future agents have clear repo-local boundaries.

- [ ] **Step 3: Add marketplace catalogs**

Create Codex catalog with one entry per plugin using local source paths:

```json
{
  "version": 1,
  "plugins": [
    {"name": "ha-foundation-skills", "source": "./plugins/ha-foundation-skills"},
    {"name": "ha-context-official", "source": "./plugins/ha-context-official"},
    {"name": "ha-config-ha-mcp", "source": "./plugins/ha-config-ha-mcp"},
    {"name": "ha-repo-poweruser", "source": "./plugins/ha-repo-poweruser"},
    {"name": "ha-deploy-vibecode", "source": "./plugins/ha-deploy-vibecode"},
    {"name": "ha-dashboard-designer", "source": "./plugins/ha-dashboard-designer"},
    {"name": "ha-review-gates", "source": "./plugins/ha-review-gates"}
  ]
}
```

Create a Claude compatibility catalog with the same plugin list and a note that Codex is primary.

Expected: validation can locate every plugin by source path.

## Task 3: Plugin Manifests And MCP Templates

**Files:**
- Create: `plugins/*/.codex-plugin/plugin.json`
- Create: `plugins/ha-context-official/.mcp.json`
- Create: `plugins/ha-config-ha-mcp/.mcp.json`
- Create: `plugins/ha-deploy-vibecode/.mcp.json`

- [ ] **Step 1: Create plugin manifests**

For each plugin, create a manifest with current supported fields. Use this minimum shape if docs do not require a different schema:

```json
{
  "name": "ha-foundation-skills",
  "version": "0.1.0",
  "description": "Instruction-only Home Assistant best-practice skills.",
  "author": "fnordpig",
  "license": "MIT",
  "keywords": ["home-assistant", "codex", "agents"],
  "skills": "./skills",
  "interface": {
    "displayName": "Home Assistant Foundation Skills",
    "shortDescription": "Best-practice guidance for Home Assistant configuration work.",
    "category": "Developer Tools",
    "capabilities": ["Read"]
  }
}
```

Expected: all seven plugins have manifests, with `Write` capability only where justified by MCP/hook/deploy/repo behavior.

- [ ] **Step 2: Create MCP templates**

Create conservative `.mcp.json` templates for the three MCP-backed plugins. Use placeholder environment variable names only, and document any config fields that require copying into user-level Codex config.

Expected: no real URL or token appears in committed files.

## Task 4: Skills And Plugin Docs

**Files:**
- Create all `plugins/*/skills/*/SKILL.md`
- Create plugin-local `docs/*.md`

- [ ] **Step 1: Add foundation skills**

Create six `SKILL.md` files with YAML frontmatter containing `name` and concise `description`, plus sections for workflow and safety:

```markdown
---
name: ha-automation-author
description: Author maintainable Home Assistant automations using native primitives first.
---

# Home Assistant Automation Author

## Use When

Use this when creating or reviewing Home Assistant automations.

## Guidance

- Prefer native triggers, conditions, helpers, scripts, scenes, and blueprints before complex Jinja.
- Prefer agent-managed files such as `automations/agent_*.yaml` over direct edits to UI-managed `automations.yaml`.

## Safety

- Do not deploy live changes without backup, validation, diff summary, and rollback notes.
- Destructive changes require explicit human approval.
```

Expected: all foundation skill categories from the spec are covered.

- [ ] **Step 2: Add MCP, repo, deploy, dashboard, and review skills**

Create skill files named in the prompt under each plugin. Each write-capable workflow must include a `Safety` or `Do not` section.

Expected: `scripts/lint_skills.py` passes without errors.

- [ ] **Step 3: Add plugin-local docs**

Create setup and policy docs named in the prompt. Include upstream links, install model, transport model, limitations, and conservative setup guidance.

Expected: each MCP-backed plugin explains how to configure the upstream without embedding secrets.

## Task 5: Stdlib Scripts

**Files:**
- Create: `scripts/validate_marketplace.py`
- Create: `scripts/validate_plugin_manifests.py`
- Create: `scripts/lint_skills.py`
- Create: `scripts/scan_ha_entity_refs.py`
- Create: `scripts/render_tree.py`
- Create: `plugins/ha-repo-poweruser/scripts/scan_ha_entity_refs.py`
- Create: `plugins/ha-repo-poweruser/scripts/propose_agent_managed_layout.py`
- Create: `plugins/ha-review-gates/hooks/pre_tool_use_policy.py`
- Create: `plugins/ha-review-gates/hooks/post_turn_summary.py`
- Create: `plugins/ha-review-gates/hooks/hooks.json`

- [ ] **Step 1: Implement marketplace validation**

Implement JSON loading, path existence checks, plugin manifest checks, referenced `skills`, `mcpServers`/MCP, and `hooks` paths.

Expected command: `python3 scripts/validate_marketplace.py`

Expected result: readable report and exit 0 after scaffold is complete.

- [ ] **Step 2: Implement manifest validation**

Validate required fields, relative paths, sensible capabilities, and write capability justification.

Expected command: `python3 scripts/validate_plugin_manifests.py`

Expected result: readable report and exit 0 after manifests are aligned.

- [ ] **Step 3: Implement skill linting**

Parse simple YAML frontmatter without third-party dependencies. Check `name`, `description`, length, and safety language for write-capable skills.

Expected command: `python3 scripts/lint_skills.py`

Expected result: readable report and exit 0.

- [ ] **Step 4: Implement entity reference scanner**

Implement recursive scanning for `.yaml`, `.yml`, `.json`, `.md`, `.jinja`, and `.j2`. Detect likely entity IDs with a regex shaped like `domain.object_name`, avoid common false positives, support `--root`, `--json`, and `--summary`.

Expected command: `python3 scripts/scan_ha_entity_refs.py --root examples/ha-config-repo --summary`

Expected result: summary includes generic sample entities and exits 0.

- [ ] **Step 5: Implement repo layout helper and hooks**

Implement `propose_agent_managed_layout.py` so it reports missing agent-managed directories/includes, only writes with `--write`, and creates `.bak` backups before edits. Implement hook scripts as conservative warning emitters that read optional JSON stdin.

Expected: no script requires third-party packages or a live Home Assistant instance.

## Task 6: General Docs And Examples

**Files:**
- Create: `docs/architecture.md`
- Create: `docs/security-model.md`
- Create: `docs/install-codex.md`
- Create: `docs/install-claude-code.md`
- Create: `docs/home-assistant-boundaries.md`
- Create: `docs/profiles.md`
- Create: `docs/examples/safe-observer-session.md`
- Create: `docs/examples/builder-session.md`
- Create: `docs/examples/power-user-repo-session.md`
- Create: `docs/examples/deployer-session.md`
- Create: `examples/codex-config/observer.config.toml`
- Create: `examples/codex-config/builder.config.toml`
- Create: `examples/codex-config/power.config.toml`

- [ ] **Step 1: Write architecture and profile docs**

Describe the seven-layer architecture and Safe Observer, Builder, Power User, Live Deployer, and Full Power profiles.

Expected: users can choose a plugin set without reading every plugin file.

- [ ] **Step 2: Write security and HA boundary docs**

Cover read-only state, configuration authoring, repo editing, live deployment, destructive operations, secrets, `.storage`, backups, rollback, UI-managed automations, YAML dashboards, storage-mode dashboards, config entries, entity registry, and device registry.

Expected: sensitive areas are explicit and conservative.

- [ ] **Step 3: Write install docs and example sessions**

Provide Codex quick start, Claude Code compatibility notes, environment variable placeholders, and example prompts for stale entity scanning, diff-only package authoring, YAML wall dashboard creation, and approved deployment.

Expected: docs are useful before any live integration is configured.

## Task 7: Example Home Assistant Config Repo

**Files:**
- Create: `examples/ha-config-repo/AGENTS.md`
- Create: `examples/ha-config-repo/configuration.yaml`
- Create: `examples/ha-config-repo/automations.yaml`
- Create: `examples/ha-config-repo/automations/agent_lighting.yaml`
- Create: `examples/ha-config-repo/packages/presence.yaml`
- Create: `examples/ha-config-repo/dashboards/wall-panel.yaml`
- Create: `examples/ha-config-repo/docs/entity-map.md`
- Create: `examples/ha-config-repo/docs/rollback.md`

- [ ] **Step 1: Create generic sample configuration**

Use only generic entities:

```text
binary_sensor.hallway_motion
light.hallway
input_boolean.guest_mode
input_select.house_mode
person.example_resident
```

Expected: scanner finds these references and no personal names or secrets exist.

- [ ] **Step 2: Document local boundaries**

In the example repo `AGENTS.md`, explain UI-managed `automations.yaml`, agent-managed `automations/`, packages, dashboards, secrets avoidance, and rollback docs.

Expected: example repo is safe to inspect and edit.

## Task 8: Validate, Commit, Publish

**Files:**
- Modify if needed: any file failing validation.

- [ ] **Step 1: Run validation**

Run:

```bash
python3 scripts/validate_marketplace.py
python3 scripts/validate_plugin_manifests.py
python3 scripts/lint_skills.py
python3 scripts/scan_ha_entity_refs.py --root examples/ha-config-repo --summary
```

Expected: all commands exit 0.

- [ ] **Step 2: Inspect git status and commit**

Run:

```bash
git status --short
git add .
git commit -m "Create Home Assistant agent marketplace scaffold"
```

Expected: scaffold commit exists after the already committed design spec.

- [ ] **Step 3: Create GitHub repository and push**

Run authenticated GitHub tooling to create `fnordpig/ha-agent-marketplace`, set `origin`, and push `main`.

Expected: remote repository exists and contains the scaffold. If auth/profile selection blocks this, stop with the local commit and report the exact blocker.

## Self-Review

- Spec coverage: research, manifests, skills, MCP templates, hooks, docs, scripts, example repo, validation, commit, and GitHub publishing are covered.
- Placeholder scan: no `TBD`, `TODO`, or deferred implementation language is used.
- Scope: one scaffold project with staged tasks; no live HA connection or third-party install is included.
- Consistency: script names, plugin names, and validation commands match the approved design spec.

