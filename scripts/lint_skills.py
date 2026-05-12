#!/usr/bin/env python3
"""Lint bundled SKILL.md files using only stdlib."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WRITE_WORDS = {"deploy", "write", "refactor", "author", "delete", "review", "dashboard", "config"}


def parse_frontmatter(text: str):
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    data = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"')
    return data, text[end + 5:]


def main() -> int:
    errors = []
    warnings = []
    for path in sorted(ROOT.glob("plugins/*/skills/*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        rel = path.relative_to(ROOT)
        if not fm.get("name"):
            errors.append(f"{rel}: missing name")
        desc = fm.get("description", "")
        if not desc:
            errors.append(f"{rel}: missing description")
        if len(desc) > 140:
            warnings.append(f"{rel}: description is long")
        if len(text.split()) > 900:
            warnings.append(f"{rel}: skill is long")
        risk = any(word in (desc + " " + fm.get("name", "")).lower() for word in WRITE_WORDS)
        if risk and ("Safety" not in body and "Do not" not in body):
            errors.append(f"{rel}: write-capable workflow lacks Safety/Do not section")
        print(f"Checked {rel}")
    for warning in warnings:
        print(f"Warning: {warning}")
    if errors:
        print("Errors:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Skill lint passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

