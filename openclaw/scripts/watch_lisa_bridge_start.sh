#!/bin/bash
# Start Lisa Bridge Monitor as a background daemon
# Usage: ./watch_lisa_bridge_start.sh [start|stop|status]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MONITOR_SCRIPT="$SCRIPT_DIR/lisa_bridge_monitor.py"
PID_FILE="/home/wls/.openclaw/workspace-lisa/.lisa_bridge_monitor.pid"
LOG_FILE="/home/wls/.openclaw/workspace-lisa/.lisa_bridge_monitor.log"

case "${1:-start}" in
    start)
        if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
            echo "Lisa bridge monitor already running (PID: $(cat "$PID_FILE"))"
            exit 0
        fi

        echo "Starting Lisa bridge monitor..."
        nohup python3 "$MONITOR_SCRIPT" > "$LOG_FILE" 2>&1 &
        echo $! > "$PID_FILE"
        echo "Started with PID: $(cat "$PID_FILE")"
        echo "Log: $LOG_FILE"
        ;;

    stop)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if kill -0 "$PID" 2>/dev/null; then
                echo "Stopping Lisa bridge monitor (PID: $PID)..."
                kill "$PID"
                rm "$PID_FILE"
                echo "Stopped"
            else
                echo "Process not running, cleaning up PID file"
                rm "$PID_FILE"
            fi
        else
            echo "No PID file found - killing any python bridge monitor processes"
            pkill -f "lisa_bridge_monitor.py"
        fi
        ;;

    status)
        if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
            echo "Lisa bridge monitor: RUNNING (PID: $(cat "$PID_FILE"))"
            echo "Log: $LOG_FILE"
            tail -5 "$LOG_FILE" 2>/dev/null || echo "No log entries yet"
        else
            echo "Lisa bridge monitor: NOT RUNNING"
            # Check if running without PID file
            if pgrep -f "lisa_bridge_monitor.py" > /dev/null; then
                echo "  (Found orphaned process, consider running: stop then start)"
            fi
        fi
        ;;

    restart)
        $0 stop
        sleep 2
        $0 start
        ;;

    *)
        echo "Usage: $0 [start|stop|status|restart]"
        exit 1
        ;;
esac
