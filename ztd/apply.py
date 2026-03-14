#!/usr/bin/env python3
"""
README HEADER
ZeroTrustDesktop-V2 - Apply guard

Purpose:
- Provide a guarded apply entrypoint for future enforcement work.
- Refuse state-changing actions unless explicitly allowed by config.
- Offer deterministic preview output without changing system state.

Behavior:
- Reads safety flags from config.
- Reports preview-only intent and future action lane.
- Refuses real apply by default.
- Does not change system state.

Author:
- SABLE + Elliot
"""

from __future__ import annotations

from dataclasses import dataclass

from ztd.config import load_config
from ztd.paths import get_paths


@dataclass
class ApplyPreview:
    mode: str
    allow_apply: bool
    would_write_firewall: bool
    would_write_restore_state: bool
    would_enforce_runtime: bool
    summary: str


def collect_apply_preview() -> ApplyPreview:
    cfg = load_config()
    allow_apply = bool(cfg.get("safety", {}).get("allow_apply", False))
    project_mode = str(cfg.get("project", {}).get("mode", "read_only"))

    return ApplyPreview(
        mode=project_mode,
        allow_apply=allow_apply,
        would_write_firewall=True,
        would_write_restore_state=True,
        would_enforce_runtime=True,
        summary="preview_only_no_state_change",
    )


def run_apply() -> int:
    paths = get_paths()
    preview = collect_apply_preview()

    print(f"[apply] repo={paths.repo_root}")
    print(f"[apply] mode={preview.mode}")
    print(f"[apply] allow_apply={preview.allow_apply}")
    print(f"[apply] would_write_firewall={preview.would_write_firewall}")
    print(f"[apply] would_write_restore_state={preview.would_write_restore_state}")
    print(f"[apply] would_enforce_runtime={preview.would_enforce_runtime}")
    print(f"[apply] summary={preview.summary}")

    if not preview.allow_apply:
        print("[apply] REFUSED safety.allow_apply is false")
        print("[apply] PREVIEW firewall/state/runtime actions remain blocked")
        return 1

    print("[apply] READY future apply actions not yet implemented")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_apply())
