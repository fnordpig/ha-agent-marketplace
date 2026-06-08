# ha-mcp Tool Policy

Use read tools freely for discovery, but remember they may reveal private household behavior.

Use write tools only after a diff-style summary. Broad write surfaces include automations, scripts, helpers, dashboards, registry metadata, files, YAML configuration, HACS, and add-ons.

Deletion, registry changes, file overwrite, file deletion, backup restore, restart, and reload operations require explicit approval and rollback notes.

Beta filesystem and YAML editing tools require upstream feature flags. Treat them as high risk.

Current `homeassistant-ai/ha-mcp` includes per-tool approval policy support and auto-backups for write/destructive calls. Treat those as an additional guard, not permission to skip marketplace review gates. For config subentries, use `ha_get_integration` to inspect metadata/schema, `ha_config_set_helper(helper_type="config_subentry", ...)` to create or update, and `ha_remove_helpers_integrations(helper_type="config_subentry", ...)` only after explicit approval.
