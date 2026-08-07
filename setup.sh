#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE="${1:---install}"
case "$MODE" in --install|--check) ;; --help|-h) printf 'Usage: %s [--install|--check]\n' "$0"; exit 0 ;; *) exit 2 ;; esac

missing=0
for command_name in python3; do
  if command -v "$command_name" >/dev/null 2>&1; then
    printf '[ok] %s found\n' "$command_name"
  else
    printf '[missing] %s must be installed explicitly\n' "$command_name" >&2
    missing=1
  fi
done
if command -v node >/dev/null 2>&1 && command -v npm >/dev/null 2>&1; then frontend_runtime=1; printf '[ok] Node.js and npm found\n'; else frontend_runtime=0; printf '[skipped] frontend install: native Node.js/npm unavailable\n'; fi
[ "$MODE" = "--check" ] || [ "$missing" -eq 0 ] || {
  printf 'No system packages were installed. Resolve prerequisites and rerun.\n' >&2; exit 1;
}

if [ "$MODE" = "--install" ]; then
  [ -f "$ROOT_DIR/.env" ] || cp "$ROOT_DIR/.env.example" "$ROOT_DIR/.env"
  if [ ! -x "$ROOT_DIR/.venv/bin/python" ]; then
    python3 -m venv "$ROOT_DIR/.venv" || {
      printf 'Install Python venv support explicitly; no system change was attempted.\n' >&2; exit 1;
    }
  fi
  "$ROOT_DIR/.venv/bin/python" -m pip install -r "$ROOT_DIR/requirements.txt"
  [ "$frontend_runtime" -eq 0 ] || npm --prefix "$ROOT_DIR/frontend" ci
fi

printf '\nExternal service detection (never installed or started here):\n'
if command -v mongod >/dev/null 2>&1; then printf '[installed] mongod\n'; else printf '[not detected] mongod\n'; fi
if command -v mongosh >/dev/null 2>&1; then printf '[installed] mongosh\n'; else printf '[not detected] mongosh\n'; fi
if pgrep -x mongod >/dev/null 2>&1; then printf '[active] mongod process\n'; else printf '[inactive] mongod process\n'; fi
config_file="$ROOT_DIR/.env"; [ -f "$config_file" ] || config_file="$ROOT_DIR/.env.example"
mongo_uri="$(sed -n 's/^MONGO_URI=//p' "$config_file" | tail -1)"; mongo_uri="${mongo_uri:-mongodb://127.0.0.1:27017}"
if "$ROOT_DIR/.venv/bin/python" - "$mongo_uri" <<'PY'
import sys
from pymongo import MongoClient
MongoClient(sys.argv[1], serverSelectionTimeoutMS=1500).admin.command('ping')
PY
then
  printf '[ready] required MongoDB accepted a ping\n'
else
  printf '[not ready] required MongoDB did not accept a ping at the configured endpoint\n'
fi
for item in 'Qdrant|http://127.0.0.1:6333/healthz' 'SearXNG|http://127.0.0.1:8080/' 'Ollama|http://127.0.0.1:11434/api/tags'; do
  name="${item%%|*}"; url="${item#*|}"
  if curl --silent --fail --max-time 2 "$url" >/dev/null 2>&1; then
    printf '[available] %s\n' "$name"
  else
    printf '[start separately] %s\n' "$name"
  fi
done
printf 'No system packages, services, provider binaries, or AI models were installed or started.\n'
