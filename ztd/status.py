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
- Prints a compact status summary for operator use.

Author:
- SABLE + Elliot
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ztd.paths import get_paths


@dataclass
class StatusItem:
    name: str
    ok: bool
    detail: str


def _latest_file(directory: Path, pattern: str) -> Path | None:
    matches = sorted(directory.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
    return matches[0] if matches else None


def collect_status() -> list[StatusItem]:
    paths = get_paths()
    items: list[StatusItem] = []

    items.append(
        StatusItem(
            name="repo_root",
            ok=paths.repo_root.exists(),
            detail=str(paths.repo_root),
        )
    )

    items.append(
        StatusItem(
            name="default_config",
            ok=paths.default_config_file.exists(),
            detail=str(paths.default_config_file),
        )
    )

    items.append(
        StatusItem(
            name="local_config",
            ok=paths.local_config_file.exists(),
            detail=str(paths.local_config_file),
        )
    )

    items.append(
        StatusItem(
            name="launch_sh",
            ok=(paths.repo_root / "launch.sh").exists(),
            detail=str(paths.repo_root / "launch.sh"),
        )
    )

    items.append(
        StatusItem(
            name="scripts_ztd",
            ok=(paths.repo_root / "scripts" / "ztd").exists(),
            detail=str(paths.repo_root / "scripts" / "ztd"),
        )
    )

    for name, path in (
        ("reports_dir", paths.reports_dir),
        ("snapshots_dir", paths.snapshots_dir),
        ("diffs_dir", paths.diffs_dir),
        ("logs_dir", paths.logs_dir),
        ("state_dir", paths.state_dir),
    ):
        items.append(
            StatusItem(
                name=name,
                ok=path.exists(),
                detail=str(path),
            )
        )

    latest_snapshot = _latest_file(paths.snapshots_dir, "doctor_*.json")
    latest_report = _latest_file(paths.reports_dir, "doctor_*.md")

    items.append(
        StatusItem(
            name="latest_doctor_snapshot",
            ok=latest_snapshot is not None,
            detail=str(latest_snapshot) if latest_snapshot else "none",
        )
    )

    items.append(
        StatusItem(
            name="latest_doctor_report",
            ok=latest_report is not None,
            detail=str(latest_report) if latest_report else "none",
        )
    )

    return items


def run_status() -> int:
    paths = get_paths()
    items = collect_status()

    print(f"[status] repo={paths.repo_root}")
    for item in items:
        state = "OK" if item.ok else "WARN"
        print(f"[status] {state} {item.name}: {item.detail}")

    return 0


if __name__ == "__main__":
    raise SystemExit(run_status())


"""
INSTRUCTIONS
1. Save this file as:
   ztd/status.py

2. Test it with:
   cd /home/pc-10/repos/ZeroTrustDesktop-V2 && ./.venv/bin/python -m ztd.status
"""
