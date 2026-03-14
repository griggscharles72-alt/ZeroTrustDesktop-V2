#!/usr/bin/env bash
set -u
set -o pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$REPO_DIR/.venv"

if [ ! -d "$VENV_DIR" ]; then
  echo "No venv found. Running bootstrap first..."
  "$REPO_DIR/bootstrap.sh" || exit 1
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

if [ "${1:-}" = "" ]; then
  echo
  echo "ZeroTrustDesktop-V2"
  echo "1) Doctor"
  echo "2) Audit"
  echo "3) Status"
  echo "4) Observe"
  echo "5) Apply"
  echo "6) Restore"
  echo "7) Exit"
  echo
  read -r -p "Select: " CHOICE
  case "$CHOICE" in
    1) set -- doctor ;;
    2) set -- audit ;;
    3) set -- status ;;
    4) set -- observe ;;
    5) set -- apply ;;
    6) set -- restore ;;
    *) exit 0 ;;
  esac
fi

python3 -m ztd "$@"
