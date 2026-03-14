#!/usr/bin/env python3
"""
README HEADER
ZeroTrustDesktop-V2 - Restore guard

Purpose:
- Provide a guarded restore entrypoint for future recovery work.
- Refuse state-changing actions unless explicitly allowed by config.

Behavior:
- Reads safety flags from config.
- Refuses by default.
- Prints deterministic refusal status without changing system state.

Author:
- SABLE + Elliot
"""

from __future__ import annotations

from ztd.config import load_config
from ztd.paths import get_paths


def run_restore() -> int:
    paths = get_paths()
    cfg = load_config()
    allow_restore = bool(cfg.get("safety", {}).get("allow_restore", False))

    print(f"[restore] repo={paths.repo_root}")
    print(f"[restore] allow_restore={allow_restore}")

    if not allow_restore:
        print("[restore] REFUSED safety.allow_restore is false")
        return 1

    print("[restore] READY future restore actions not yet implemented")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_restore())
