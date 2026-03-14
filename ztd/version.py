#!/usr/bin/env python3
"""
README HEADER
ZeroTrustDesktop-V2 - Version identity

Purpose:
- Provide a single source of truth for project identity and version.
- Keep launcher, CLI, and docs aligned to the same version string.

Author:
- SABLE + Elliot
"""

from __future__ import annotations

PROJECT_NAME = "ZeroTrustDesktop-V2"
VERSION = "0.1.0"
PHASE = "read-only baseline"

FULL_VERSION = f"{PROJECT_NAME} {VERSION} ({PHASE})"


def get_version() -> str:
    return FULL_VERSION


if __name__ == "__main__":
    print(get_version())
