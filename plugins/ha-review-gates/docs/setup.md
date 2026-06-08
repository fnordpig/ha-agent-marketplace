# Review Gates Setup

This plugin bundles review skills and conservative hook templates.

The review skills are installed normally with the plugin. The hook scripts are
opt-in templates only; the plugin manifest does not auto-register them.

Why: hooks run outside the normal MCP/tool path and can block every tool call if
the plugin cache is incomplete or the hook runtime changes. Home Assistant
safety should degrade to skill-based review guidance, not brick the agent.

The template lives at `hooks/templates/hooks.json` rather than `hooks/hooks.json`
on purpose: Claude Code auto-loads any `hooks/hooks.json` at a plugin root on
install, which would defeat the opt-in design. Keeping it one level deeper means
neither Codex nor Claude Code registers it automatically.

To enable the hooks manually, copy or reference `hooks/templates/hooks.json` from
a local Codex/Claude hook configuration after confirming that both scripts exist
in the plugin root:

- `hooks/pre_tool_use_policy.py`
- `hooks/post_turn_summary.py`

The hook commands are fail-open and warning-oriented. They do not assume a
fail-closed API unless the host client clearly supports it.
