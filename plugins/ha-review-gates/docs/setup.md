# Review Gates Setup

This plugin bundles review skills and conservative hook templates.

The review skills are installed normally with the plugin. The hook scripts are
opt-in templates only; the plugin manifest does not auto-register them.

Why: hooks run outside the normal MCP/tool path and can block every tool call if
the plugin cache is incomplete or the hook runtime changes. Home Assistant
safety should degrade to skill-based review guidance, not brick the agent.

To enable the hooks manually, copy or reference `hooks/hooks.json` from a local
Codex/Claude hook configuration after confirming that both scripts exist in the
same plugin root:

- `hooks/pre_tool_use_policy.py`
- `hooks/post_turn_summary.py`

The hook commands are fail-open and warning-oriented. They do not assume a
fail-closed API unless the host client clearly supports it.
