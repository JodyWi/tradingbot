#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$ROOT_DIR/logs"

PYTHON_PORT="${AUTOLUNO_PYTHON_PORT:-8001}"
FRONTEND_PORT="${AUTOLUNO_FRONTEND_PORT:-3001}"
START_NODE="${AUTOLUNO_START_NODE:-0}"
NODE_PORT="${AUTOLUNO_NODE_PORT:-3002}"

AUTOPOLY_PORTS="8000 5173"
AUTOLUNO_PORTS="$PYTHON_PORT $FRONTEND_PORT"
if [ "$START_NODE" = "1" ]; then
  AUTOLUNO_PORTS="$AUTOLUNO_PORTS $NODE_PORT"
fi

mkdir -p "$LOG_DIR"

for port in $AUTOLUNO_PORTS; do
  for reserved in $AUTOPOLY_PORTS; do
    if [ "$port" = "$reserved" ]; then
      echo "Refusing to start: AutoLuno port $port would clash with AutoPoly."
      exit 1
    fi
  done
done

stop_port() {
  local port="$1"
  local pids
  pids="$(lsof -ti :"$port" 2>/dev/null || true)"
  if [ -n "$pids" ]; then
    echo "Stopping existing process on port $port: $pids"
    kill $pids 2>/dev/null || true
    sleep 1
  fi

  pids="$(lsof -ti :"$port" 2>/dev/null || true)"
  if [ -n "$pids" ]; then
    echo "Force stopping process on port $port: $pids"
    kill -9 $pids 2>/dev/null || true
  fi
}

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1"
    exit 1
  fi
}

require_command lsof
require_command node
require_command npm

echo "AutoLuno ports:"
echo "  Python API:  http://localhost:$PYTHON_PORT"
if [ "$START_NODE" = "1" ]; then
  echo "  Node API:    http://localhost:$NODE_PORT"
else
  echo "  Node API:    disabled by default; set AUTOLUNO_START_NODE=1 to run legacy SQLite service"
fi
echo "  Frontend:    http://localhost:$FRONTEND_PORT"
echo "AutoPoly reserved ports left untouched: $AUTOPOLY_PORTS"

stop_port "$PYTHON_PORT"
if [ "$START_NODE" = "1" ]; then
  stop_port "$NODE_PORT"
fi
stop_port "$FRONTEND_PORT"

if [ ! -d "$ROOT_DIR/backend/venv" ]; then
  echo "Missing backend virtualenv: $ROOT_DIR/backend/venv"
  echo "Create it with: cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
  exit 1
fi

echo "Starting Python backend on $PYTHON_PORT..."
nohup bash -c '
  cd "$1"
  source backend/venv/bin/activate
  PYTHONPATH="$1" python backend/server.py
' bash "$ROOT_DIR" >> "$LOG_DIR/backend.log" 2>&1 &

if [ "$START_NODE" = "1" ]; then
  echo "Starting legacy Node backend on $NODE_PORT..."
  nohup bash -c '
    cd "$1/backend"
    NODE_PATH="$1/frontend/node_modules" node server.js
  ' bash "$ROOT_DIR" >> "$LOG_DIR/node_backend.log" 2>&1 &
fi

echo "Starting Vite frontend on $FRONTEND_PORT..."
nohup bash -c '
  cd "$1/frontend"
  npm start -- --host 0.0.0.0 --port "$2"
' bash "$ROOT_DIR" "$FRONTEND_PORT" >> "$LOG_DIR/frontend.log" 2>&1 &

echo "Started AutoLuno. Logs:"
echo "  $LOG_DIR/backend.log"
if [ "$START_NODE" = "1" ]; then
  echo "  $LOG_DIR/node_backend.log"
fi
echo "  $LOG_DIR/frontend.log"
