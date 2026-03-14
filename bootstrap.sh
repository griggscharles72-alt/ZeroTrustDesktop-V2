#!/usr/bin/env bash
set -u
set -o pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$REPO_DIR/.venv"

mkdir -p \
  "$REPO_DIR/output/reports" \
  "$REPO_DIR/output/snapshots" \
  "$REPO_DIR/output/diffs" \
  "$REPO_DIR/output/logs" \
  "$REPO_DIR/config"

if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

python -m pip install --upgrade pip >/dev/null 2>&1 || true

if [ -f "$REPO_DIR/requirements.txt" ]; then
  python -m pip install -r "$REPO_DIR/requirements.txt" >/dev/null 2>&1 || true
fi

if [ ! -f "$REPO_DIR/config/ztd.local.yaml" ]; then
  cp "$REPO_DIR/config/ztd.default.yaml" "$REPO_DIR/config/ztd.local.yaml" 2>/dev/null || true
fi

chmod +x "$REPO_DIR/launch.sh" "$REPO_DIR/scripts/ztd" 2>/dev/null || true

printf '\nBootstrap complete.\n'
printf 'Run next:\n  cd %s && ./launch.sh\n' "$REPO_DIR"
