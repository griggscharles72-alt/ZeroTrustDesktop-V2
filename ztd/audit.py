#!/usr/bin/env python3
"""
README HEADER
ZeroTrustDesktop-V2 - Audit module

Purpose:
- Provide a higher-level read-only audit summary for V2.
- Combine config, repo state, and latest generated artifacts into one audit view.
- Stay safe and deterministic.

Behavior:
- Reports grouped config, artifact, and entrypoint checks.
- Tracks severity for each item.
- Emits summary counts and an overall result.
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
    severity: str = "warn"


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
            "config.project_mode",
            str(project_cfg.get("mode", "read_only")) == "read_only",
            str(project_cfg.get("mode", "unknown")),
            "critical",
        )
    )
    items.append(
        AuditItem(
            "config.allow_apply",
            bool(safety_cfg.get("allow_apply", False)) is False,
            str(safety_cfg.get("allow_apply", False)),
            "critical",
        )
    )
    items.append(
        AuditItem(
            "config.allow_restore",
            bool(safety_cfg.get("allow_restore", False)) is False,
            str(safety_cfg.get("allow_restore", False)),
            "critical",
        )
    )
    items.append(
        AuditItem(
            "config.firewall_backend",
            bool(firewall_cfg.get("backend")),
            str(firewall_cfg.get("backend", "unset")),
            "warn",
        )
    )

    latest_snapshot = _latest_file(paths.snapshots_dir, "doctor_*.json")
    latest_report = _latest_file(paths.reports_dir, "doctor_*.md")

    items.append(
        AuditItem(
            "artifacts.doctor_snapshot_present",
            latest_snapshot is not None,
            str(latest_snapshot) if latest_snapshot else "none",
            "warn",
        )
    )
    items.append(
        AuditItem(
            "artifacts.doctor_report_present",
            latest_report is not None,
            str(latest_report) if latest_report else "none",
            "warn",
        )
    )
    items.append(
        AuditItem(
            "entrypoints.launcher_present",
            (paths.repo_root / "launch.sh").exists(),
            str(paths.repo_root / "launch.sh"),
            "warn",
        )
    )
    items.append(
        AuditItem(
            "entrypoints.wrapper_present",
            (paths.repo_root / "scripts" / "ztd").exists(),
            str(paths.repo_root / "scripts" / "ztd"),
            "warn",
        )
    )

    return items


def build_audit_summary(items: list[AuditItem]) -> dict[str, int | str]:
    ok_count = sum(1 for item in items if item.ok)
    warn_count = sum(1 for item in items if not item.ok)
    critical_warn_count = sum(1 for item in items if (not item.ok and item.severity == "critical"))
    result = "baseline_safe" if critical_warn_count == 0 else "needs_review"

    return {
        "ok_count": ok_count,
        "warn_count": warn_count,
        "critical_warn_count": critical_warn_count,
        "result": result,
    }


def run_audit() -> int:
    paths = get_paths()
    items = collect_audit()
    summary = build_audit_summary(items)

    logger.info("repo=%s", paths.repo_root)
    for item in items:
        state = "OK" if item.ok else "WARN"
        logger.info("%s %s [%s]: %s", state, item.name, item.severity, item.detail)

    logger.info("INFO summary.ok_count: %s", summary["ok_count"])
    logger.info("INFO summary.warn_count: %s", summary["warn_count"])
    logger.info("INFO summary.critical_warn_count: %s", summary["critical_warn_count"])
    logger.info("INFO summary.result: %s", summary["result"])

    return 0


if __name__ == "__main__":
    raise SystemExit(run_audit())
