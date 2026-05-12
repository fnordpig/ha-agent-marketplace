# ha-mcp Tool Policy

Use read tools freely for discovery, but remember they may reveal private household behavior.

Use write tools only after a diff-style summary. Broad write surfaces include automations, scripts, helpers, dashboards, registry metadata, files, YAML configuration, HACS, and add-ons.

Deletion, registry changes, file overwrite, file deletion, backup restore, restart, and reload operations require explicit approval and rollback notes.

Beta filesystem and YAML editing tools require upstream feature flags. Treat them as high risk.

