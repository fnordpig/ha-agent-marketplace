#!/usr/bin/env python3
"""Inspect or create a conservative agent-managed HA config layout."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    config = root / "configuration.yaml"
    dirs = [root / "automations", root / "packages", root / "dashboards"]
    for directory in dirs:
        print(f"{directory.relative_to(root)}: {'exists' if directory.exists() else 'missing'}")
        if args.write and not directory.exists():
            directory.mkdir(parents=True)
    includes = [
        "automation: !include_dir_merge_list automations",
        "homeassistant:",
        "  packages: !include_dir_named packages",
        "lovelace:",
        "  dashboards: !include dashboards/dashboards.yaml",
    ]
    if not config.exists():
        print("configuration.yaml: missing")
        return 0
    text = config.read_text(encoding="utf-8")
    missing = [line for line in includes if line not in text]
    if not missing:
        print("configuration.yaml: includes look present")
        return 0
    print("Suggested include lines:")
    for line in missing:
        print(line)
    if args.write:
        backup = config.with_suffix(config.suffix + ".bak")
        shutil.copy2(config, backup)
        config.write_text(text.rstrip() + "\n\n# Agent-managed layout suggestions\n" + "\n".join(missing) + "\n", encoding="utf-8")
        print(f"wrote {config} after backup {backup}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

