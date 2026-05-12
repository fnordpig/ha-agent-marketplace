#!/usr/bin/env python3
"""Validate plugin manifests."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {"name", "version", "description"}
WRITE_OK = {"ha-context-official", "ha-config-ha-mcp", "ha-repo-poweruser", "ha-deploy-vibecode", "ha-dashboard-designer", "ha-review-gates"}


def main() -> int:
    errors = []
    for path in sorted(ROOT.glob("plugins/*/.codex-plugin/plugin.json")):
        manifest = json.loads(path.read_text(encoding="utf-8"))
        name = manifest.get("name", path.parents[1].name)
        missing = REQUIRED - set(manifest)
        if missing:
            errors.append(f"{name}: missing {sorted(missing)}")
        for key in ("skills", "mcpServers", "hooks"):
            value = manifest.get(key)
            if value and not value.startswith("./"):
                errors.append(f"{name}: {key} should start with ./")
        caps = manifest.get("interface", {}).get("capabilities", [])
        if any(cap not in {"Read", "Write"} for cap in caps):
            errors.append(f"{name}: unsupported capability {caps}")
        if "Write" in caps and name not in WRITE_OK:
            errors.append(f"{name}: declares Write without policy justification")
        print(f"Checked {name}")
    if errors:
        print("Errors:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Manifest validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

