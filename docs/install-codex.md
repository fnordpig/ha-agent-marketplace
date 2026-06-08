# Install With Codex

After this repository is published:

```bash
codex plugin marketplace add fnordpig/ha-agent-marketplace --ref main
codex plugin list --marketplace ha-agent-marketplace
```

Install the plugins you want from the configured marketplace:

```bash
codex plugin add ha-foundation-skills@ha-agent-marketplace
codex plugin add ha-context-official@ha-agent-marketplace
```

For local development, add the working tree directly:

```bash
codex plugin marketplace add .
```

MCP-backed plugins include templates under `docs/templates/mcp.json`. They are not named `.mcp.json` at plugin root because Codex auto-discovers and starts root `.mcp.json` files immediately, and placeholder URLs such as `${HOMEASSISTANT_URL}/api/mcp` will fail startup. Copy real URLs and tokens only into your local Codex config or environment, never into this repository.

For Home Assistant MCP setup, stay inside Codex and ask:

```text
Set up Home Assistant MCPs for http://homeassistant:8123 with the builder profile.
```

The setup skill runs the shared plugin script with `uv run python`. It may write the non-secret Home Assistant URL, but it writes only token environment variable references, never token values.

## Upstream Home Assistant Skill Pack

This marketplace exposes `homeassistant-ai/skills` as a direct Git plugin source so Codex can fetch it independently. It also includes the same upstream repo as a maintainer submodule at `plugins/homeassistant-ai-skills`.

Current Codex marketplace Git install code uses plain `git clone`, so initialize submodules after cloning this repository only if you want the local maintainer copy:

```bash
git submodule update --init --recursive
```

Codex accepts the upstream `.claude-plugin/plugin.json` manifest and loads the default `skills/` directory.
