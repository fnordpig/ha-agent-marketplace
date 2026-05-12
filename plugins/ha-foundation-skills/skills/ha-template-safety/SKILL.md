---
name: ha-template-safety
description: Review Home Assistant templates for maintainability and failure behavior.
---

# Home Assistant Template Safety

## Guidance

- Prefer native Home Assistant features before Jinja.
- Keep templates short, readable, and defensive about missing states.
- Use helpers or scripts when logic should be inspectable by users.

## Safety

- Do not introduce templates that hide destructive service calls or depend on undocumented entity names.

