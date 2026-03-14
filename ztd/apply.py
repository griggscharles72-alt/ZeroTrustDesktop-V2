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
- Reads latest state and diff artifacts when available.
- Refuses real apply by default.
- Does not change system state.

Author:
- SABLE + Elliot
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ztd.config import load_config
from ztd.paths import get_paths


@dataclass
class ApplyPreview:
    mode: str
    allow_apply: bool
    would_write_firewall: bool
    would_write_restore_state: bool
    would_enforce_runtime: bool
    latest_state_file: str
    latest_diff_file: str
    latest_diff_status: str
    latest_changed_count: int
    summary: str


def _latest_file(directory: Path, pattern: str) -> Path | None:
    matches = sorted(
        [p for p in directory.glob(pattern) if p.is_file() and p.name != ".gitkeep"],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return matches[0] if matches else None


def _load_json(path: Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def collect_apply_preview() -> ApplyPreview:
    cfg = load_config()
    paths = get_paths()

    allow_apply = bool(cfg.get("safety", {}).get("allow_apply", False))
    project_mode = str(cfg.get("project", {}).get("mode", "read_only"))

    latest_state = _latest_file(paths.state_dir, "state_*.json")
    latest_diff = _latest_file(paths.diffs_dir, "state_diff_*.json")
    latest_diff_payload = _load_json(latest_diff) or {}

    latest_diff_status = str(latest_diff_payload.get("status", "none"))
    latest_changed_count = int(latest_diff_payload.get("changed_count", 0))

    summary = "preview_only_no_state_change"
    if latest_diff_status == "changed" and latest_changed_count > 0:
        summary = "preview_only_changes_detected"
    elif latest_diff_status == "unchanged":
        summary = "preview_only_baseline_matches"
    elif latest_diff_status == "initial_state":
        summary = "preview_only_initial_state"

    return ApplyPreview(
        mode=project_mode,
        allow_apply=allow_apply,
        would_write_firewall=True,
        would_write_restore_state=True,
        would_enforce_runtime=True,
        latest_state_file=str(latest_state) if latest_state else "none",
        latest_diff_file=str(latest_diff) if latest_diff else "none",
        latest_diff_status=latest_diff_status,
        latest_changed_count=latest_changed_count,
        summary=summary,
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
    print(f"[apply] latest_state_file={preview.latest_state_file}")
    print(f"[apply] latest_diff_file={preview.latest_diff_file}")
    print(f"[apply] latest_diff_status={preview.latest_diff_status}")
    print(f"[apply] latest_changed_count={preview.latest_changed_count}")
    print(f"[apply] summary={preview.summary}")

    if not preview.allow_apply:
        print("[apply] REFUSED safety.allow_apply is false")
        print("[apply] PREVIEW firewall/state/runtime actions remain blocked")
        return 1

    print("[apply] READY future apply actions not yet implemented")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_apply())
