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
        print(json.dumps({"decision": "warn", "message": message}))
    else:
        print(json.dumps({"decision": "allow", "message": "No Home Assistant safety warning."}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

