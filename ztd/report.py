#!/usr/bin/env python3
"""
README HEADER
ZeroTrustDesktop-V2 - Report writers

Purpose:
- Centralize report writing for V2 modules.
- Support both JSON snapshots and markdown reports.
- Keep report output deterministic and anchored to repo paths.

Behavior:
- Writes timestamped JSON snapshot files.
- Writes timestamped markdown summary reports.
- Uses output directories from repo-safe path discovery.

Author:
- SABLE + Elliot
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from ztd.paths import get_paths


def utc_timestamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")


def write_json_snapshot(prefix: str, payload: dict[str, Any]) -> Path:
    paths = get_paths()
    stamp = utc_timestamp()
    out = paths.snapshots_dir / f"{prefix}_{stamp}.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return out


def write_markdown_report(title: str, prefix: str, lines: list[str]) -> Path:
    paths = get_paths()
    stamp = utc_timestamp()
    out = paths.reports_dir / f"{prefix}_{stamp}.md"

    body = [f"# {title}", "", f"Generated (UTC): {stamp}", ""]
    body.extend(lines)
    body.append("")

    out.write_text("\n".join(body), encoding="utf-8")
    return out


if __name__ == "__main__":
    example_json = write_json_snapshot(
        "report_test",
        {"status": "ok", "module": "report"},
    )
    example_md = write_markdown_report(
        "Report Test",
        "report_test",
        ["- status: ok", "- module: report"],
    )
    print(f"json={example_json}")
    print(f"markdown={example_md}")


"""
INSTRUCTIONS
1. Save this file as:
   ztd/report.py

2. Test it with:
   cd /home/pc-10/repos/ZeroTrustDesktop-V2 && ./.venv/bin/python -m ztd.report
"""
