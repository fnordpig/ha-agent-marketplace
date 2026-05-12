#!/usr/bin/env python3
"""Render a compact repository tree."""

from __future__ import annotations

from pathlib import Path

IGNORE = {".git", "__pycache__", ".pytest_cache", "reference"}


def walk(path: Path, prefix: str = ""):
    entries = sorted([p for p in path.iterdir() if p.name not in IGNORE and not p.name.endswith(".pyc")], key=lambda p: (p.is_file(), p.name))
    for index, entry in enumerate(entries):
        branch = "`-- " if index == len(entries) - 1 else "|-- "
        print(prefix + branch + entry.name)
        if entry.is_dir():
            walk(entry, prefix + ("    " if index == len(entries) - 1 else "|   "))


if __name__ == "__main__":
    print(Path.cwd().name)
    walk(Path.cwd())

