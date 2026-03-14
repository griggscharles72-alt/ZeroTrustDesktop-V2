#!/usr/bin/env python3
"""
README HEADER
ZeroTrustDesktop-V2 - Status summary

Purpose:
- Provide a quick operational status view for the V2 repo.
- Summarize core readiness and latest generated doctor artifacts.
- Stay read-only and safe.

Behavior:
- Checks config files, launcher/wrapper presence, and output directories.
- Finds the most recent doctor JSON snapshot and markdown report.
- Reports repo branch, commit, cleanliness, and Python runtime details.
- Uses shared logging utilities for consistent console output.

Author:
- SABLE + Elliot
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from ztd.logging_utils import get_logger
from ztd.paths import get_paths

logger = get_logger("ztd.status")


@dataclass
class StatusItem:
    name: str
    ok: bool
    detail: str


def _latest_file(directory: Path, pattern: str) -> Path | None:
    matches = sorted(directory.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
    return matches[0] if matches else None


def _git_output(args: list[str]) -> tuple[bool, str]:
    try:
        completed = subprocess.run(
            ["git", *args],
            capture_output=True,
            text=True,
            cwd=get_paths().repo_root,
            timeout=10,
            check=False,
        )
        output = (completed.stdout or completed.stderr).strip()
        return completed.returncode == 0, output
    except Exception as exc:
        return False, str(exc)


def collect_status() -> list[StatusItem]:
    paths = get_paths()
    items: list[StatusItem] = []

    items.append(StatusItem("repo_root", paths.repo_root.exists(), str(paths.repo_root)))
    items.append(StatusItem("default_config", paths.default_config_file.exists(), str(paths.default_config_file)))
    items.append(StatusItem("local_config", paths.local_config_file.exists(), str(paths.local_config_file)))
    items.append(StatusItem("launch_sh", (paths.repo_root / "launch.sh").exists(), str(paths.repo_root / "launch.sh")))
    items.append(StatusItem("scripts_ztd", (paths.repo_root / "scripts" / "ztd").exists(), str(paths.repo_root / "scripts" / "ztd")))

    for name, path in (
        ("reports_dir", paths.reports_dir),
        ("snapshots_dir", paths.snapshots_dir),
        ("diffs_dir", paths.diffs_dir),
        ("logs_dir", paths.logs_dir),
        ("state_dir", paths.state_dir),
    ):
        items.append(StatusItem(name, path.exists(), str(path)))

    latest_snapshot = _latest_file(paths.snapshots_dir, "doctor_*.json")
    latest_report = _latest_file(paths.reports_dir, "doctor_*.md")

    items.append(StatusItem("latest_doctor_snapshot", latest_snapshot is not None, str(latest_snapshot) if latest_snapshot else "none"))
    items.append(StatusItem("latest_doctor_report", latest_report is not None, str(latest_report) if latest_report else "none"))

    ok, branch = _git_output(["branch", "--show-current"])
    items.append(StatusItem("git_branch", ok and bool(branch), branch or "unknown"))

    ok, commit = _git_output(["rev-parse", "--short", "HEAD"])
    items.append(StatusItem("git_commit", ok and bool(commit), commit or "unknown"))

    ok, dirty = _git_output(["status", "--porcelain"])
    clean = ok and dirty == ""
    items.append(StatusItem("git_worktree_clean", clean, "clean" if clean else (dirty or "dirty")))

    items.append(StatusItem("python_executable", Path(sys.executable).exists(), sys.executable))
    items.append(StatusItem("python_version", True, sys.version.split()[0]))

    venv_path = Path(sys.prefix)
    items.append(StatusItem("venv_path", venv_path.exists(), str(venv_path)))

    return items


def run_status() -> int:
    paths = get_paths()
    items = collect_status()

    logger.info("repo=%s", paths.repo_root)
    for item in items:
        state = "OK" if item.ok else "WARN"
        logger.info("%s %s: %s", state, item.name, item.detail)

    return 0


if __name__ == "__main__":
    raise SystemExit(run_status())
