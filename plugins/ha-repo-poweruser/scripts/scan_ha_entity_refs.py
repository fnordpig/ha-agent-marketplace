#!/usr/bin/env python3
"""Plugin-local wrapper for the root Home Assistant entity scanner."""

from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[3]
runpy.run_path(str(ROOT / "scripts" / "scan_ha_entity_refs.py"), run_name="__main__")

