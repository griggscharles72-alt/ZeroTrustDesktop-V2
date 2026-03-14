#!/usr/bin/env python3
"""
README HEADER
ZeroTrustDesktop-V2 - Audit module

Purpose:
- Provide a higher-level read-only audit summary for V2.
- Combine config, repo state, and latest generated artifacts into one audit view.
- Stay safe and deterministic.

Behavior:
- Reports current mode and safety flags from config.
- Reports latest doctor snapshot/report presence.
- Reports current repo readiness through a compact audit summary.

Author:
- SABLE + Elliot
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ztd.config import load_config
from ztd.paths import get_paths


@dataclass
class AuditItem:
    name: str
    ok: bool
    detail: str


def _latest_file(directory: Path, pattern: str) -> Path | None:
    matches = sorted(directory.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
    return matches[0] if matches else None


def collect_audit() -> list[AuditItem]:
    paths = get_paths()
    cfg = load_config()
    items: list[AuditItem] = []

    project_cfg = cfg.get("project", {})
    safety_cfg = cfg.get("safety", {})
    firewall_cfg = cfg.get("firewall", {})

    items.append(
        AuditItem(
            name="project_mode",
            ok=str(project_cfg.get("mode", "read_only")) == "read_only",
            detail=str(project_cfg.get("mode", "unknown")),
        )
    )

    items.append(
        AuditItem(
            name="allow_apply",
            ok=bool(safety_cfg.get("allow_apply", False)) is False,
            detail=str(safety_cfg.get("allow_apply", False)),
        )
    )

    items.append(
        AuditItem(
            name="allow_restore",
            ok=bool(safety_cfg.get("allow_restore", False)) is False,
            detail=str(safety_cfg.get("allow_restore", False)),
        )
    )

    items.append(
        AuditItem(
            name="firewall_backend",
            ok=bool(firewall_cfg.get("backend")),
            detail=str(firewall_cfg.get("backend", "unset")),
        )
    )

    latest_snapshot = _latest_file(paths.snapshots_dir, "doctor_*.json")
    latest_report = _latest_file(paths.reports_dir, "doctor_*.md")

    items.append(
        AuditItem(
            name="doctor_snapshot_present",
            ok=latest_snapshot is not None,
            detail=str(latest_snapshot) if latest_snapshot else "none",
        )
    )

    items.append(
        AuditItem(
            name="doctor_report_present",
            ok=latest_report is not None,
            detail=str(latest_report) if latest_report else "none",
        )
    )

    items.append(
        AuditItem(
            name="launcher_present",
            ok=(paths.repo_root / "launch.sh").exists(),
            detail=str(paths.repo_root / "launch.sh"),
        )
    )

    items.append(
        AuditItem(
            name="wrapper_present",
            ok=(paths.repo_root / "scripts" / "ztd").exists(),
            detail=str(paths.repo_root / "scripts" / "ztd"),
        )
    )

    return items


def run_audit() -> int:
    paths = get_paths()
    items = collect_audit()

    print(f"[audit] repo={paths.repo_root}")
    for item in items:
        state = "OK" if item.ok else "WARN"
        print(f"[audit] {state} {item.name}: {item.detail}")

    return 0


if __name__ == "__main__":
    raise SystemExit(run_audit())
