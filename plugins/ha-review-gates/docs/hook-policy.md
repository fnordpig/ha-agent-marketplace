# Hook Policy

These hooks are optional templates, not marketplace-installed defaults. They ship
at `hooks/templates/hooks.json` (not `hooks/hooks.json`) so that Claude Code does
not auto-discover and register them on install; Codex does not auto-register them
either, since the plugin manifest does not declare a hooks path.

Use them only when you want an additional local warning layer around sensitive
Home Assistant work. The main safety model is the review-gates skills plus
preview/diff/validation discipline in the MCP tools.

The pre-tool hook warns on commands and tool payloads containing sensitive terms:

- delete
- remove
- `rm -rf`
- restart
- reboot
- hassio
- `ha core restart`
- `docker compose down`
- `.storage`
- `secrets.yaml`
- `known_devices.yaml`
- direct writes to `automations.yaml`

The post-turn hook emits a short reporting reminder.

Both hook commands are intentionally fail-open. If the hook script is missing
from a local cache, the command exits successfully instead of blocking all
agent tool calls (in Codex or Claude Code). The hook warning is an aid, not an
enforcement boundary.
