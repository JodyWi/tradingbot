#!/usr/bin/env bash
set -Eeuo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$DIR/../../.." && pwd)"
LOCAL_BIN="$DIR/bin/ollama"
MODEL_DIR="$DIR/models"
HOME_DIR="$DIR/home"
PID_FILE="$ROOT_DIR/logs/ollama.pid"
LOG_FILE="$ROOT_DIR/logs/ollama.log"
PORT="${AUTOLUNO_OLLAMA_PORT:-11434}"
URL="${OLLAMA_URL:-http://127.0.0.1:${PORT}}"
AUTO_UPDATE="${OLLAMA_AUTO_UPDATE:-false}"

ollama_bin() {
  if [ -x "$LOCAL_BIN" ]; then
    printf '%s\n' "$LOCAL_BIN"
  elif command -v ollama >/dev/null 2>&1; then
    command -v ollama
  else
    return 1
  fi
}

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

download_local_bundle() (
  local machine arch archive temp_dir found_bin
  machine="$(uname -m)"
  case "$machine" in
    x86_64|amd64) arch="amd64" ;;
    aarch64|arm64) arch="arm64" ;;
    *) echo "Unsupported Ollama architecture: $machine" >&2; exit 1 ;;
  esac

  archive="$(mktemp --suffix=.tar.zst)"
  temp_dir="$(mktemp -d)"
  trap 'rm -f "$archive"; rm -rf "$temp_dir"' EXIT

  curl -fL "https://ollama.com/download/ollama-linux-${arch}.tar.zst" -o "$archive"
  zstd -dc "$archive" | tar -xf - -C "$temp_dir"

  found_bin="$(find "$temp_dir" -type f -path '*/bin/ollama' | head -n 1)"
  [ -n "$found_bin" ] || { echo "Downloaded Ollama bundle did not contain bin/ollama." >&2; exit 1; }

  rm -rf "$DIR/bin" "$DIR/lib"
  mkdir -p "$DIR/bin" "$DIR/lib"
  cp -a "$(dirname "$found_bin")/." "$DIR/bin/"
  if [ -d "$temp_dir/lib" ]; then
    cp -a "$temp_dir/lib/." "$DIR/lib/"
  fi
  chmod +x "$LOCAL_BIN"
)

case "${1:-status}" in
  setup)
    if ! ollama_bin >/dev/null 2>&1 || [ "${AUTO_UPDATE,,}" = "true" ]; then
      download_local_bundle
    fi
    ;;
  start)
    if curl --silent --fail --max-time 3 "${URL%/}/api/tags" >/dev/null 2>&1; then
      exit 0
    fi
    stop_service
    BIN="$(ollama_bin)" || { echo "Ollama is not installed. Run: $0 setup" >&2; exit 1; }
    mkdir -p "$MODEL_DIR" "$HOME_DIR" "$(dirname "$PID_FILE")" "$(dirname "$LOG_FILE")"
    (
      cd "$DIR"
      exec env \
        HOME="$HOME_DIR" \
        OLLAMA_HOST="127.0.0.1:$PORT" \
        OLLAMA_MODELS="$MODEL_DIR" \
        OLLAMA_KEEP_ALIVE="${OLLAMA_KEEP_ALIVE:-5m}" \
        LD_LIBRARY_PATH="$DIR/lib/ollama:${LD_LIBRARY_PATH:-}" \
        PATH="$DIR/bin:$PATH" \
        "$BIN" serve
    ) >> "$LOG_FILE" 2>&1 &
    printf '%s\n' "$!" > "$PID_FILE"
    ;;
  stop)
    stop_service
    ;;
  pull)
    shift
    BIN="$(ollama_bin)" || { echo "Ollama is not installed." >&2; exit 1; }
    [ "$#" -gt 0 ] || { echo "Usage: $0 pull MODEL [MODEL ...]" >&2; exit 2; }
    for model in "$@"; do
      env \
        HOME="$HOME_DIR" \
        OLLAMA_HOST="127.0.0.1:$PORT" \
        OLLAMA_MODELS="$MODEL_DIR" \
        LD_LIBRARY_PATH="$DIR/lib/ollama:${LD_LIBRARY_PATH:-}" \
        PATH="$DIR/bin:$PATH" \
        "$BIN" pull "$model"
    done
    ;;
  list)
    BIN="$(ollama_bin)" || { echo "Ollama is not installed." >&2; exit 1; }
    env HOME="$HOME_DIR" OLLAMA_HOST="127.0.0.1:$PORT" OLLAMA_MODELS="$MODEL_DIR" \
      LD_LIBRARY_PATH="$DIR/lib/ollama:${LD_LIBRARY_PATH:-}" PATH="$DIR/bin:$PATH" "$BIN" list
    ;;
  health)
    curl --silent --fail --max-time 3 "${URL%/}/api/tags" >/dev/null
    ;;
  logs)
    touch "$LOG_FILE"
    exec tail -n 100 -F "$LOG_FILE"
    ;;
  status)
    if curl --silent --fail --max-time 3 "${URL%/}/api/tags" >/dev/null 2>&1; then
      echo "running"
      exit 0
    fi
    echo "stopped"
    exit 1
    ;;
  *)
    echo "Usage: $0 {setup|start|stop|pull|list|health|logs|status}" >&2
    exit 2
    ;;
esac
