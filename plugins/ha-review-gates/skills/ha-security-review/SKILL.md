---
name: ha-security-review
description: Review Home Assistant agent changes for secrets and privilege boundaries.
---

# HA Security Review

## Checklist

- No real tokens, URLs, secrets, or personal entity names are committed.
- MCP tools match the requested privilege profile.
- Sensitive files are not edited casually.

## Safety

- Do not expose `secrets.yaml`, long-lived tokens, agent keys, or private URLs in logs or docs.

