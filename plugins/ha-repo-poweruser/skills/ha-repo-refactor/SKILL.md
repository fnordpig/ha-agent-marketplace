---
name: ha-repo-refactor
description: Refactor Home Assistant YAML repos with git-first reviewable changes.
---

# HA Repo Refactor

## Guidance

- Work in agent-managed files where possible.
- Keep YAML includes obvious and documented.
- Run entity reference scans before moving or renaming entities.

## Safety

- Do not edit secrets or `.storage`.
- Do not reload or deploy from repo work without validation and approval.

