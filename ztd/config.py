#!/usr/bin/env python3
"""
README HEADER
ZeroTrustDesktop-V2 - Config loader

Purpose:
- Load tracked defaults and optional local overrides.
- Provide one normalized config object to the rest of V2.
- Keep behavior deterministic and repo-root anchored.

Behavior:
- Reads config/ztd.default.yaml if present.
- Reads config/ztd.local.yaml if present.
- Deep-merges local values over defaults.
- Falls back safely if PyYAML is not installed.

Author:
- SABLE + Elliot
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from ztd.paths import get_paths

try:
    import yaml  # type: ignore
except Exception:
    yaml = None


DEFAULT_CONFIG: dict[str, Any] = {
    "project": {
        "name": "ZeroTrustDesktop-V2",
        "mode": "read_only",
        "output_root": "output",
        "log_level": "INFO",
    },
    "runtime": {
        "reports_dir": "output/reports",
        "snapshots_dir": "output/snapshots",
        "diffs_dir": "output/diffs",
        "logs_dir": "output/logs",
        "state_dir": "output/state",
    },
    "launcher": {
        "default_command": "status",
        "show_menu": True,
    },
    "safety": {
        "allow_apply": False,
        "allow_restore": False,
        "require_explicit_flags": True,
    },
    "network": {
        "wifi_interface": "wlan0",
        "vpn_expected": False,
        "vpn_interface": "tun0",
    },
    "firewall": {
        "backend": "ufw",
        "expected_enabled": True,
    },
    "observability": {
        "write_markdown_report": True,
        "write_json_snapshot": True,
        "collect_processes": True,
        "collect_network": True,
        "collect_firewall": True,
        "collect_system": True,
    },
    "doctor": {
        "check_python": True,
        "check_vscode": True,
        "check_git": True,
        "check_firewall": True,
        "check_apparmor": True,
        "check_fail2ban": True,
    },
}


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def _load_yaml_file(path: Path) -> dict[str, Any]:
    if not path.exists() or path.stat().st_size == 0:
        return {}

    if yaml is None:
        return {}

    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    if not isinstance(data, dict):
        raise ValueError(f"Config file must contain a dictionary at top level: {path}")

    return data


def load_config() -> dict[str, Any]:
    paths = get_paths()

    config = deepcopy(DEFAULT_CONFIG)
    default_file_data = _load_yaml_file(paths.default_config_file)
    local_file_data = _load_yaml_file(paths.local_config_file)

    if default_file_data:
        config = _deep_merge(config, default_file_data)

    if local_file_data:
        config = _deep_merge(config, local_file_data)

    return config


if __name__ == "__main__":
    cfg = load_config()
    print(f"project.name={cfg['project']['name']}")
    print(f"project.mode={cfg['project']['mode']}")
    print(f"launcher.default_command={cfg['launcher']['default_command']}")
    print(f"firewall.backend={cfg['firewall']['backend']}")
    print(f"safety.allow_apply={cfg['safety']['allow_apply']}")
    print(f"doctor.check_python={cfg['doctor']['check_python']}")


"""
INSTRUCTIONS
1. Save this file as:
   ztd/config.py

2. Test it with:
   cd /home/pc-10/repos/ZeroTrustDesktop-V2 && ./.venv/bin/python -m ztd.config
"""
