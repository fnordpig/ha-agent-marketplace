---
name: ha-live-deploy-safety
description: Enforce backup, validation, approval, and rollback for live HA deploys.
---

# HA Live Deploy Safety

## Required Before Deploy

- Human-readable deployment plan.
- Backup confirmation.
- Config validation result.
- Rollback path.
- Explicit approval.

## Safety

- Do not restart, reboot, remove, or delete without user confirmation and dependency scan.

