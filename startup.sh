#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; LOG="$ROOT/logs"; ACTION="${1:-start}"
PYTHON="${AUTOLUNO_PYTHON:-$ROOT/.venv/bin/python}"; START_FRONTEND="${AUTOLUNO_START_FRONTEND:-1}"; mkdir -p "$LOG"
choose_port(){ "$PYTHON" - "$1" "$2" <<'PY'
import socket,sys
ports=[int(sys.argv[2])] if sys.argv[2] else range(int(sys.argv[1]),int(sys.argv[1])+20)
for p in ports:
 with socket.socket() as s:
  try:s.bind(('127.0.0.1',p))
  except OSError:continue
 print(p);raise SystemExit
raise SystemExit('requested port unavailable or bounded allocation range exhausted')
PY
}
stop_one(){ local f="$1" p;[ -f "$f" ]||return 0;p="$(sed -n '1p' "$f")";if [ -n "$p" ]&&kill -0 "$p" 2>/dev/null;then kill "$p";wait "$p" 2>/dev/null||true;fi;rm -f "$f";}
stop_all(){ stop_one "$LOG/frontend.pid";stop_one "$LOG/backend.pid";}
case "$ACTION" in
 stop)stop_all;printf 'Auto Luno stopped.\n';exit;;restart)"$0" stop;exec "$0" start;;
 status)for n in backend frontend;do p="$(sed -n '1p' "$LOG/$n.pid" 2>/dev/null||true)";if [ -n "$p" ]&&kill -0 "$p" 2>/dev/null;then printf '[running] %s PID %s\n' "$n" "$p";else printf '[stopped] %s\n' "$n";fi;done;[ ! -f "$LOG/endpoints.env" ]||cat "$LOG/endpoints.env";exit;;
 logs)tail -n 100 -F "$LOG/backend.log" "$LOG/frontend.log";exit;;start);;*)printf 'Usage: %s [start|stop|restart|status|logs]\n' "$0" >&2;exit 2;;esac
[ "${AUTOLUNO_START_NODE:-0}" = 0 ]||{ printf 'Legacy Node backend is quarantined and is never launched by startup.sh.\n' >&2;exit 1;}
[ -x "$PYTHON" ]||{ printf 'Run ./setup.sh first; .venv is missing.\n' >&2;exit 1;}
"$PYTHON" -c 'import flask,pymongo'||{ printf 'Backend dependencies incomplete; run ./setup.sh.\n' >&2;exit 1;}
BP="$(choose_port "${AUTOLUNO_BACKEND_PORT_BASE:-8001}" "${AUTOLUNO_BACKEND_PORT:-${AUTOLUNO_PYTHON_PORT:-}}")";FP="$(choose_port "${AUTOLUNO_FRONTEND_PORT_BASE:-3001}" "${AUTOLUNO_FRONTEND_PORT:-}")";BU="http://127.0.0.1:$BP";FU="http://127.0.0.1:$FP";stop_all
printf 'BACKEND_PORT=%s\nFRONTEND_PORT=%s\nBACKEND_URL=%s\nFRONTEND_URL=%s\nAPI_BASE_URL=%s/api\n' "$BP" "$FP" "$BU" "$FU" "$BU">"$LOG/endpoints.env"
(cd "$ROOT"&&exec "$PYTHON" -m flask --app backend.app.main:app run --host 127.0.0.1 --port "$BP")>"$LOG/backend.log" 2>&1&echo $!>"$LOG/backend.pid"
if [ "$START_FRONTEND" = 1 ];then command -v node>/dev/null&&command -v npm>/dev/null||{ "$0" stop;printf 'Node.js/npm unavailable; set AUTOLUNO_START_FRONTEND=0 for backend-only.\n' >&2;exit 1;};[ -d "$ROOT/frontend/node_modules" ]||{ "$0" stop;printf 'Frontend dependencies missing; run ./setup.sh.\n' >&2;exit 1;};(cd "$ROOT/frontend"&&VITE_PROXY_TARGET="$BU" exec npm run dev -- --host 127.0.0.1 --port "$FP" --strictPort)>"$LOG/frontend.log" 2>&1&echo $!>"$LOG/frontend.pid";fi
sleep 1;kill -0 "$(cat "$LOG/backend.pid")" 2>/dev/null||{ tail -30 "$LOG/backend.log" >&2;exit 1;}
printf 'Backend liveness: %s/api/health\nReadiness (MongoDB required): %s/api/ready\n' "$BU" "$BU";[ "$START_FRONTEND" != 1 ]||printf 'Frontend: %s (API proxy -> %s)\n' "$FU" "$BU";printf 'Logs: %s\n' "$LOG"
