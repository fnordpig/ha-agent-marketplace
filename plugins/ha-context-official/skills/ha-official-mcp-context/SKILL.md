---
name: ha-official-mcp-context
description: Use the official Home Assistant MCP Server for exposed context and Assist tools.
---

# Official Home Assistant MCP Context

## Good For

- Reading exposed state and context.
- Assist-oriented tools and low-risk control of explicitly exposed entities.

## Not Ideal For

- Full configuration authoring.
- Repo refactoring.
- Arbitrary YAML or dashboard mutation.

## Safety

- Do not assume hidden entities are available.
- Do not use this profile as proof that configuration files are safe to edit.

