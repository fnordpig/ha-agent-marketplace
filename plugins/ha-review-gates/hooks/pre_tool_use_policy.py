#!/usr/bin/env python3
"""Warn about sensitive Home Assistant operations in hook payloads."""

from __future__ import annotations

import json
import sys

DANGEROUS = [
    "delete", "remove", "rm -rf", "restart", "reboot", "hassio",
    "ha core restart", "docker compose down", ".storage", "secrets.yaml",
    "known_devices.yaml", "automations.yaml",
]


def _pre_tool_use_context(message: str) -> str:
    return json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "additionalContext": message,
        },
    })


def main() -> int:
    raw = sys.stdin.read()
    haystack = raw.lower()
    try:
        payload = json.loads(raw) if raw.strip() else {}
        haystack += " " + json.dumps(payload).lower()
    except json.JSONDecodeError:
        payload = {}
    hits = [term for term in DANGEROUS if term in haystack]
    if hits:
        message = "Home Assistant safety warning: sensitive operation detected: " + ", ".join(hits)
        print(_pre_tool_use_context(message))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
