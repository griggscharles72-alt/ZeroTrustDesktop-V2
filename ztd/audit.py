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
- Uses shared logging utilities for consistent console output.

Author:
- SABLE + Elliot
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ztd.config import load_config
from ztd.logging_utils import get_logger
from ztd.paths import get_paths

logger = get_logger("ztd.audit")


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

    items.append(AuditItem("project_mode", str(project_cfg.get("mode", "read_only")) == "read_only", str(project_cfg.get("mode", "unknown"))))
    items.append(AuditItem("allow_apply", bool(safety_cfg.get("allow_apply", False)) is False, str(safety_cfg.get("allow_apply", False))))
    items.append(AuditItem("allow_restore", bool(safety_cfg.get("allow_restore", False)) is False, str(safety_cfg.get("allow_restore", False))))
    items.append(AuditItem("firewall_backend", bool(firewall_cfg.get("backend")), str(firewall_cfg.get("backend", "unset"))))

    latest_snapshot = _latest_file(paths.snapshots_dir, "doctor_*.json")
    latest_report = _latest_file(paths.reports_dir, "doctor_*.md")

    items.append(AuditItem("doctor_snapshot_present", latest_snapshot is not None, str(latest_snapshot) if latest_snapshot else "none"))
    items.append(AuditItem("doctor_report_present", latest_report is not None, str(latest_report) if latest_report else "none"))
    items.append(AuditItem("launcher_present", (paths.repo_root / "launch.sh").exists(), str(paths.repo_root / "launch.sh")))
    items.append(AuditItem("wrapper_present", (paths.repo_root / "scripts" / "ztd").exists(), str(paths.repo_root / "scripts" / "ztd")))

    return items


def run_audit() -> int:
    paths = get_paths()
    items = collect_audit()

    logger.info("repo=%s", paths.repo_root)
    for item in items:
        state = "OK" if item.ok else "WARN"
        logger.info("%s %s: %s", state, item.name, item.detail)

    return 0


if __name__ == "__main__":
    raise SystemExit(run_audit())