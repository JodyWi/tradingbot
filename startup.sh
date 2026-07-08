#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$ROOT_DIR/logs"
ACTION="${1:-start}"

PYTHON_PORT="${AUTOLUNO_PYTHON_PORT:-8001}"
FRONTEND_PORT="${AUTOLUNO_FRONTEND_PORT:-3001}"
START_NODE="${AUTOLUNO_START_NODE:-0}"
NODE_PORT="${AUTOLUNO_NODE_PORT:-3002}"
FORCE_PORT_CLEAR="${AUTOLUNO_FORCE_PORT_CLEAR:-0}"
AUTO_INSTALL_SYSTEM="${AUTOLUNO_AUTO_INSTALL_SYSTEM:-1}"
PYTHON_READY_URL="${AUTOLUNO_PYTHON_READY_URL:-http://127.0.0.1:${PYTHON_PORT}/api/health}"
FRONTEND_READY_URL="${AUTOLUNO_FRONTEND_READY_URL:-http://127.0.0.1:${FRONTEND_PORT}/}"
PYTHON_READY_ATTEMPTS="${AUTOLUNO_PYTHON_READY_ATTEMPTS:-90}"
FRONTEND_READY_ATTEMPTS="${AUTOLUNO_FRONTEND_READY_ATTEMPTS:-60}"
NODE_READY_ATTEMPTS="${AUTOLUNO_NODE_READY_ATTEMPTS:-45}"

AUTOPOLY_PORTS="8000 5173"
AUTOLUNO_PORTS="$PYTHON_PORT $FRONTEND_PORT"
if [ "$START_NODE" = "1" ]; then
  AUTOLUNO_PORTS="$AUTOLUNO_PORTS $NODE_PORT"
fi

# All research/AI services run directly on the host. No Docker is used.
SEARXNG_URL="${SEARXNG_URL:-http://127.0.0.1/searxng/}"
SEARXNG_LOCAL_PORT="${AUTOLUNO_SEARXNG_PORT:-8080}"
SEARXNG_LOCAL_URL="${AUTOLUNO_SEARXNG_LOCAL_URL:-http://127.0.0.1:${SEARXNG_LOCAL_PORT}/}"
SEARXNG_AUTO_SETUP="${SEARXNG_AUTO_SETUP:-true}"
SEARXNG_AUTO_START="${SEARXNG_AUTO_START:-true}"
SEARXNG_AUTO_LOGS="${SEARXNG_AUTO_LOGS:-true}"
SEARXNG_AUTO_UPDATE="${SEARXNG_AUTO_UPDATE:-false}"
SEARXNG_MANAGER="$ROOT_DIR/backend/frameworks/searxng/manage.sh"

QDRANT_PORT="${AUTOLUNO_QDRANT_PORT:-6333}"
QDRANT_GRPC_PORT="${AUTOLUNO_QDRANT_GRPC_PORT:-6334}"
QDRANT_LOCAL_URL="${AUTOLUNO_QDRANT_LOCAL_URL:-http://127.0.0.1:${QDRANT_PORT}}"
QDRANT_URL="${QDRANT_URL:-$QDRANT_LOCAL_URL}"
QDRANT_AUTO_SETUP="${QDRANT_AUTO_SETUP:-true}"
QDRANT_AUTO_START="${QDRANT_AUTO_START:-true}"
QDRANT_AUTO_LOGS="${QDRANT_AUTO_LOGS:-true}"
QDRANT_AUTO_UPDATE="${QDRANT_AUTO_UPDATE:-false}"
QDRANT_MANAGER="$ROOT_DIR/backend/frameworks/qdrant/manage.sh"

OLLAMA_PORT="${AUTOLUNO_OLLAMA_PORT:-11434}"
OLLAMA_LOCAL_URL="${AUTOLUNO_OLLAMA_LOCAL_URL:-http://127.0.0.1:${OLLAMA_PORT}}"
OLLAMA_URL="${OLLAMA_URL:-$OLLAMA_LOCAL_URL}"
OLLAMA_AUTO_SETUP="${OLLAMA_AUTO_SETUP:-true}"
OLLAMA_AUTO_START="${OLLAMA_AUTO_START:-true}"
OLLAMA_AUTO_LOGS="${OLLAMA_AUTO_LOGS:-true}"
OLLAMA_AUTO_UPDATE="${OLLAMA_AUTO_UPDATE:-false}"
OLLAMA_MODEL_LIST="${AUTOLUNO_OLLAMA_MODELS:-}"
OLLAMA_MANAGER="$ROOT_DIR/backend/frameworks/ollama/manage.sh"

BACKEND_LOG="$LOG_DIR/backend.log"
FRONTEND_LOG="$LOG_DIR/frontend.log"
NODE_LOG="$LOG_DIR/node_backend.log"
DEPS_LOG="$LOG_DIR/dependencies.log"
SEARXNG_LOG="$LOG_DIR/searxng.log"
QDRANT_LOG="$LOG_DIR/qdrant.log"
OLLAMA_LOG="$LOG_DIR/ollama.log"

BACKEND_PID_FILE="$LOG_DIR/backend.pid"
FRONTEND_PID_FILE="$LOG_DIR/frontend.pid"
NODE_PID_FILE="$LOG_DIR/node_backend.pid"

mkdir -p "$LOG_DIR"
touch "$BACKEND_LOG" "$FRONTEND_LOG" "$SEARXNG_LOG" "$QDRANT_LOG" "$OLLAMA_LOG"
touch "$DEPS_LOG"
> "$QDRANT_LOG"
if [ "$START_NODE" = "1" ]; then
  touch "$NODE_LOG"
fi

if [ -t 1 ] && [ -z "${NO_COLOR:-}" ]; then
  RESET=$'\033[0m'
  BOLD=$'\033[1m'
  DIM=$'\033[2m'
  RED=$'\033[31m'
  GREEN=$'\033[32m'
  YELLOW=$'\033[33m'
  BLUE=$'\033[34m'
  MAGENTA=$'\033[35m'
  CYAN=$'\033[36m'
else
  RESET=""
  BOLD=""
  DIM=""
  RED=""
  GREEN=""
  YELLOW=""
  BLUE=""
  MAGENTA=""
  CYAN=""
fi

say() { printf '%s\n' "$*"; }
say_info() { printf '[info] %s\n' "$*"; }
say_ok() { printf '[ ok ] %s\n' "$*"; }
say_warn() { printf '[warn] %s\n' "$*"; }
warn() { printf 'WARNING: %s\n' "$*" >&2; }
fail() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }
run_logged() {
  local label="$1"
  shift
  local cmd=("$@")
  if "${cmd[@]}" >> "$DEPS_LOG" 2>&1; then
    say_ok "$label"
    return 0
  fi
  say_warn "$label"
  return 1
}
stream_logs() {
  local label="$1"
  local color="$2"
  local log_file="$3"
  awk -v label="$label" -v color="$color" -v reset="$RESET" -v log_file="$log_file" '
    {
      print $0 >> log_file
      fflush(log_file)
      print color "[" label "]" reset " " $0
      fflush()
    }
  '
}

is_true() {
  case "${1,,}" in
    1|true|yes|on) return 0 ;;
    *) return 1 ;;
  esac
}

APT_UPDATED=0
apt_install() {
  is_true "$AUTO_INSTALL_SYSTEM" \
    || fail "A system dependency is missing. Enable AUTOLUNO_AUTO_INSTALL_SYSTEM=1 or install it manually."
  command -v apt-get >/dev/null 2>&1 \
    || fail "Automatic system-package installation currently supports apt-based Linux only."

  local sudo_cmd=()
  if [ "${EUID:-$(id -u)}" -ne 0 ]; then
    command -v sudo >/dev/null 2>&1 || fail "sudo is required to install system packages."
    sudo_cmd=(sudo)
  fi

  if [ "$APT_UPDATED" -eq 0 ]; then
    say "Updating system package index..."
    "${sudo_cmd[@]}" apt-get update
    APT_UPDATED=1
  fi

  say "Installing system packages: $*"
  DEBIAN_FRONTEND=noninteractive "${sudo_cmd[@]}" apt-get install -y "$@"
}

ensure_command() {
  local command_name="$1"
  shift
  if ! command -v "$command_name" >/dev/null 2>&1; then
    apt_install "$@"
  fi
  command -v "$command_name" >/dev/null 2>&1 \
    || fail "Unable to install required command: $command_name"
}

ensure_apt_packages() {
  local missing=() package
  command -v dpkg-query >/dev/null 2>&1 \
    || fail "Automatic SearXNG dependency setup requires an apt/dpkg-based Linux system."
  for package in "$@"; do
    if ! dpkg-query -W -f='${Status}' "$package" 2>/dev/null | grep -q 'install ok installed'; then
      missing+=("$package")
    fi
  done
  if [ "${#missing[@]}" -gt 0 ]; then
    apt_install "${missing[@]}"
  fi
}

ensure_base_commands() {
  ensure_command lsof lsof
  ensure_command curl curl
  ensure_command git git
  ensure_command make make
  ensure_command tar tar
  ensure_command python3 python3
  ensure_command node nodejs npm
  ensure_command npm npm

  if ! python3 -m venv --help >/dev/null 2>&1; then
    apt_install python3-venv python3-pip
  fi
}

port_pids() {
  lsof -tiTCP:"$1" -sTCP:LISTEN 2>/dev/null || true
}

stop_pid_file() {
  local label="$1"
  local pid_file="$2"

  [ -f "$pid_file" ] || return 0

  local pid
  pid="$(cat "$pid_file" 2>/dev/null || true)"
  if [ -n "$pid" ] && kill -0 "$pid" >/dev/null 2>&1; then
    say "Stopping $label (PID $pid)..."
    kill "$pid" >/dev/null 2>&1 || true
    for _ in $(seq 1 20); do
      kill -0 "$pid" >/dev/null 2>&1 || break
      sleep 0.25
    done
    if kill -0 "$pid" >/dev/null 2>&1; then
      warn "$label did not stop cleanly; force stopping PID $pid."
      kill -9 "$pid" >/dev/null 2>&1 || true
    fi
  fi
  rm -f "$pid_file"
}

stop_port() {
  local label="$1"
  local port="$2"
  local pids
  pids="$(port_pids "$port")"
  [ -z "$pids" ] && return 0

  say "Stopping $label on port $port (PID(s) $pids)..."
  # shellcheck disable=SC2086
  kill $pids >/dev/null 2>&1 || true
  sleep 0.5
  pids="$(port_pids "$port")"
  if [ -n "$pids" ]; then
    # shellcheck disable=SC2086
    kill -9 $pids >/dev/null 2>&1 || true
  fi
}

prepare_port() {
  local label="$1"
  local port="$2"
  local pid_file="$3"

  stop_pid_file "$label" "$pid_file"
  stop_port "$label" "$port"

  local pids
  pids="$(port_pids "$port")"
  [ -z "$pids" ] && return 0

  if [ "$FORCE_PORT_CLEAR" = "1" ]; then
    warn "Force clearing port $port for $label. Existing PID(s): $pids"
    # shellcheck disable=SC2086
    kill $pids >/dev/null 2>&1 || true
    sleep 1
    pids="$(port_pids "$port")"
    if [ -n "$pids" ]; then
      # shellcheck disable=SC2086
      kill -9 $pids >/dev/null 2>&1 || true
    fi
  else
    fail "Port $port is occupied by PID(s): $pids. Stop it or use AUTOLUNO_FORCE_PORT_CLEAR=1."
  fi
}

http_ready() {
  curl --silent --show-error --fail --max-time 3 "$1" >/dev/null 2>&1
}

wait_for_url() {
  local label="$1"
  local url="$2"
  local attempts="${3:-60}"

  for _ in $(seq 1 "$attempts"); do
    if http_ready "$url"; then
      say "$label is ready: $url"
      return 0
    fi
    sleep 1
  done
  return 1
}

wait_for_port() {
  local label="$1"
  local port="$2"
  local pid="$3"
  local attempts="${4:-45}"

  for _ in $(seq 1 "$attempts"); do
    if ! kill -0 "$pid" >/dev/null 2>&1; then
      fail "$label exited during startup. Check its log file."
    fi
    if [ -n "$(port_pids "$port")" ]; then
      say "$label is listening on port $port."
      return 0
    fi
    sleep 1
  done

  fail "$label did not start listening on port $port."
}

copy_env_template() {
  local target="$1"
  shift

  [ -e "$target" ] && return 0

  local template
  for template in "$@"; do
    if [ -f "$template" ]; then
      cp "$template" "$target"
      say "Created ${target#$ROOT_DIR/} from ${template#$ROOT_DIR/}."
      return 0
    fi
  done

  touch "$target"
  say "Created empty ${target#$ROOT_DIR/}."
}

set_env_key() {
  local file="$1"
  local key="$2"
  local value="$3"
  local temp_file

  touch "$file"
  temp_file="$(mktemp)"
  awk -v key="$key" -v value="$value" '
    BEGIN { written = 0 }
    $0 ~ "^[[:space:]]*" key "=" && written == 0 {
      print key "=" value
      written = 1
      next
    }
    { print }
    END {
      if (written == 0) print key "=" value
    }
  ' "$file" > "$temp_file"
  mv "$temp_file" "$file"
}

validate_ports() {
  local port reserved
  for port in $AUTOLUNO_PORTS; do
    case "$port" in
      ''|*[!0-9]*) fail "Invalid AutoLuno port: $port" ;;
    esac
    for reserved in $AUTOPOLY_PORTS; do
      if [ "$port" = "$reserved" ]; then
        fail "AutoLuno port $port would clash with AutoPoly."
      fi
    done
  done

  if [ "$PYTHON_PORT" = "$FRONTEND_PORT" ] \
    || { [ "$START_NODE" = "1" ] && [ "$NODE_PORT" = "$PYTHON_PORT" ]; } \
    || { [ "$START_NODE" = "1" ] && [ "$NODE_PORT" = "$FRONTEND_PORT" ]; }; then
    fail "AutoLuno application services cannot share a port."
  fi
}

write_searxng_manager() {
  local dir="$ROOT_DIR/backend/frameworks/searxng"
  local secret_file="$dir/.secret"
  mkdir -p "$dir"

  if [ ! -s "$secret_file" ]; then
    python3 -c 'import secrets; print(secrets.token_hex(32))' > "$secret_file"
    chmod 600 "$secret_file"
  fi

  if [ ! -f "$dir/settings.yml" ]; then
    local secret
    secret="$(cat "$secret_file")"
    cat > "$dir/settings.yml" <<EOF_SETTINGS
use_default_settings: true

general:
  debug: false
  instance_name: "AutoLuno Search"

search:
  safe_search: 0
  formats:
    - html
    - json

server:
  secret_key: "$secret"
  limiter: false
  image_proxy: true
  method: GET
EOF_SETTINGS
    say "Created backend/frameworks/searxng/settings.yml."
  fi

  # Always replace the manager so an older Docker-based manager cannot remain.
  cat > "$SEARXNG_MANAGER" <<'EOF_MANAGER'
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
EOF_MANAGER
  chmod +x "$SEARXNG_MANAGER"
}

write_qdrant_manager() {
  local dir="$ROOT_DIR/backend/frameworks/qdrant"
  mkdir -p "$dir/bin" "$dir/storage"

  # Always replace the manager so an older Docker-based manager cannot remain.
  cat > "$QDRANT_MANAGER" <<'EOF_MANAGER'
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
GRPC_PORT="${AUTOLUNO_QDRANT_GRPC_PORT:-6334}"
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
EOF_MANAGER
  chmod +x "$QDRANT_MANAGER"
}

write_ollama_manager() {
  local dir="$ROOT_DIR/backend/frameworks/ollama"
  mkdir -p "$dir/bin" "$dir/lib" "$dir/models" "$dir/home"

  cat > "$OLLAMA_MANAGER" <<'EOF_MANAGER'
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
EOF_MANAGER
  chmod +x "$OLLAMA_MANAGER"
}

setup_searxng() {
  if http_ready "$SEARXNG_URL"; then
    say "SearXNG is already available; reusing $SEARXNG_URL"
    return 0
  fi

  if ! is_true "$SEARXNG_AUTO_SETUP"; then
    warn "SearXNG is unavailable and automatic setup is disabled."
    return 0
  fi

  say "Setting up host-local SearXNG..."
  ensure_apt_packages python3-dev python3-babel python3-venv python3-pip python-is-python3 git build-essential libxslt1-dev zlib1g-dev libffi-dev libssl-dev
  write_searxng_manager

  if [ -n "$(port_pids "$SEARXNG_LOCAL_PORT")" ] && ! http_ready "$SEARXNG_LOCAL_URL"; then
    fail "SearXNG port $SEARXNG_LOCAL_PORT is occupied by another unhealthy service."
  fi

  AUTOLUNO_SEARXNG_PORT="$SEARXNG_LOCAL_PORT" \
    AUTOLUNO_SEARXNG_LOCAL_URL="$SEARXNG_LOCAL_URL" \
    SEARXNG_AUTO_UPDATE="$SEARXNG_AUTO_UPDATE" \
    "$SEARXNG_MANAGER" setup

  if is_true "$SEARXNG_AUTO_START"; then
    AUTOLUNO_SEARXNG_PORT="$SEARXNG_LOCAL_PORT" \
      AUTOLUNO_SEARXNG_LOCAL_URL="$SEARXNG_LOCAL_URL" \
      "$SEARXNG_MANAGER" start

    wait_for_url "SearXNG" "$SEARXNG_LOCAL_URL" 90 \
      || fail "SearXNG failed to become ready. Check $SEARXNG_LOG."
  fi

  SEARXNG_URL="$SEARXNG_LOCAL_URL"
}

setup_qdrant() {
  if http_ready "${QDRANT_URL%/}/"; then
    say "Qdrant is already available; reusing $QDRANT_URL"
    return 0
  fi

  if ! is_true "$QDRANT_AUTO_SETUP"; then
    warn "Qdrant is unavailable and automatic setup is disabled."
    return 0
  fi

  say "Setting up host-local Qdrant binary..."
  write_qdrant_manager

  if [ -n "$(port_pids "$QDRANT_PORT")" ] && ! http_ready "${QDRANT_LOCAL_URL%/}/"; then
    fail "Qdrant port $QDRANT_PORT is occupied by another unhealthy service."
  fi

  QDRANT_URL="$QDRANT_LOCAL_URL"
  AUTOLUNO_QDRANT_PORT="$QDRANT_PORT" \
    AUTOLUNO_QDRANT_GRPC_PORT="$QDRANT_GRPC_PORT" \
    QDRANT_URL="$QDRANT_URL" \
    QDRANT_AUTO_UPDATE="$QDRANT_AUTO_UPDATE" \
    "$QDRANT_MANAGER" setup

  if is_true "$QDRANT_AUTO_START"; then
    AUTOLUNO_QDRANT_PORT="$QDRANT_PORT" \
      AUTOLUNO_QDRANT_GRPC_PORT="$QDRANT_GRPC_PORT" \
      QDRANT_URL="$QDRANT_URL" \
      "$QDRANT_MANAGER" start

    wait_for_url "Qdrant" "${QDRANT_URL%/}/" 60 \
      || fail "Qdrant failed to become ready. Check $QDRANT_LOG."
  fi
}

setup_ollama() {
  local health_url="${OLLAMA_URL%/}/api/tags"
  if http_ready "$health_url"; then
    say "Ollama is already available; reusing $OLLAMA_URL"
  else
    if ! is_true "$OLLAMA_AUTO_SETUP"; then
      warn "Ollama is unavailable and automatic setup is disabled."
      return 0
    fi

    say "Setting up host-local Ollama..."
    ensure_command zstd zstd
    write_ollama_manager

    if [ -n "$(port_pids "$OLLAMA_PORT")" ] && ! http_ready "${OLLAMA_LOCAL_URL%/}/api/tags"; then
      fail "Ollama port $OLLAMA_PORT is occupied by another unhealthy service."
    fi

    OLLAMA_URL="$OLLAMA_LOCAL_URL"
    AUTOLUNO_OLLAMA_PORT="$OLLAMA_PORT" \
      OLLAMA_URL="$OLLAMA_URL" \
      OLLAMA_AUTO_UPDATE="$OLLAMA_AUTO_UPDATE" \
      "$OLLAMA_MANAGER" setup

    if is_true "$OLLAMA_AUTO_START"; then
      AUTOLUNO_OLLAMA_PORT="$OLLAMA_PORT" OLLAMA_URL="$OLLAMA_URL" "$OLLAMA_MANAGER" start
      wait_for_url "Ollama" "${OLLAMA_URL%/}/api/tags" 90 \
        || fail "Ollama failed to become ready. Check $OLLAMA_LOG."
    fi
  fi

  if [ -n "$OLLAMA_MODEL_LIST" ]; then
    # shellcheck disable=SC2086
    AUTOLUNO_OLLAMA_PORT="$OLLAMA_PORT" OLLAMA_URL="$OLLAMA_URL" "$OLLAMA_MANAGER" pull $OLLAMA_MODEL_LIST
  fi
}

start_service_logs() {
  local command="$1"
  local pid_var="$2"

  if [ -z "$command" ]; then
    printf -v "$pid_var" '%s' "none"
    return 0
  fi

  (
    trap - INT TERM EXIT
    exec bash -lc "$command"
  ) &
  printf -v "$pid_var" '%s' "$!"
}

stop_all() {
  say "Stopping AutoLuno..."
  stop_pid_file "Python backend" "$BACKEND_PID_FILE"
  stop_pid_file "frontend" "$FRONTEND_PID_FILE"
  stop_pid_file "legacy Node backend" "$NODE_PID_FILE"
  if [ -n "${SEARXNG_LOG_PID:-}" ] && [ "${SEARXNG_LOG_PID:-none}" != "none" ]; then
    kill "$SEARXNG_LOG_PID" >/dev/null 2>&1 || true
  fi
  if [ -n "${QDRANT_LOG_PID:-}" ] && [ "${QDRANT_LOG_PID:-none}" != "none" ]; then
    kill "$QDRANT_LOG_PID" >/dev/null 2>&1 || true
  fi
  if [ -n "${OLLAMA_LOG_PID:-}" ] && [ "${OLLAMA_LOG_PID:-none}" != "none" ]; then
    kill "$OLLAMA_LOG_PID" >/dev/null 2>&1 || true
  fi
  stop_port "Python backend" "$PYTHON_PORT"
  stop_port "frontend" "$FRONTEND_PORT"
  if [ "$START_NODE" = "1" ]; then
    stop_port "legacy Node backend" "$NODE_PORT"
  fi
  [ -x "$SEARXNG_MANAGER" ] && "$SEARXNG_MANAGER" stop || true
  [ -x "$QDRANT_MANAGER" ] && "$QDRANT_MANAGER" stop || true
  [ -x "$OLLAMA_MANAGER" ] && "$OLLAMA_MANAGER" stop || true
  say "AutoLuno services stopped."
}

on_exit() {
  local code=$?
  trap - INT TERM EXIT
  if [ "$code" -ne 0 ]; then
    stop_all
  fi
  exit "$code"
}

if [ "$ACTION" = "stop" ]; then
  stop_all
  exit 0
elif [ "$ACTION" != "start" ]; then
  fail "Usage: $0 [start|stop]"
fi

trap 'stop_all; exit 130' INT
trap 'stop_all; exit 143' TERM
trap on_exit EXIT

say "AutoLuno local development"
say "Backend + Frontend + local research services"
say "Shared services are host-wide; AutoLuno reuses SearXNG, Qdrant, and Ollama when they already exist."
say ""
say_info "Starting backend on :$PYTHON_PORT"
say_info "Starting frontend on :$FRONTEND_PORT"
if [ "$START_NODE" = "1" ]; then
  say_info "Starting legacy Node on :$NODE_PORT"
fi

ensure_base_commands
validate_ports

copy_env_template "$ROOT_DIR/.env" \
  "$ROOT_DIR/.env.example" \
  "$ROOT_DIR/.env.template"
if [ -d "$ROOT_DIR/frontend" ]; then
  copy_env_template "$ROOT_DIR/frontend/.env" \
    "$ROOT_DIR/frontend/.env.example" \
    "$ROOT_DIR/frontend/.env.template"
fi

# Replace any previous container-based managers before checking shared services.
write_searxng_manager
write_qdrant_manager
write_ollama_manager

setup_searxng
setup_qdrant
setup_ollama

if [ -x "$SEARXNG_MANAGER" ] && "$SEARXNG_MANAGER" status >/dev/null 2>&1; then
  say_info "Streaming SearXNG logs."
  start_service_logs "\"$SEARXNG_MANAGER\" logs" SEARXNG_LOG_PID
else
  SEARXNG_LOG_PID="none"
fi

QDRANT_LOG_PID="none"

if [ -x "$OLLAMA_MANAGER" ] && "$OLLAMA_MANAGER" status >/dev/null 2>&1; then
  start_service_logs "\"$OLLAMA_MANAGER\" logs" OLLAMA_LOG_PID
else
  OLLAMA_LOG_PID="none"
fi

export SEARXNG_URL QDRANT_URL OLLAMA_URL
set_env_key "$ROOT_DIR/.env" "SEARXNG_URL" "$SEARXNG_URL"
set_env_key "$ROOT_DIR/.env" "QDRANT_URL" "$QDRANT_URL"
set_env_key "$ROOT_DIR/.env" "OLLAMA_URL" "$OLLAMA_URL"

# Create the AutoLuno Python environment and install its packages.
if [ ! -x "$ROOT_DIR/.venv/bin/python" ]; then
  say "Creating AutoLuno Python virtual environment..."
  rm -rf "$ROOT_DIR/.venv"
  python3 -m venv "$ROOT_DIR/.venv"
fi

say "Preparing AutoLuno Python dependencies..."
run_logged "Python dependency base packages installed." \
  "$ROOT_DIR/.venv/bin/python" -m pip install --upgrade pip setuptools wheel
if [ -f "$ROOT_DIR/requirements.txt" ]; then
  run_logged "Python requirements installed." \
    "$ROOT_DIR/.venv/bin/python" -m pip install -r "$ROOT_DIR/requirements.txt"
else
  warn "No requirements.txt found; skipping Python package installation."
fi

[ -f "$ROOT_DIR/backend/main.py" ] || fail "Missing Python entrypoint: $ROOT_DIR/backend/main.py"
[ -d "$ROOT_DIR/frontend" ] || fail "Missing frontend directory: $ROOT_DIR/frontend"
[ -f "$ROOT_DIR/frontend/package.json" ] || fail "Missing frontend/package.json"

install_npm_dependencies() {
  local directory="$1"
  local label="$2"
  say "Preparing $label dependencies..."
  if [ ! -d "$directory/node_modules" ] && [ -f "$directory/package-lock.json" ]; then
    (cd "$directory" && npm ci --no-audit --no-fund) >> "$DEPS_LOG" 2>&1 \
      && say_ok "$label dependencies installed." \
      || { say_warn "$label dependencies install failed."; return 1; }
  else
    (cd "$directory" && npm install --no-audit --no-fund) >> "$DEPS_LOG" 2>&1 \
      && say_ok "$label dependencies installed." \
      || { say_warn "$label dependencies install failed."; return 1; }
  fi
}

install_npm_dependencies "$ROOT_DIR/frontend" "frontend"

FRONTEND_SCRIPT=""
if node -e 'const p=require(process.argv[1]);process.exit(p.scripts&&p.scripts.dev?0:1)' "$ROOT_DIR/frontend/package.json"; then
  FRONTEND_SCRIPT="dev"
elif node -e 'const p=require(process.argv[1]);process.exit(p.scripts&&p.scripts.start?0:1)' "$ROOT_DIR/frontend/package.json"; then
  FRONTEND_SCRIPT="start"
else
  fail "frontend/package.json must define a dev or start script."
fi

if [ "$START_NODE" = "1" ]; then
  [ -f "$ROOT_DIR/backend/legacy/server.js" ] || fail "Missing legacy Node entrypoint: $ROOT_DIR/backend/legacy/server.js"
  if [ -f "$ROOT_DIR/backend/package.json" ]; then
    install_npm_dependencies "$ROOT_DIR/backend" "legacy Node backend"
  fi
fi

prepare_port "Python backend" "$PYTHON_PORT" "$BACKEND_PID_FILE"
prepare_port "frontend" "$FRONTEND_PORT" "$FRONTEND_PID_FILE"
if [ "$START_NODE" = "1" ]; then
  prepare_port "legacy Node backend" "$NODE_PORT" "$NODE_PID_FILE"
fi

say ""
say "URLs"
say "  App       http://localhost:$FRONTEND_PORT"
say "  API       http://localhost:$PYTHON_PORT/api/server-time"
if [ "$START_NODE" = "1" ]; then
  say "  Node API:    http://localhost:$NODE_PORT"
else
  say "  Node API:    disabled; set AUTOLUNO_START_NODE=1 to enable it"
fi
say "  SearXNG   $SEARXNG_URL"
say "  Qdrant    $QDRANT_URL"
say "  Ollama    $OLLAMA_URL"
say ""

say "Starting Python backend on $PYTHON_PORT..."
(
  trap - INT TERM EXIT
  cd "$ROOT_DIR"
  exec > >(stream_logs "backend" "$CYAN" "$BACKEND_LOG") 2>&1
  exec env \
    PYTHONPATH="$ROOT_DIR" \
    AUTOLUNO_PYTHON_PORT="$PYTHON_PORT" \
    PORT="$PYTHON_PORT" \
    SEARXNG_URL="$SEARXNG_URL" \
    QDRANT_URL="$QDRANT_URL" \
    OLLAMA_URL="$OLLAMA_URL" \
    "$ROOT_DIR/.venv/bin/python" "$ROOT_DIR/backend/main.py"
) &
BACKEND_PID=$!
printf '%s\n' "$BACKEND_PID" > "$BACKEND_PID_FILE"

if [ "$START_NODE" = "1" ]; then
  say "Starting legacy Node backend on $NODE_PORT..."
  nohup bash -c '
    root="$1"
    port="$2"
    cd "$root/backend"
    exec env \
      AUTOLUNO_NODE_PORT="$port" \
      PORT="$port" \
      NODE_PATH="$root/backend/node_modules:$root/frontend/node_modules" \
      SEARXNG_URL="$SEARXNG_URL" \
      QDRANT_URL="$QDRANT_URL" \
      OLLAMA_URL="$OLLAMA_URL" \
      node "$root/backend/legacy/server.js"
  ' bash "$ROOT_DIR" "$NODE_PORT" >> "$NODE_LOG" 2>&1 &
  NODE_PID=$!
  printf '%s\n' "$NODE_PID" > "$NODE_PID_FILE"
fi

say "Starting Vite frontend on $FRONTEND_PORT using npm run $FRONTEND_SCRIPT..."
(
  trap - INT TERM EXIT
  cd "$ROOT_DIR/frontend"
  exec > >(stream_logs "frontend" "$MAGENTA" "$FRONTEND_LOG") 2>&1
  exec npm run "$FRONTEND_SCRIPT" -- --host 0.0.0.0 --port "$FRONTEND_PORT" --strictPort
) &
FRONTEND_PID=$!
printf '%s\n' "$FRONTEND_PID" > "$FRONTEND_PID_FILE"

wait_for_port "Python backend" "$PYTHON_PORT" "$BACKEND_PID" "$PYTHON_READY_ATTEMPTS"
wait_for_url "Python backend" "$PYTHON_READY_URL" "$PYTHON_READY_ATTEMPTS" \
  || fail "Python backend failed readiness check: $PYTHON_READY_URL. Check $BACKEND_LOG."
if [ "$START_NODE" = "1" ]; then
  wait_for_port "Legacy Node backend" "$NODE_PORT" "$NODE_PID" "$NODE_READY_ATTEMPTS"
fi
wait_for_port "Frontend" "$FRONTEND_PORT" "$FRONTEND_PID" "$FRONTEND_READY_ATTEMPTS"
wait_for_url "Frontend" "$FRONTEND_READY_URL" "$FRONTEND_READY_ATTEMPTS" \
  || fail "Frontend failed readiness check: $FRONTEND_READY_URL. Check $FRONTEND_LOG."

say ""
say_ok "Backend healthy  PID $BACKEND_PID"
if [ "$START_NODE" = "1" ]; then
  say_ok "Legacy Node healthy PID $NODE_PID"
fi
say_ok "Frontend healthy PID $FRONTEND_PID"
say_ok "SearXNG logs     PID ${SEARXNG_LOG_PID:-none}"
say_ok "Qdrant logs      PID ${QDRANT_LOG_PID:-none}"
say_ok "Ollama logs      PID ${OLLAMA_LOG_PID:-none}"
say ""
say "Logs"
say "  $BACKEND_LOG"
say "  $FRONTEND_LOG"
say "  $SEARXNG_LOG"
say "  $QDRANT_LOG"
say "  $OLLAMA_LOG"
say ""
say "Framework streams"
say "  backend -> $BACKEND_LOG"
say "  frontend -> $FRONTEND_LOG"
say "  searxng -> $SEARXNG_LOG"
say "  qdrant -> $QDRANT_LOG"
say "  ollama -> $OLLAMA_LOG"

wait_for_children() {
  local pids=("$BACKEND_PID" "$FRONTEND_PID")
  if [ "$START_NODE" = "1" ]; then
    pids+=("$NODE_PID")
  fi

  while :; do
    for pid in "${pids[@]}"; do
      if ! kill -0 "$pid" >/dev/null 2>&1; then
        fail "A managed service exited unexpectedly. Check the logs above."
      fi
    done
    sleep 1
  done
}

wait_for_children
