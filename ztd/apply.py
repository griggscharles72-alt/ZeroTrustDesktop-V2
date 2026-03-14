#!/usr/bin/env python3
"""
README HEADER
ZeroTrustDesktop-V2 - Apply guard

Purpose:
- Provide a guarded apply entrypoint for future enforcement work.
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


def run_apply() -> int:
    paths = get_paths()
    cfg = load_config()
    allow_apply = bool(cfg.get("safety", {}).get("allow_apply", False))

    print(f"[apply] repo={paths.repo_root}")
    print(f"[apply] allow_apply={allow_apply}")

    if not allow_apply:
        print("[apply] REFUSED safety.allow_apply is false")
        return 1

    print("[apply] READY future apply actions not yet implemented")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_apply())
