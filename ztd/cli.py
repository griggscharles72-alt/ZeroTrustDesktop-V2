#!/usr/bin/env python3
"""
README HEADER
ZeroTrustDesktop-V2 - CLI entrypoint

Purpose:
- Provide the canonical command router for V2.
- Support both explicit subcommands and launcher-driven selection.
- Keep command execution deterministic and easy to extend.

Behavior:
- Accepts an optional command argument.
- Falls back to launcher menu when no command is provided.
- Ensures runtime directories exist before command handling.
- Routes live commands to real modules when implemented.
- Keeps unfinished commands scaffold-safe.

Author:
- SABLE + Elliot
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ztd.audit import run_audit
from ztd.doctor import run_doctor
from ztd.launcher import VALID_COMMANDS, show_menu
from ztd.paths import get_paths
from ztd.status import run_status


def run_scaffold_command(command: str) -> int:
    paths = get_paths()
    print(f"[ztd] command={command}")
    print(f"[ztd] repo={paths.repo_root}")
    print(f"[ztd] output={paths.output_dir}")
    print("[ztd] scaffold aligned and ready for module implementation")
    return 0


def run_command(command: str) -> int:
    command = command.strip().lower()

    if command == "doctor":
        return run_doctor()

    if command == "status":
        return run_status()

    if command == "audit":
        return run_audit()

    return run_scaffold_command(command)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ztd", description="ZeroTrustDesktop-V2")
    parser.add_argument("command", nargs="?", choices=VALID_COMMANDS, help="Command to run")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    command = args.command or show_menu()
    return run_command(command)


if __name__ == "__main__":
    raise SystemExit(main())
