#!/usr/bin/env bash
set -u
set -o pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$REPO_DIR/.venv"
TITLE="ZeroTrustDesktop-V2"

ensure_bootstrap() {
  if [ ! -d "$VENV_DIR" ]; then
    printf '[launch] No virtual environment found. Running bootstrap...\n'
    "$REPO_DIR/bootstrap.sh" || {
      printf '[launch] Bootstrap failed.\n' >&2
      exit 1
    }
  fi
}

run_cli() {
  # shellcheck disable=SC1091
  source "$VENV_DIR/bin/activate"
  python3 -m ztd "$@"
}

show_menu() {
  printf '\n%s\n' "$TITLE"
  printf '1) Doctor\n'
  printf '2) Audit\n'
  printf '3) Status\n'
  printf '4) Observe\n'
  printf '5) Apply\n'
  printf '6) Restore\n'
  printf '7) Exit\n\n'
}

ensure_bootstrap

if [ "${1:-}" = "" ]; then
  show_menu
  read -r -p "Select: " CHOICE
  case "$CHOICE" in
    1) set -- doctor ;;
    2) set -- audit ;;
    3) set -- status ;;
    4) set -- observe ;;
    5) set -- apply ;;
    6) set -- restore ;;
    7) exit 0 ;;
    "") set -- status ;;
    *) printf '[launch] Invalid selection: %s\n' "$CHOICE" >&2; exit 1 ;;
  esac
fi

run_cli "$@"
