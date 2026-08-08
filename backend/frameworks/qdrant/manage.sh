#!/usr/bin/env bash
set -Eeuo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$DIR/../../.." && pwd)"
BIN="$DIR/bin/qdrant"
STORAGE="$DIR/storage"
CONFIG="$DIR/config.yaml"
PID_FILE="$ROOT_DIR/logs/qdrant.pid"
LOG_FILE="$ROOT_DIR/logs/qdrant.log"
PORT="${AUTOLUNO_QDRANT_PORT:-6333}"
GRPC_PORT="${AUTOLUNO_QDRANT_GRPC_PORT:-$((PORT + 1))}"
URL="${QDRANT_URL:-http://127.0.0.1:${PORT}}"
AUTO_UPDATE="${QDRANT_AUTO_UPDATE:-false}"

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

download_binary() (
  local machine target meta archive temp_dir asset_url extracted
  machine="$(uname -m)"
  case "$machine" in
    x86_64|amd64) target="x86_64" ;;
    aarch64|arm64) target="aarch64" ;;
    *) echo "Unsupported Qdrant architecture: $machine" >&2; exit 1 ;;
  esac

  meta="$(mktemp)"
  archive="$(mktemp --suffix=.tar.gz)"
  temp_dir="$(mktemp -d)"
  trap 'rm -f "$meta" "$archive"; rm -rf "$temp_dir"' EXIT

  curl -fsSL https://api.github.com/repos/qdrant/qdrant/releases/latest -o "$meta"
  asset_url="$(python3 - "$meta" "$target" <<'PY'
import json
import sys

path, arch = sys.argv[1:]
with open(path, encoding="utf-8") as handle:
    release = json.load(handle)
assets = release.get("assets", [])
preferred = [
    f"qdrant-{arch}-unknown-linux-musl.tar.gz",
    f"qdrant-{arch}-unknown-linux-gnu.tar.gz",
]
for name in preferred:
    for asset in assets:
        if asset.get("name") == name:
            print(asset["browser_download_url"])
            raise SystemExit
for asset in assets:
    name = asset.get("name", "")
    if name.startswith(f"qdrant-{arch}-") and name.endswith(".tar.gz"):
        print(asset["browser_download_url"])
        raise SystemExit
raise SystemExit(f"No Linux Qdrant binary asset found for {arch}")
PY
)"

  curl -fL "$asset_url" -o "$archive"
  tar -xzf "$archive" -C "$temp_dir"
  extracted="$(find "$temp_dir" -type f -name qdrant | head -n 1)"
  [ -n "$extracted" ] || { echo "Downloaded Qdrant archive did not contain a qdrant binary." >&2; exit 1; }
  install -m 0755 "$extracted" "$BIN"
)

write_config() {
  mkdir -p "$STORAGE"
  cat > "$CONFIG" <<EOF_CONFIG
storage:
  storage_path: "$STORAGE"

service:
  host: "127.0.0.1"
  http_port: $PORT
  grpc_port: $GRPC_PORT

telemetry_disabled: true
EOF_CONFIG
}

case "${1:-status}" in
  setup)
    if [ ! -x "$BIN" ] || [ "${AUTO_UPDATE,,}" = "true" ]; then
      download_binary
    fi
    write_config
    ;;
  start)
    if curl --silent --fail --max-time 3 "${URL%/}/" >/dev/null 2>&1; then
      exit 0
    fi
    stop_service
    [ -x "$BIN" ] || { echo "Qdrant is not installed. Run: $0 setup" >&2; exit 1; }
    write_config
    mkdir -p "$(dirname "$PID_FILE")" "$(dirname "$LOG_FILE")"
    (
      cd "$DIR"
      exec "$BIN" --config-path "$CONFIG"
    ) >> "$LOG_FILE" 2>&1 &
    printf '%s\n' "$!" > "$PID_FILE"
    ;;
  stop)
    stop_service
    ;;
  health)
    curl --silent --fail --max-time 3 "${URL%/}/" >/dev/null
    ;;
  logs)
    touch "$LOG_FILE"
    exec tail -n 100 -F "$LOG_FILE"
    ;;
  status)
    if curl --silent --fail --max-time 3 "${URL%/}/" >/dev/null 2>&1; then
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
