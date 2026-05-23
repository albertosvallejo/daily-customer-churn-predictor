#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="/data/.openclaw/workspace/projects/TFM/daily-customer-churn-predictor"
HOST="127.0.0.1"
PORT="62881"
LOG_DIR="$PROJECT_ROOT/logs"
LOG_FILE="$LOG_DIR/churn_api_62881.log"
PID_FILE="$LOG_DIR/churn_api_62881.pid"
HEALTH_URL="http://${HOST}:${PORT}/health"
START_CMD=(python3 -c "from api.churn_service import run_server; run_server(port=${PORT})")

mkdir -p "$LOG_DIR"

check_health() {
  python3 - <<'PY'
import json
import sys
import urllib.request
url = "http://127.0.0.1:62881/health"
try:
    with urllib.request.urlopen(url, timeout=3) as response:
        payload = json.loads(response.read().decode("utf-8"))
    ok = response.status == 200 and payload.get("service") == "daily-customer-churn-api" and payload.get("status") == "ok"
except Exception:
    ok = False
sys.exit(0 if ok else 1)
PY
}

find_listener_info() {
  python3 - <<'PY'
from pathlib import Path
import os
port_hex = format(62881, '04X')
inodes = []
with open('/proc/net/tcp') as handle:
    next(handle)
    for line in handle:
        parts = line.split()
        local = parts[1]
        state = parts[3]
        inode = parts[9]
        _ip, port = local.split(':')
        if port == port_hex and state == '0A':
            inodes.append(inode)
for pid in filter(str.isdigit, os.listdir('/proc')):
    fd_dir = Path('/proc') / pid / 'fd'
    try:
        for fd in fd_dir.iterdir():
            try:
                target = os.readlink(fd)
            except OSError:
                continue
            for inode in inodes:
                if target == f'socket:[{inode}]':
                    cmdline = (Path('/proc') / pid / 'cmdline').read_text(errors='ignore').replace('\x00', ' ').strip()
                    print(f"{pid}\t{cmdline}")
                    raise SystemExit
    except Exception:
        continue
PY
}

if check_health; then
  echo "healthy"
  exit 0
fi

listener_info="$(find_listener_info || true)"
if [[ -n "$listener_info" ]]; then
  listener_pid="${listener_info%%$'\t'*}"
  listener_cmd="${listener_info#*$'\t'}"
  if [[ "$listener_cmd" == *"api.churn_service"* ]]; then
    kill "$listener_pid" || true
    sleep 1
  else
    echo "Port ${PORT} is already occupied by another process: ${listener_cmd}" >&2
    exit 1
  fi
fi

if [[ -f "$PID_FILE" ]]; then
  stale_pid="$(cat "$PID_FILE" 2>/dev/null || true)"
  if [[ -n "$stale_pid" ]] && kill -0 "$stale_pid" 2>/dev/null; then
    kill "$stale_pid" || true
    sleep 1
  fi
fi

cd "$PROJECT_ROOT"
nohup env PYTHONPATH=src "${START_CMD[@]}" >> "$LOG_FILE" 2>&1 &
new_pid=$!
printf '%s\n' "$new_pid" > "$PID_FILE"

for _ in $(seq 1 15); do
  if check_health; then
    echo "started:${new_pid}"
    exit 0
  fi
  sleep 1
done

echo "Failed to start churn API on port ${PORT}" >&2
exit 1
