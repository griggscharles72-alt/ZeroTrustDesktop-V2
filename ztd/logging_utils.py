#!/usr/bin/env python3
"""
README HEADER
ZeroTrustDesktop-V2 - Logging utilities

Purpose:
- Centralize logging setup for V2 modules.
- Provide consistent console and file logging.
- Keep logging deterministic and repo-anchored.

Behavior:
- Builds a named logger with deterministic formatting.
- Avoids duplicate handlers on repeated imports.
- Defaults to config-safe INFO style output.
- Writes logs to output/logs/ztd.log in addition to console.

Author:
- SABLE + Elliot
"""

from __future__ import annotations

import logging
from pathlib import Path

from ztd.config import load_config
from ztd.paths import get_paths


def get_log_file_path(filename: str = "ztd.log") -> Path:
    paths = get_paths()
    paths.logs_dir.mkdir(parents=True, exist_ok=True)
    return paths.logs_dir / filename


def get_logger(name: str) -> logging.Logger:
    cfg = load_config()
    level_name = str(cfg.get("project", {}).get("log_level", "INFO")).upper()
    level = getattr(logging, level_name, logging.INFO)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    if logger.handlers:
        return logger

    formatter = logging.Formatter("[%(name)s] %(levelname)s %(message)s")

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    file_handler = logging.FileHandler(get_log_file_path(), encoding="utf-8")
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


if __name__ == "__main__":
    logger = get_logger("ztd.logging")
    logger.info("logging utils ready")
    print(f"log_file={get_log_file_path()}")
