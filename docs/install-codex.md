# Install With Codex

After this repository is published:

```bash
npx codex-marketplace add fnordpig/ha-agent-marketplace --plugins --project
```

For one plugin:

```bash
npx codex-marketplace add fnordpig/ha-agent-marketplace/plugins/ha-foundation-skills --plugin --project
```

MCP-backed plugins include `.mcp.json` templates. Copy real URLs and tokens only into your local Codex config or environment, never into this repository.

## Upstream Home Assistant Skill Pack

This marketplace includes `homeassistant-ai/skills` as a Git submodule at `plugins/homeassistant-ai-skills`. Current Codex marketplace Git install code uses plain `git clone`, so initialize submodules after cloning this repository if you want the local upstream skill pack:

```bash
git submodule update --init --recursive
```

Codex accepts the upstream `.claude-plugin/plugin.json` manifest and loads the default `skills/` directory.
