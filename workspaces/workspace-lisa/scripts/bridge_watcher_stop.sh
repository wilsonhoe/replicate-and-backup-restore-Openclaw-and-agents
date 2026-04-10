#!/bin/bash
# Bridge File Watcher Stopper

PID_FILE="/tmp/bridge_file_watcher.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        kill "$PID"
        rm "$PID_FILE"
        echo "🛑 Bridge watcher stopped"
    else
        echo "⚠️  Process not running"
        rm "$PID_FILE"
    fi
else
    echo "⚠️  No PID file found - watcher may not be running"
fi
