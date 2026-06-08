#!/usr/bin/env python3
"""Validate the Codex marketplace catalog and plugin paths."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATHS = (
    Path(".codex-plugin/plugin.json"),
    Path(".claude-plugin/plugin.json"),
)
INSTALL_POLICIES = {"AVAILABLE", "INSTALLED_BY_DEFAULT", "NOT_AVAILABLE"}
AUTH_POLICIES = {"ON_INSTALL", "ON_USE"}
PLUGIN_ROOT_REF = re.compile(r"\$\{(?:CLAUDE|CODEX)_PLUGIN_ROOT\}/([^\"'\s]+)")


def load_json(path: Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def rel_exists(base: Path, rel: str) -> bool:
    return (base / rel).resolve().exists()


def iter_hook_commands(value):
    if isinstance(value, dict):
        command = value.get("command")
        if isinstance(command, str):
            yield command
        for item in value.values():
            yield from iter_hook_commands(item)
    elif isinstance(value, list):
        for item in value:
            yield from iter_hook_commands(item)


def validate_hook_template(name: str, plugin_dir: Path, errors: list[str]) -> None:
    # Templates live under hooks/templates/ so Claude Code does not auto-load
    # them on install (it only auto-discovers hooks/hooks.json). The legacy
    # hooks/hooks.json path is still scanned for backward compatibility.
    hook_paths = (
        plugin_dir / "hooks" / "templates" / "hooks.json",
        plugin_dir / "hooks" / "hooks.json",
    )
    for hooks_path in hook_paths:
        if not hooks_path.exists():
            continue
        rel_label = hooks_path.relative_to(plugin_dir)
        try:
            hooks = load_json(hooks_path)
        except json.JSONDecodeError as exc:
            errors.append(f"{name}: invalid {rel_label}: {exc}")
            continue
        for command in iter_hook_commands(hooks):
            for rel in PLUGIN_ROOT_REF.findall(command):
                if not (plugin_dir / rel).exists():
                    errors.append(f"{name}: hook command references missing file: {rel}")


def validate_local_plugin(name: str, root: Path, path: str, errors: list[str]) -> None:
    plugin_dir = (root / path).resolve()
    print(f"- {name}: {plugin_dir.relative_to(root)}")
    if not plugin_dir.exists():
        errors.append(f"{name}: source path missing: {path}")
        return
    manifest_path = next(
        (plugin_dir / rel for rel in MANIFEST_PATHS if (plugin_dir / rel).exists()),
        None,
    )
    if manifest_path is None:
        errors.append(f"{name}: missing .codex-plugin/plugin.json or .claude-plugin/plugin.json")
        return
    manifest = load_json(manifest_path)
    for field in ("skills", "mcpServers", "hooks", "commands"):
        rel = manifest.get(field)
        if rel and not rel_exists(plugin_dir, rel):
            errors.append(f"{name}: {field} path missing: {rel}")
    validate_hook_template(name, plugin_dir, errors)


def main() -> int:
    errors = []
    market = ROOT / ".agents" / "plugins" / "marketplace.json"
    data = load_json(market)
    print(f"Marketplace: {market.relative_to(ROOT)}")
    for entry in data.get("plugins", []):
        name = entry.get("name", "<missing>")
        source = entry.get("source", {})
        policy = entry.get("policy", {})
        installation = policy.get("installation", "AVAILABLE") if isinstance(policy, dict) else "AVAILABLE"
        authentication = policy.get("authentication", "ON_INSTALL") if isinstance(policy, dict) else "ON_INSTALL"
        if installation not in INSTALL_POLICIES:
            errors.append(f"{name}: unsupported installation policy: {installation}")
        if authentication not in AUTH_POLICIES:
            errors.append(f"{name}: unsupported authentication policy: {authentication}")
        if not isinstance(source, dict):
            errors.append(f"{name}: source must be an object")
            continue
        source_kind = source.get("source")
        if source_kind == "local":
            path = source.get("path")
            if not path:
                errors.append(f"{name}: local source missing path")
                continue
            validate_local_plugin(name, ROOT, path, errors)
            continue
        if source_kind in {"url", "git-subdir"}:
            url = source.get("url")
            if not url:
                errors.append(f"{name}: git source missing url")
            if source_kind == "git-subdir" and not source.get("path"):
                errors.append(f"{name}: git-subdir source missing path")
            print(f"- {name}: git {url}")
            continue
        errors.append(f"{name}: unsupported source kind: {source_kind}")
    if errors:
        print("Errors:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Marketplace validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
