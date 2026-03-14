#!/usr/bin/env python3
"""
README HEADER
ZeroTrustDesktop-V2 - CLI entrypoint

Purpose:
- Provide a clean command router for V2.
- Keep operator surface minimal while architecture stays modular.

Current behavior:
- Safe scaffold phase.
- Commands print placeholder status until modules are implemented.

Author:
- Elliot + ChatGPT

INSTRUCTIONS
- This file is the command router for:
  doctor, audit, status, observe, apply, restore
"""

from __future__ import annotations

import argparse
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _ensure_output_dirs() -> None:
    base = _repo_root() / "output"
    for sub in ("reports", "snapshots", "diffs", "logs"):
        (base / sub).mkdir(parents=True, exist_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(prog="ztd", description="ZeroTrustDesktop-V2")
    parser.add_argument(
        "command",
        choices=["doctor", "audit", "status", "observe", "apply", "restore"],
        help="Command to run",
    )
    args = parser.parse_args()

    _ensure_output_dirs()
    print(f"[ztd] command={args.command}")
    print(f"[ztd] repo={_repo_root()}")
    print("[ztd] scaffold aligned and ready for module implementation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
