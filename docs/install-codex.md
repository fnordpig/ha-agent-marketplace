# Install With Codex

After this repository is published:

```bash
npx codex-marketplace add fnordpig/ha-agent-marketplace --plugins --project
```

For one plugin:

```bash
npx codex-marketplace add fnordpig/ha-agent-marketplace/plugins/ha-foundation-skills --plugin --project
```

MCP-backed plugins include templates under `docs/templates/mcp.json`. They are not named `.mcp.json` at plugin root because Codex auto-discovers and starts root `.mcp.json` files immediately, and placeholder URLs such as `${HOMEASSISTANT_URL}/api/mcp` will fail startup. Copy real URLs and tokens only into your local Codex config or environment, never into this repository.

## Upstream Home Assistant Skill Pack

This marketplace exposes `homeassistant-ai/skills` as a direct Git plugin source so Codex can fetch it independently. It also includes the same upstream repo as a maintainer submodule at `plugins/homeassistant-ai-skills`.

Current Codex marketplace Git install code uses plain `git clone`, so initialize submodules after cloning this repository only if you want the local maintainer copy:

```bash
git submodule update --init --recursive
```

Codex accepts the upstream `.claude-plugin/plugin.json` manifest and loads the default `skills/` directory.
