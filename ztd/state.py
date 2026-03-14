#!/usr/bin/env python3
"""
README HEADER
ZeroTrustDesktop-V2 - State and diff foundation

Purpose:
- Provide a read-only baseline state snapshot for the local repo/runtime.
- Compare current state against the latest saved state.
- Write deterministic state and diff artifacts for future preview workflows.

Behavior:
- Captures a compact structured state.
- Saves state JSON into output/state.
- Compares current state to latest prior state JSON.
- Saves diff JSON into output/diffs.
- Does not change system security/runtime state.

Author:
- SABLE + Elliot
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from ztd.paths import get_paths


@dataclass
class RuntimeState:
    timestamp_utc: str
    repo_root: str
    git_branch: str
    git_commit: str
    python_executable: str
    python_version: str
    latest_snapshot: str
    latest_report: str


def _utc_now_stamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")


def _utc_now_iso() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _read_text_safe(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").strip()
    except Exception:
        return "unknown"


def _latest_file(directory: Path, pattern: str) -> Path | None:
    matches = sorted(
        [p for p in directory.glob(pattern) if p.is_file() and p.name != ".gitkeep"],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return matches[0] if matches else None


def collect_runtime_state() -> RuntimeState:
    import subprocess
    import sys

    paths = get_paths()

    def run_git(args: list[str]) -> str:
        try:
            result = subprocess.run(
                ["git", *args],
                cwd=paths.repo_root,
                capture_output=True,
                text=True,
                check=False,
                timeout=10,
            )
            text = (result.stdout or result.stderr).strip()
            return text if text else "unknown"
        except Exception:
            return "unknown"

    latest_snapshot = _latest_file(paths.snapshots_dir, "doctor_*.json")
    latest_report = _latest_file(paths.reports_dir, "doctor_*.md")

    return RuntimeState(
        timestamp_utc=_utc_now_iso(),
        repo_root=str(paths.repo_root),
        git_branch=run_git(["rev-parse", "--abbrev-ref", "HEAD"]),
        git_commit=run_git(["rev-parse", "--short", "HEAD"]),
        python_executable=sys.executable,
        python_version=".".join(map(str, sys.version_info[:3])),
        latest_snapshot=str(latest_snapshot) if latest_snapshot else "none",
        latest_report=str(latest_report) if latest_report else "none",
    )


def _state_file_path(stamp: str) -> Path:
    paths = get_paths()
    paths.state_dir.mkdir(parents=True, exist_ok=True)
    return paths.state_dir / f"state_{stamp}.json"


def _diff_file_path(stamp: str) -> Path:
    paths = get_paths()
    paths.diffs_dir.mkdir(parents=True, exist_ok=True)
    return paths.diffs_dir / f"state_diff_{stamp}.json"


def _latest_state_file() -> Path | None:
    paths = get_paths()
    return _latest_file(paths.state_dir, "state_*.json")


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(state: RuntimeState) -> Path:
    stamp = _utc_now_stamp()
    target = _state_file_path(stamp)
    target.write_text(json.dumps(asdict(state), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return target


def diff_states(previous: dict[str, Any] | None, current: dict[str, Any]) -> dict[str, Any]:
    if previous is None:
        return {
            "status": "initial_state",
            "changed_keys": sorted(current.keys()),
            "previous_timestamp_utc": "none",
            "current_timestamp_utc": current.get("timestamp_utc", "unknown"),
        }

    changed = []
    for key in sorted(set(previous.keys()) | set(current.keys())):
        if previous.get(key) != current.get(key):
            changed.append(
                {
                    "key": key,
                    "previous": previous.get(key, "missing"),
                    "current": current.get(key, "missing"),
                }
            )

    return {
        "status": "changed" if changed else "unchanged",
        "changed_count": len(changed),
        "changed": changed,
        "previous_timestamp_utc": previous.get("timestamp_utc", "unknown"),
        "current_timestamp_utc": current.get("timestamp_utc", "unknown"),
    }


def save_diff(diff_payload: dict[str, Any]) -> Path:
    stamp = _utc_now_stamp()
    target = _diff_file_path(stamp)
    target.write_text(json.dumps(diff_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return target


def run_state_capture() -> int:
    latest_before = _latest_state_file()
    previous = _load_json(latest_before) if latest_before else None

    state = collect_runtime_state()
    current_payload = asdict(state)

    state_file = save_state(state)
    diff_payload = diff_states(previous, current_payload)
    diff_file = save_diff(diff_payload)

    print(f"[state] state_file={state_file}")
    print(f"[state] diff_file={diff_file}")
    print(f"[state] diff_status={diff_payload['status']}")
    if "changed_count" in diff_payload:
        print(f"[state] changed_count={diff_payload['changed_count']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(run_state_capture())
