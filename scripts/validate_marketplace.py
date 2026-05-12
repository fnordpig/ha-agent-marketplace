#!/usr/bin/env python3
"""Validate the Codex marketplace catalog and plugin paths."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def rel_exists(base: Path, rel: str) -> bool:
    return (base / rel).resolve().exists()


def main() -> int:
    errors = []
    market = ROOT / ".agents" / "plugins" / "marketplace.json"
    data = load_json(market)
    print(f"Marketplace: {market.relative_to(ROOT)}")
    for entry in data.get("plugins", []):
        name = entry.get("name", "<missing>")
        source = entry.get("source", {})
        path = source.get("path") if isinstance(source, dict) else None
        if not path:
            errors.append(f"{name}: missing source.path")
            continue
        plugin_dir = (ROOT / path).resolve()
        print(f"- {name}: {plugin_dir.relative_to(ROOT)}")
        if not plugin_dir.exists():
            errors.append(f"{name}: source path missing: {path}")
            continue
        manifest_path = plugin_dir / ".codex-plugin" / "plugin.json"
        if not manifest_path.exists():
            errors.append(f"{name}: missing .codex-plugin/plugin.json")
            continue
        manifest = load_json(manifest_path)
        for field in ("skills", "mcpServers", "hooks"):
            rel = manifest.get(field)
            if rel and not rel_exists(plugin_dir, rel):
                errors.append(f"{name}: {field} path missing: {rel}")
    if errors:
        print("Errors:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Marketplace validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

