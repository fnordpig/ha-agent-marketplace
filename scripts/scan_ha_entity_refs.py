#!/usr/bin/env python3
"""Scan files for likely Home Assistant entity IDs."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

EXTENSIONS = {".yaml", ".yml", ".json", ".md", ".jinja", ".j2"}
ENTITY_RE = re.compile(r"\b([a-z][a-z0-9_]*\.[a-z0-9_]+(?:_[a-z0-9]+)*)\b")
DOMAINS = {
    "automation", "binary_sensor", "button", "calendar", "camera", "climate",
    "cover", "device_tracker", "fan", "group", "humidifier", "input_boolean",
    "input_button", "input_datetime", "input_number", "input_select",
    "input_text", "light", "lock", "media_player", "number", "person",
    "remote", "scene", "script", "select", "sensor", "switch", "timer",
    "update", "vacuum", "weather", "zone",
}


def iter_files(root: Path):
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in EXTENSIONS:
            if any(part in {".git", "__pycache__"} for part in path.parts):
                continue
            yield path


def scan(root: Path):
    results = []
    for path in iter_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
        except OSError:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            stripped = line.strip()
            if stripped.startswith("service:") or stripped.startswith("- service:"):
                continue
            for match in ENTITY_RE.finditer(line):
                entity = match.group(1)
                domain = entity.split(".", 1)[0]
                if domain not in DOMAINS:
                    continue
                results.append({
                    "file": str(path.relative_to(root)),
                    "line": lineno,
                    "entity_id": entity,
                    "excerpt": line.strip()[:200],
                })
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if not root.exists():
        print(f"root does not exist: {root}", file=sys.stderr)
        return 2
    results = scan(root)
    if args.json:
        print(json.dumps(results, indent=2, sort_keys=True))
    else:
        by_entity = {}
        for item in results:
            by_entity.setdefault(item["entity_id"], []).append(item)
        if args.summary:
            print(f"Scanned {root}")
            print(f"Found {len(results)} references to {len(by_entity)} entities")
            for entity in sorted(by_entity):
                print(f"{entity}: {len(by_entity[entity])}")
        else:
            for item in results:
                print(f"{item['file']}:{item['line']}: {item['entity_id']} :: {item['excerpt']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
