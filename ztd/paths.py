#!/usr/bin/env python3
"""
README HEADER
ZeroTrustDesktop-V2 - Repo-safe path handling

Purpose:
- Centralize all filesystem path logic for the project.
- Keep execution location-independent.
- Ensure output and config directories are created safely.

Behavior:
- Anchors all important paths from the repo root.
- Exposes helper methods for active config, output dirs, and legacy dirs.
- Creates runtime directories on demand.

Author:
- Elliot + ChatGPT
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ZTDPaths:
    repo_root: Path
    config_dir: Path
    firewall_config_dir: Path
    output_dir: Path
    reports_dir: Path
    snapshots_dir: Path
    diffs_dir: Path
    logs_dir: Path
    state_dir: Path
    legacy_dir: Path
    tests_dir: Path

    @classmethod
    def discover(cls) -> "ZTDPaths":
        repo_root = Path(__file__).resolve().parent.parent
        config_dir = repo_root / "config"
        firewall_config_dir = config_dir / "firewall"
        output_dir = repo_root / "output"

        return cls(
            repo_root=repo_root,
            config_dir=config_dir,
            firewall_config_dir=firewall_config_dir,
            output_dir=output_dir,
            reports_dir=output_dir / "reports",
            snapshots_dir=output_dir / "snapshots",
            diffs_dir=output_dir / "diffs",
            logs_dir=output_dir / "logs",
            state_dir=output_dir / "state",
            legacy_dir=repo_root / "legacy",
            tests_dir=repo_root / "tests",
        )

    @property
    def default_config_file(self) -> Path:
        return self.config_dir / "ztd.default.yaml"

    @property
    def local_config_file(self) -> Path:
        return self.config_dir / "ztd.local.yaml"

    def ensure_runtime_dirs(self) -> None:
        for path in (
            self.output_dir,
            self.reports_dir,
            self.snapshots_dir,
            self.diffs_dir,
            self.logs_dir,
            self.state_dir,
        ):
            path.mkdir(parents=True, exist_ok=True)


def get_paths() -> ZTDPaths:
    paths = ZTDPaths.discover()
    paths.ensure_runtime_dirs()
    return paths


if __name__ == "__main__":
    p = get_paths()
    print(f"repo_root={p.repo_root}")
    print(f"config_dir={p.config_dir}")
    print(f"output_dir={p.output_dir}")
    print(f"reports_dir={p.reports_dir}")
    print(f"snapshots_dir={p.snapshots_dir}")
    print(f"diffs_dir={p.diffs_dir}")
    print(f"logs_dir={p.logs_dir}")
    print(f"state_dir={p.state_dir}")


"""
INSTRUCTIONS
1. Save this file as:
   ztd/paths.py

2. Test it with:
   cd /home/pc-10/repos/ZeroTrustDesktop-V2 && python3 ztd/paths.py

3. Or test through the venv with:
   cd /home/pc-10/repos/ZeroTrustDesktop-V2 && ./.venv/bin/python ztd/paths.py
"""
