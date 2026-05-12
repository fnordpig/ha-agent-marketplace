# Security Model

## Trust Boundaries

Read-only state can still expose household behavior. Treat entity names, areas, people, schedules, logs, and history as private.

Configuration authoring can break automations or expose devices. Prefer diff-only proposals until the user approves.

Repo editing is safer than live mutation but still requires validation before deployment.

Live deployment is high privilege. It requires backup confirmation, config validation, diff summary, deployment status, rollback path, and explicit approval.

## Sensitive Targets

- `.storage/`
- `secrets.yaml`
- `known_devices.yaml`
- UI-managed `automations.yaml`
- entity and device registries
- config entries
- HACS, add-ons, themes, and custom components
- restart, reboot, delete, remove, and `rm -rf` operations

## Rollback

Every deploy plan must describe the backup used, the validation result, the exact files changed, and the rollback command or UI path.

