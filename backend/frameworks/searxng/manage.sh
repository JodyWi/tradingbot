#!/usr/bin/env bash
set -Eeuo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$DIR/../../.." && pwd)"
SRC="$DIR/src"
SETTINGS="$DIR/settings.yml"
PID_FILE="$ROOT_DIR/logs/searxng.pid"
LOG_FILE="$ROOT_DIR/logs/searxng.log"
PORT="${AUTOLUNO_SEARXNG_PORT:-8080}"
URL="${AUTOLUNO_SEARXNG_LOCAL_URL:-http://127.0.0.1:${PORT}/}"
AUTO_UPDATE="${SEARXNG_AUTO_UPDATE:-false}"

running() {
  [ -f "$PID_FILE" ] || return 1
  local pid
  pid="$(cat "$PID_FILE" 2>/dev/null || true)"
  [ -n "$pid" ] && kill -0 "$pid" >/dev/null 2>&1
}

stop_service() {
  if running; then
    local pid
    pid="$(cat "$PID_FILE")"
    kill "$pid" >/dev/null 2>&1 || true
    for _ in $(seq 1 20); do
      kill -0 "$pid" >/dev/null 2>&1 || break
      sleep 0.25
    done
    kill -0 "$pid" >/dev/null 2>&1 && kill -9 "$pid" >/dev/null 2>&1 || true
  fi
  rm -f "$PID_FILE"
}

case "${1:-status}" in
  setup)
    if [ ! -d "$SRC/.git" ]; then
      rm -rf "$SRC"
      git clone --depth 1 https://github.com/searxng/searxng.git "$SRC"
    elif [ "${AUTO_UPDATE,,}" = "true" ]; then
      git -C "$SRC" pull --ff-only
    fi
    (cd "$SRC" && make install)
    ;;
  start)
    if curl --silent --fail --max-time 3 "$URL" >/dev/null 2>&1; then
      exit 0
    fi
    stop_service
    [ -x "$SRC/local/py3/bin/python" ] || {
      echo "SearXNG is not installed. Run: $0 setup" >&2
      exit 1
    }
    mkdir -p "$(dirname "$PID_FILE")" "$(dirname "$LOG_FILE")"
    (
      cd "$SRC"
      exec env \
        PYTHONUNBUFFERED=1 \
        SEARXNG_SETTINGS_PATH="$SETTINGS" \
        SEARXNG_BIND_ADDRESS="127.0.0.1" \
        SEARXNG_PORT="$PORT" \
        SEARXNG_BASE_URL="$URL" \
        "$SRC/local/py3/bin/python" -m searx.webapp
    ) >> "$LOG_FILE" 2>&1 &
    printf '%s\n' "$!" > "$PID_FILE"
    ;;
  stop)
    stop_service
    ;;
  health)
    curl --silent --fail --max-time 3 "$URL" >/dev/null
    ;;
  logs)
    touch "$LOG_FILE"
    exec tail -n 100 -F "$LOG_FILE"
    ;;
  status)
    if curl --silent --fail --max-time 3 "$URL" >/dev/null 2>&1; then
      echo "running"
      exit 0
    fi
    echo "stopped"
    exit 1
    ;;
  *)
    echo "Usage: $0 {setup|start|stop|health|logs|status}" >&2
    exit 2
    ;;
esac
