#!/usr/bin/env python3
"""
README HEADER
ZeroTrustDesktop-V2 - Restore guard

Purpose:
- Provide a guarded restore entrypoint for future recovery work.
- Refuse state-changing actions unless explicitly allowed by config.
- Offer deterministic preview output without changing system state.

Behavior:
- Reads safety flags from config.
- Reports preview-only intent and future recovery lane.
- Refuses real restore by default.
- Does not change system state.

Author:
- SABLE + Elliot
"""

from __future__ import annotations

from dataclasses import dataclass

from ztd.config import load_config
from ztd.paths import get_paths


@dataclass
class RestorePreview:
    mode: str
    allow_restore: bool
    would_restore_firewall: bool
    would_restore_runtime: bool
    would_load_saved_state: bool
    summary: str


def collect_restore_preview() -> RestorePreview:
    cfg = load_config()
    allow_restore = bool(cfg.get("safety", {}).get("allow_restore", False))
    project_mode = str(cfg.get("project", {}).get("mode", "read_only"))

    return RestorePreview(
        mode=project_mode,
        allow_restore=allow_restore,
        would_restore_firewall=True,
        would_restore_runtime=True,
        would_load_saved_state=True,
        summary="preview_only_no_state_change",
    )


def run_restore() -> int:
    paths = get_paths()
    preview = collect_restore_preview()

    print(f"[restore] repo={paths.repo_root}")
    print(f"[restore] mode={preview.mode}")
    print(f"[restore] allow_restore={preview.allow_restore}")
    print(f"[restore] would_restore_firewall={preview.would_restore_firewall}")
    print(f"[restore] would_restore_runtime={preview.would_restore_runtime}")
    print(f"[restore] would_load_saved_state={preview.would_load_saved_state}")
    print(f"[restore] summary={preview.summary}")

    if not preview.allow_restore:
        print("[restore] REFUSED safety.allow_restore is false")
        print("[restore] PREVIEW firewall/runtime/state recovery remains blocked")
        return 1

    print("[restore] READY future restore actions not yet implemented")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_restore())
