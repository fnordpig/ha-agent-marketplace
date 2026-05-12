---
name: ha-backup-rollback
description: Require backup and rollback coverage for Home Assistant changes.
---

# Home Assistant Backup And Rollback

## Guidance

- Identify the backup or git commit before change.
- Record validation output.
- Document how to roll back each changed file or live deployment.

## Safety

- Do not perform live deploys without backup confirmation, validation result, diff summary, and rollback path.

