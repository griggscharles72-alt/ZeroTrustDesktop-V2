#!/usr/bin/env python3
"""
README HEADER
ZeroTrustDesktop-V2 - Launcher routing

Purpose:
- Provide a simple interactive launcher for V2.
- Route menu selections into the same command model used by the CLI.
- Keep the operator surface easy while preserving deterministic behavior.

Behavior:
- Reads launcher defaults from config.
- Shows a simple menu when no command is supplied.
- Returns a normalized command string for CLI execution.
- Supports both direct-script and module execution.

Author:
- SABLE + Elliot
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Iterable

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ztd.config import load_config

VALID_COMMANDS = ("doctor", "audit", "status", "observe", "apply", "restore")


def normalize_command(command: str) -> str:
    value = command.strip().lower()
    if value not in VALID_COMMANDS:
        raise ValueError(f"Unsupported command: {command}")
    return value


def get_default_command() -> str:
    cfg = load_config()
    command = str(cfg.get("launcher", {}).get("default_command", "status"))
    return normalize_command(command)


def show_menu(options: Iterable[str] = VALID_COMMANDS) -> str:
    options = tuple(options)

    print()
    print("ZeroTrustDesktop-V2")
    for idx, name in enumerate(options, start=1):
        print(f"{idx}) {name.capitalize()}")
    print(f"{len(options) + 1}) Exit")
    print()

    raw = input("Select: ").strip()
    if not raw:
        return get_default_command()

    if raw.isdigit():
        index = int(raw)
        if 1 <= index <= len(options):
            return options[index - 1]
        if index == len(options) + 1:
            raise SystemExit(0)

    return normalize_command(raw)


if __name__ == "__main__":
    try:
        selected = show_menu()
        print(f"selected={selected}")
    except SystemExit:
        raise
    except Exception as exc:
        print(f"launcher_error={exc}")
        raise SystemExit(1)


"""
INSTRUCTIONS
1. Save this file as:
   ztd/launcher.py

2. Test direct script mode with:
   cd /home/pc-10/repos/ZeroTrustDesktop-V2 && printf '3\n' | ./.venv/bin/python ztd/launcher.py

3. Test module mode with:
   cd /home/pc-10/repos/ZeroTrustDesktop-V2 && printf '3\n' | ./.venv/bin/python -m ztd.launcher
"""
