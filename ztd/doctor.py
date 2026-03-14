#!/usr/bin/env python3
"""
README HEADER
ZeroTrustDesktop-V2 - Doctor checks

Purpose:
- Provide a read-only baseline diagnostic for the local machine.
- Check core tools and services relevant to ZeroTrustDesktop-V2.
- Return structured results for later report generation.

Behavior:
- Collects simple presence and status checks.
- Does not change system state.
- Writes both JSON snapshot and markdown summary outputs.

Author:
- SABLE + Elliot
"""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import asdict, dataclass
from typing import Any

from ztd.config import load_config
from ztd.paths import get_paths
from ztd.report import write_json_snapshot, write_markdown_report


@dataclass
class CheckResult:
    name: str
    ok: bool
    detail: str


def _command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def _run_command(command: list[str]) -> tuple[bool, str]:
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        output = (completed.stdout or completed.stderr).strip()
        return completed.returncode == 0, output
    except Exception as exc:
        return False, str(exc)


def collect_doctor_results() -> list[CheckResult]:
    cfg = load_config()
    results: list[CheckResult] = []

    doctor_cfg = cfg.get("doctor", {})

    if doctor_cfg.get("check_python", True):
        results.append(
            CheckResult(
                name="python3",
                ok=_command_exists("python3"),
                detail=shutil.which("python3") or "python3 not found",
            )
        )

    if doctor_cfg.get("check_git", True):
        results.append(
            CheckResult(
                name="git",
                ok=_command_exists("git"),
                detail=shutil.which("git") or "git not found",
            )
        )

    if doctor_cfg.get("check_vscode", True):
        results.append(
            CheckResult(
                name="vscode",
                ok=_command_exists("code"),
                detail=shutil.which("code") or "code not found",
            )
        )

    if doctor_cfg.get("check_firewall", True):
        ok, detail = _run_command(
            ["bash", "-lc", "if command -v ufw >/dev/null 2>&1; then ufw status; else echo ufw not found; exit 1; fi"]
        )
        results.append(
            CheckResult(
                name="firewall_ufw",
                ok=ok,
                detail=detail or "ufw status unavailable",
            )
        )

    if doctor_cfg.get("check_apparmor", True):
        ok, detail = _run_command(
            ["bash", "-lc", "if command -v aa-status >/dev/null 2>&1; then aa-status; else echo aa-status not found; exit 1; fi"]
        )
        normalized_ok = ok or "apparmor module is loaded" in detail.lower()
        results.append(
            CheckResult(
                name="apparmor",
                ok=normalized_ok,
                detail=detail or "aa-status unavailable",
            )
        )

    if doctor_cfg.get("check_fail2ban", True):
        ok, detail = _run_command(
            ["bash", "-lc", "if command -v fail2ban-client >/dev/null 2>&1; then fail2ban-client ping; else echo fail2ban-client not found; exit 1; fi"]
        )
        results.append(
            CheckResult(
                name="fail2ban",
                ok=ok,
                detail=detail or "fail2ban-client unavailable",
            )
        )

    return results


def build_doctor_payload(results: list[CheckResult]) -> dict[str, Any]:
    paths = get_paths()
    return {
        "repo_root": str(paths.repo_root),
        "results": [asdict(item) for item in results],
    }


def build_doctor_markdown_lines(results: list[CheckResult]) -> list[str]:
    lines = ["## Doctor Results", ""]
    for item in results:
        state = "OK" if item.ok else "WARN"
        lines.append(f"- **{item.name}**: {state}")
        lines.append(f"  - detail: {item.detail}")
    return lines


def run_doctor() -> int:
    paths = get_paths()
    results = collect_doctor_results()

    json_file = write_json_snapshot("doctor", build_doctor_payload(results))
    markdown_file = write_markdown_report(
        "ZeroTrustDesktop-V2 Doctor Report",
        "doctor",
        build_doctor_markdown_lines(results),
    )

    print(f"[doctor] repo={paths.repo_root}")
    print(f"[doctor] snapshot={json_file}")
    print(f"[doctor] report={markdown_file}")

    for item in results:
        state = "OK" if item.ok else "WARN"
        print(f"[doctor] {state} {item.name}: {item.detail}")

    return 0


if __name__ == "__main__":
    raise SystemExit(run_doctor())


"""
INSTRUCTIONS
1. Save this file as:
   ztd/doctor.py

2. Test it with:
   cd /home/pc-10/repos/ZeroTrustDesktop-V2 && ./.venv/bin/python -m ztd.doctor

3. Expected behavior:
   - prints doctor checks
   - writes JSON snapshot into output/snapshots/
   - writes markdown report into output/reports/
"""
