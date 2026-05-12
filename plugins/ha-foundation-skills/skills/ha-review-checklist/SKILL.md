---
name: ha-review-checklist
description: Review Home Assistant configuration changes before approval or deployment.
---

# Home Assistant Review Checklist

## Checklist

- Does the change use native HA primitives before complex templates?
- Are new files agent-managed and clearly named?
- Were entity references scanned?
- Are backups, validation, and rollback notes present?

## Safety

- Do not approve destructive changes without explicit user approval.

