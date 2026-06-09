#!/usr/bin/env python3
"""Configure the official Home Assistant MCP Server for Codex or Claude Code."""

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

DEFAULT_NAME = "home-assistant-official"
DEFAULT_TOKEN_ENV = "HOMEASSISTANT_TOKEN"
DEFAULT_PATH = "/api/mcp"
DEFAULT_HTTP_PORT = 8123
SAFE_BARE_KEY = re.compile(r"^[A-Za-z0-9_-]+$")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Register Home Assistant's official /api/mcp endpoint for Codex or Claude Code.",
    )
    parser.add_argument(
        "host",
        help=(
            "Home Assistant host or URL. Examples: homeassistant.local, "
            "192.168.1.10:8123, https://ha.example.com"
        ),
    )
    parser.add_argument(
        "--client",
        choices=("codex", "claude"),
        default="codex",
        help=(
            "Target agent host. codex writes Codex config.toml (default); "
            "claude prints the equivalent `claude mcp add-json` command to run."
        ),
    )
    parser.add_argument(
        "--scheme",
        choices=("http", "https"),
        help="Scheme to use when HOST is not already a URL. Default: http.",
    )
    parser.add_argument(
        "--https",
        action="store_true",
        help="Shortcut for --scheme https when HOST is not already a URL.",
    )
    parser.add_argument(
        "--port",
        type=int,
        help=(
            "Port to use. Defaults to 8123 for http hosts without a port; "
            "https hosts omit a port unless supplied."
        ),
    )
    parser.add_argument(
        "--path",
        default=DEFAULT_PATH,
        help=f"MCP endpoint path. Default: {DEFAULT_PATH}.",
    )
    parser.add_argument(
        "--name",
        default=DEFAULT_NAME,
        help=f"MCP server name. Default: {DEFAULT_NAME}.",
    )
    parser.add_argument(
        "--token-env",
        default=DEFAULT_TOKEN_ENV,
        help=f"Environment variable containing the HA token. Default: {DEFAULT_TOKEN_ENV}.",
    )
    parser.add_argument(
        "--codex-home",
        default=os.environ.get("CODEX_HOME", "~/.codex"),
        help="Codex home directory (only used with --client codex). Default: CODEX_HOME or ~/.codex.",
    )
    parser.add_argument(
        "--startup-timeout",
        type=float,
        default=10.0,
        help="MCP startup timeout in seconds (Codex only). Default: 10.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the Codex config block without writing config.toml (Codex only).",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Do not create a timestamped config.toml backup before writing.",
    )
    return parser.parse_args(argv)


def normalize_url(raw_host: str, args: argparse.Namespace) -> str:
    raw_host = raw_host.strip()
    if not raw_host:
        raise ValueError("host must not be empty")

    if args.scheme and args.https and args.scheme != "https":
        raise ValueError("--https conflicts with --scheme http")

    default_scheme = args.scheme or ("https" if args.https else "http")
    had_scheme = "://" in raw_host
    candidate = raw_host if had_scheme else f"{default_scheme}://{raw_host}"
    parsed = urlsplit(candidate)

    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Home Assistant MCP URL must use http or https")
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

    path = args.path if args.path is not None else parsed.path
    if not path or path == "/":
        path = DEFAULT_PATH
    if not path.startswith("/"):
        path = f"/{path}"

    return urlunsplit((parsed.scheme, netloc, path, "", ""))


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


def is_target_mcp_header(line: str, server_name: str) -> bool:
    stripped = line.strip()
    if not stripped.startswith("[") or stripped.startswith("[["):
        return False
    end = stripped.find("]")
    if end == -1:
        return False
    header = stripped[1:end].strip()
    parts = split_toml_path(header)
    return len(parts) >= 2 and parts[0] == "mcp_servers" and parts[1] == server_name


def remove_existing_server_sections(text: str, server_name: str) -> str:
    kept: list[str] = []
    skipping = False
    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        is_header = stripped.startswith("[") and not stripped.startswith("[[")
        if is_header:
            skipping = is_target_mcp_header(line, server_name)
        if not skipping:
            kept.append(line)
    return "".join(kept).rstrip() + ("\n" if kept else "")


def toml_key(key: str) -> str:
    if SAFE_BARE_KEY.fullmatch(key):
        return key
    return json.dumps(key)


def toml_string(value: str) -> str:
    return json.dumps(value)


def config_block(
    server_name: str,
    url: str,
    token_env: str,
    startup_timeout: float,
) -> str:
    return (
        f"[mcp_servers.{toml_key(server_name)}]\n"
        f"url = {toml_string(url)}\n"
        f"bearer_token_env_var = {toml_string(token_env)}\n"
        f"startup_timeout_sec = {startup_timeout:.1f}\n"
    )


def write_config(
    codex_home: Path,
    server_name: str,
    block: str,
    dry_run: bool,
    backup: bool,
) -> Path | None:
    config_path = codex_home / "config.toml"
    if dry_run:
        print(block, end="")
        return None

    codex_home.mkdir(parents=True, exist_ok=True)
    existing = config_path.read_text(encoding="utf-8") if config_path.exists() else ""
    updated = remove_existing_server_sections(existing, server_name)
    if updated and not updated.endswith("\n"):
        updated += "\n"
    updated += ("\n" if updated.strip() else "") + block

    backup_path: Path | None = None
    if backup and config_path.exists():
        stamp = time.strftime("%Y%m%d-%H%M%S")
        backup_path = config_path.with_name(f"{config_path.name}.{stamp}.bak")
        shutil.copy2(config_path, backup_path)

    config_path.write_text(updated, encoding="utf-8")
    return backup_path


def shell_single_quote(value: str) -> str:
    return "'" + value.replace("'", "'\\''") + "'"


def run_codex(args: argparse.Namespace, url: str) -> int:
    block = config_block(args.name, url, args.token_env, args.startup_timeout)
    backup_path = write_config(
        codex_home=Path(args.codex_home).expanduser(),
        server_name=args.name,
        block=block,
        dry_run=args.dry_run,
        backup=not args.no_backup,
    )
    if args.dry_run:
        return 0
    print(f"Configured Codex MCP server `{args.name}`")
    print(f"URL: {url}")
    print(f"Token env: {args.token_env}")
    if backup_path:
        print(f"Backup: {backup_path}")
    if args.token_env not in os.environ:
        print(f"Warning: {args.token_env} is not set in this process")
    print("Restart Codex, then use /mcp verbose to confirm startup.")
    return 0


def run_claude(args: argparse.Namespace, url: str) -> int:
    spec = {
        "type": "http",
        "url": url,
        "headers": {"Authorization": "Bearer ${" + args.token_env + "}"},
    }
    print(f"# Claude Code setup for the official Home Assistant MCP server `{args.name}`")
    print(f"claude mcp add-json {args.name} {shell_single_quote(json.dumps(spec))}")
    if args.token_env not in os.environ:
        print(f"# Export {args.token_env} before the MCP starts.")
    print(
        "# The official server may require OAuth instead of a bearer token; "
        "see docs/install-claude-code.md for the OAuth variant."
    )
    print("# Then restart Claude Code or run /mcp to confirm.")
    return 0


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if not SAFE_BARE_KEY.fullmatch(args.name):
        print(
            "error: --name must contain only letters, numbers, underscores, and hyphens",
            file=sys.stderr,
        )
        return 2
    if not SAFE_BARE_KEY.fullmatch(args.token_env):
        print(
            "error: --token-env must contain only letters, numbers, underscores, and hyphens",
            file=sys.stderr,
        )
        return 2

    try:
        url = normalize_url(args.host, args)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.client == "claude":
        return run_claude(args, url)
    return run_codex(args, url)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
