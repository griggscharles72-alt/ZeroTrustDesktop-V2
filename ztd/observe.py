#!/usr/bin/env python3
"""
README HEADER
ZeroTrustDesktop-V2 - Observe module

Purpose:
- Provide a lightweight read-only observation snapshot for the local machine.
- Surface recent filesystem and runtime artifact state without changing anything.
- Stay safe, fast, and deterministic.

Behavior:
- Reports latest doctor snapshot/report.
- Reports latest files in reports, snapshots, diffs, and logs.
- Gives a compact operator view of recent repo activity.
- Uses shared logging utilities for consistent console output.

Author:
- SABLE + Elliot
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ztd.logging_utils import get_logger
from ztd.paths import get_paths

logger = get_logger("ztd.observe")


@dataclass
class ObserveItem:
    name: str
    ok: bool
    detail: str


def _latest_file(directory: Path, pattern: str = "*") -> Path | None:
    matches = sorted(
        [p for p in directory.glob(pattern) if p.is_file() and p.name != ".gitkeep"],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return matches[0] if matches else None


def collect_observation() -> list[ObserveItem]:
    paths = get_paths()
    items: list[ObserveItem] = []

    latest_doctor_snapshot = _latest_file(paths.snapshots_dir, "doctor_*.json")
    latest_doctor_report = _latest_file(paths.reports_dir, "doctor_*.md")
    latest_diff = _latest_file(paths.diffs_dir, "*")
    latest_log = _latest_file(paths.logs_dir, "*")

    items.append(ObserveItem("latest_doctor_snapshot", latest_doctor_snapshot is not None, str(latest_doctor_snapshot) if latest_doctor_snapshot else "none"))
    items.append(ObserveItem("latest_doctor_report", latest_doctor_report is not None, str(latest_doctor_report) if latest_doctor_report else "none"))
    items.append(ObserveItem("latest_diff", latest_diff is not None, str(latest_diff) if latest_diff else "none"))
    items.append(ObserveItem("latest_log", latest_log is not None, str(latest_log) if latest_log else "none"))

    for label, directory in (
        ("reports_dir", paths.reports_dir),
        ("snapshots_dir", paths.snapshots_dir),
        ("diffs_dir", paths.diffs_dir),
        ("logs_dir", paths.logs_dir),
    ):
        count = len([p for p in directory.iterdir() if p.is_file() and p.name != ".gitkeep"])
        items.append(ObserveItem(f"{label}_file_count", True, str(count)))

    return items


def run_observe() -> int:
    paths = get_paths()
    items = collect_observation()

    logger.info("repo=%s", paths.repo_root)
    for item in items:
        state = "OK" if item.ok else "WARN"
        logger.info("%s %s: %s", state, item.name, item.detail)

    return 0


if __name__ == "__main__":
    raise SystemExit(run_observe())