#!/usr/bin/env python3
"""Lint bundled SKILL.md files using only stdlib."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WRITE_WORDS = {"deploy", "write", "refactor", "author", "delete", "review", "dashboard", "config"}
GRAPH_KEYS = {"generalizes_to", "specializes_into", "cross_references"}


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


def parse_graph(text: str) -> dict[str, list[str]]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    graph: dict[str, list[str]] = {}
    current: str | None = None
    in_graph = False
    for line in text[4:end].splitlines():
        if line == "graph:":
            in_graph = True
            current = None
            continue
        if in_graph and line and not line.startswith(" "):
            in_graph = False
            current = None
        if not in_graph:
            continue
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.endswith(":") and stripped[:-1] in GRAPH_KEYS:
            current = stripped[:-1]
            graph.setdefault(current, [])
            continue
        if ": []" in stripped:
            key = stripped.split(":", 1)[0]
            if key in GRAPH_KEYS:
                graph[key] = []
                current = None
            continue
        if current and stripped.startswith("- "):
            graph.setdefault(current, []).append(stripped[2:].strip())
    return graph


def main() -> int:
    errors = []
    warnings = []
    skill_paths = sorted(ROOT.glob("plugins/*/skills/*/SKILL.md"))
    known_skills = set()
    for path in skill_paths:
        text = path.read_text(encoding="utf-8")
        fm, _ = parse_frontmatter(text)
        if fm.get("name"):
            known_skills.add(fm["name"])
    for path in skill_paths:
        text = path.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        graph = parse_graph(text)
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
        for key, targets in graph.items():
            for target in targets:
                if target in known_skills:
                    continue
                if target.startswith(("docs/", "plugins/")) and (ROOT / target).exists():
                    continue
                errors.append(f"{rel}: graph {key} target missing: {target}")
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
