#!/usr/bin/env python3
"""Configure Home Assistant MCP profiles for Codex or Claude Code."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

SAFE_BARE_KEY = re.compile(r"^[A-Za-z0-9_-]+$")
DEFAULT_HA_TOKEN_ENV = "HOMEASSISTANT_TOKEN"
DEFAULT_HA_URL_ENV = "HOMEASSISTANT_URL"
DEFAULT_AGENT_URL_ENV = "HA_AGENT_URL"
DEFAULT_AGENT_KEY_ENV = "HA_AGENT_KEY"
DEFAULT_HTTP_PORT = 8123
DEFAULT_OFFICIAL_PATH = "/api/mcp"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Configure Home Assistant MCP servers for Codex or Claude Code.",
    )
    parser.add_argument(
        "host",
        nargs="?",
        help="Home Assistant host or URL, for example homeassistant.local or http://homeassistant:8123.",
    )
    parser.add_argument(
        "--client",
        choices=("codex", "claude"),
        default="codex",
        help=(
            "Target agent host. codex writes Codex config.toml (default); "
            "claude prints the equivalent `claude mcp add-json` commands to run."
        ),
    )
    parser.add_argument(
        "--profile",
        choices=("observer", "builder", "deployer", "full"),
        default="builder",
        help="MCP set to configure. Default: builder.",
    )
    parser.add_argument("--scheme", choices=("http", "https"), help="Scheme for bare hosts.")
    parser.add_argument("--https", action="store_true", help="Shortcut for --scheme https.")
    parser.add_argument("--port", type=int, help="Port for bare hosts.")
    parser.add_argument(
        "--ha-url-env",
        default=DEFAULT_HA_URL_ENV,
        help=(
            "Env var name to pass to ha-mcp. The setup writes the normalized host URL "
            f"under this env key. Default: {DEFAULT_HA_URL_ENV}."
        ),
    )
    parser.add_argument(
        "--ha-token-env",
        default=DEFAULT_HA_TOKEN_ENV,
        help=f"Env var containing the Home Assistant token. Default: {DEFAULT_HA_TOKEN_ENV}.",
    )
    parser.add_argument(
        "--agent-url-env",
        default=DEFAULT_AGENT_URL_ENV,
        help=f"Env var containing the Vibecode agent URL. Default: {DEFAULT_AGENT_URL_ENV}.",
    )
    parser.add_argument(
        "--agent-key-env",
        default=DEFAULT_AGENT_KEY_ENV,
        help=f"Env var containing the Vibecode agent key. Default: {DEFAULT_AGENT_KEY_ENV}.",
    )
    parser.add_argument(
        "--include-deployer",
        action="store_true",
        help="Allow configuring high-privilege Vibecode deployer MCP for --profile full.",
    )
    parser.add_argument(
        "--codex-home",
        default=os.environ.get("CODEX_HOME", "~/.codex"),
        help="Codex home directory (only used with --client codex). Default: CODEX_HOME or ~/.codex.",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-backup", action="store_true")
    return parser.parse_args(argv)


def validate_name(flag: str, value: str) -> bool:
    if SAFE_BARE_KEY.fullmatch(value):
        return True
    print(f"error: {flag} must contain only letters, numbers, underscores, and hyphens", file=sys.stderr)
    return False


def normalize_ha_url(raw_host: str, args: argparse.Namespace) -> str:
    raw_host = raw_host.strip()
    if not raw_host:
        raise ValueError("host must not be empty")
    if args.scheme and args.https and args.scheme != "https":
        raise ValueError("--https conflicts with --scheme http")

    default_scheme = args.scheme or ("https" if args.https else "http")
    had_scheme = "://" in raw_host
    parsed = urlsplit(raw_host if had_scheme else f"{default_scheme}://{raw_host}")
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Home Assistant URL must use http or https")
    if parsed.username or parsed.password:
        raise ValueError("do not put credentials in the Home Assistant URL")
    if parsed.query or parsed.fragment:
        raise ValueError("query strings and fragments are not supported")
    if not parsed.hostname:
        raise ValueError("could not determine a host name from the Home Assistant URL")

    port = args.port
    if port is None:
        try:
            port = parsed.port
        except ValueError as exc:
            raise ValueError(f"invalid port in host: {exc}") from exc
    if port is None and not had_scheme and parsed.scheme == "http":
        port = DEFAULT_HTTP_PORT
    if port is not None and not (1 <= port <= 65535):
        raise ValueError("port must be between 1 and 65535")

    hostname = parsed.hostname
    if ":" in hostname and not hostname.startswith("["):
        hostname = f"[{hostname}]"
    netloc = hostname if port is None else f"{hostname}:{port}"
    path = parsed.path if parsed.path and parsed.path != "/" else ""
    return urlunsplit((parsed.scheme, netloc, path.rstrip("/"), "", ""))


def official_mcp_url(base_url: str) -> str:
    return base_url.rstrip("/") + DEFAULT_OFFICIAL_PATH


# --- Server selection (shared by both render paths so they cannot drift) -----


def selected_server_names(args: argparse.Namespace) -> list[str]:
    names: list[str] = []
    if args.profile in {"observer", "builder", "full"}:
        names.append("home-assistant-official")
    if args.profile in {"builder", "full"}:
        names.append("home-assistant-config-uvx")
    if args.profile == "deployer" or (args.profile == "full" and args.include_deployer):
        names.append("home-assistant-vibecode")
    return names


def require_base_url(names: list[str], base_url: str | None) -> None:
    if base_url is None and {"home-assistant-official", "home-assistant-config-uvx"} & set(names):
        raise ValueError("host is required for observer, builder, and full profiles")


def required_envs(args: argparse.Namespace, names: list[str]) -> set[str]:
    envs: set[str] = set()
    if {"home-assistant-official", "home-assistant-config-uvx"} & set(names):
        envs.add(args.ha_token_env)
    if "home-assistant-vibecode" in names:
        envs.update({args.agent_url_env, args.agent_key_env})
    return envs


# --- Codex render path (TOML in config.toml) ---------------------------------


def split_toml_path(header: str) -> list[str]:
    parts: list[str] = []
    buf: list[str] = []
    in_quote = False
    escaped = False
    for char in header.strip():
        if escaped:
            buf.append(char)
            escaped = False
            continue
        if in_quote and char == "\\":
            escaped = True
            continue
        if char == '"':
            in_quote = not in_quote
            continue
        if char == "." and not in_quote:
            parts.append("".join(buf).strip())
            buf = []
            continue
        buf.append(char)
    parts.append("".join(buf).strip())
    return parts


def is_target_mcp_header(line: str, server_names: set[str]) -> bool:
    stripped = line.strip()
    if not stripped.startswith("[") or stripped.startswith("[["):
        return False
    end = stripped.find("]")
    if end == -1:
        return False
    parts = split_toml_path(stripped[1:end].strip())
    return len(parts) >= 2 and parts[0] == "mcp_servers" and parts[1] in server_names


def remove_existing_server_sections(text: str, server_names: set[str]) -> str:
    kept: list[str] = []
    skipping = False
    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        is_header = stripped.startswith("[") and not stripped.startswith("[[")
        if is_header:
            skipping = is_target_mcp_header(line, server_names)
        if not skipping:
            kept.append(line)
    return "".join(kept).rstrip() + ("\n" if kept else "")


def toml_key(key: str) -> str:
    return key if SAFE_BARE_KEY.fullmatch(key) else json.dumps(key)


def toml_string(value: str) -> str:
    return json.dumps(value)


def toml_array(values: list[str]) -> str:
    return "[" + ", ".join(toml_string(value) for value in values) + "]"


def official_block(url: str, token_env: str) -> str:
    return (
        f"[mcp_servers.{toml_key('home-assistant-official')}]\n"
        f"url = {toml_string(url)}\n"
        f"bearer_token_env_var = {toml_string(token_env)}\n"
        "startup_timeout_sec = 10.0\n"
    )


def ha_mcp_uvx_block(base_url: str, url_env: str, token_env: str) -> str:
    return (
        f"[mcp_servers.{toml_key('home-assistant-config-uvx')}]\n"
        'command = "uvx"\n'
        'args = ["ha-mcp@latest"]\n'
        f"env_vars = {toml_array([token_env])}\n"
        "startup_timeout_sec = 30.0\n"
        "\n"
        "[mcp_servers.home-assistant-config-uvx.env]\n"
        f"{url_env} = {toml_string(base_url)}\n"
    )


def vibecode_block(agent_url_env: str, agent_key_env: str) -> str:
    return (
        f"[mcp_servers.{toml_key('home-assistant-vibecode')}]\n"
        'command = "npx"\n'
        'args = ["-y", "@coolver/home-assistant-mcp@latest"]\n'
        f"env_vars = {toml_array([agent_url_env, agent_key_env])}\n"
        "startup_timeout_sec = 30.0\n"
    )


def codex_blocks(names: list[str], args: argparse.Namespace, base_url: str | None) -> dict[str, str]:
    blocks: dict[str, str] = {}
    for name in names:
        if name == "home-assistant-official":
            assert base_url is not None  # guaranteed by require_base_url
            blocks[name] = official_block(official_mcp_url(base_url), args.ha_token_env)
        elif name == "home-assistant-config-uvx":
            assert base_url is not None  # guaranteed by require_base_url
            blocks[name] = ha_mcp_uvx_block(base_url, args.ha_url_env, args.ha_token_env)
        elif name == "home-assistant-vibecode":
            blocks[name] = vibecode_block(args.agent_url_env, args.agent_key_env)
    return blocks


def write_config(codex_home: Path, blocks: dict[str, str], dry_run: bool, backup: bool) -> Path | None:
    rendered = "\n".join(block.rstrip() for block in blocks.values()).rstrip() + "\n"
    if dry_run:
        print(rendered, end="")
        return None

    codex_home.mkdir(parents=True, exist_ok=True)
    config_path = codex_home / "config.toml"
    existing = config_path.read_text(encoding="utf-8") if config_path.exists() else ""
    updated = remove_existing_server_sections(existing, set(blocks))
    if updated and not updated.endswith("\n"):
        updated += "\n"
    updated += ("\n" if updated.strip() else "") + rendered

    backup_path = None
    if backup and config_path.exists():
        stamp = time.strftime("%Y%m%d-%H%M%S")
        backup_path = config_path.with_name(f"{config_path.name}.{stamp}.bak")
        shutil.copy2(config_path, backup_path)
    config_path.write_text(updated, encoding="utf-8")
    return backup_path


def run_codex(args: argparse.Namespace, names: list[str], base_url: str | None) -> int:
    blocks = codex_blocks(names, args, base_url)
    backup_path = write_config(
        Path(args.codex_home).expanduser(), blocks, args.dry_run, not args.no_backup
    )
    if args.dry_run:
        return 0
    print(f"Configured Home Assistant MCP profile `{args.profile}` for Codex")
    for name in blocks:
        print(f"- {name}")
    if backup_path:
        print(f"Backup: {backup_path}")
    missing = sorted({name for name in required_envs(args, names) if name not in os.environ})
    if missing:
        print(f"Warning: not set in this process: {', '.join(missing)}")
    print("Restart Codex, then use /mcp verbose to confirm startup.")
    return 0


# --- Claude Code render path (claude mcp add-json commands) -------------------


def shell_single_quote(value: str) -> str:
    return "'" + value.replace("'", "'\\''") + "'"


def env_ref(name: str) -> str:
    return "${" + name + "}"


def claude_spec(name: str, args: argparse.Namespace, base_url: str | None) -> dict:
    if name == "home-assistant-official":
        assert base_url is not None  # guaranteed by require_base_url
        return {
            "type": "http",
            "url": official_mcp_url(base_url),
            "headers": {"Authorization": f"Bearer {env_ref(args.ha_token_env)}"},
        }
    if name == "home-assistant-config-uvx":
        assert base_url is not None  # guaranteed by require_base_url
        return {
            "command": "uvx",
            "args": ["ha-mcp@latest"],
            "env": {args.ha_url_env: base_url, args.ha_token_env: env_ref(args.ha_token_env)},
        }
    if name == "home-assistant-vibecode":
        return {
            "command": "npx",
            "args": ["-y", "@coolver/home-assistant-mcp@latest"],
            "env": {
                args.agent_url_env: env_ref(args.agent_url_env),
                args.agent_key_env: env_ref(args.agent_key_env),
            },
        }
    raise ValueError(f"unknown server name: {name}")


def run_claude(args: argparse.Namespace, names: list[str], base_url: str | None) -> int:
    print(f"# Claude Code setup for Home Assistant MCP profile `{args.profile}`")
    print("# Run each command, then restart Claude Code or run /mcp to confirm.")
    for name in names:
        spec = claude_spec(name, args, base_url)
        print(f"claude mcp add-json {name} {shell_single_quote(json.dumps(spec))}")
    missing = sorted({name for name in required_envs(args, names) if name not in os.environ})
    if missing:
        print(f"# Export before the MCP starts: {', '.join(missing)}")
    if "home-assistant-official" in names:
        print(
            "# The official server may require OAuth instead of a bearer token; "
            "see docs/install-claude-code.md for the OAuth variant."
        )
    return 0


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    for flag, value in (
        ("--ha-url-env", args.ha_url_env),
        ("--ha-token-env", args.ha_token_env),
        ("--agent-url-env", args.agent_url_env),
        ("--agent-key-env", args.agent_key_env),
    ):
        if not validate_name(flag, value):
            return 2

    try:
        base_url = normalize_ha_url(args.host, args) if args.host else None
        names = selected_server_names(args)
        require_base_url(names, base_url)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if not names:
        print("error: no MCP servers selected", file=sys.stderr)
        return 2
    if args.profile == "full" and not args.include_deployer:
        print("Skipping deployer MCP for full profile; pass --include-deployer to enable it.")

    if args.client == "claude":
        return run_claude(args, names, base_url)
    return run_codex(args, names, base_url)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
