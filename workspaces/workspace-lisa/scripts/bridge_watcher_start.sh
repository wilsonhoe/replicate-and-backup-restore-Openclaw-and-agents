#!/bin/bash
# Bridge File Watcher Starter
# Run this to start monitoring for Claude messages

SCRIPT_DIR="/home/wls/.openclaw/workspace-lisa/scripts"
PID_FILE="/tmp/bridge_file_watcher.pid"
LOG_FILE="/home/wls/.openclaw/workspace-lisa/memory/bridge-watcher.log"

echo "🟢 Starting Bridge File Watcher..."

# Check if already running
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "⚠️  Watcher already running (PID: $PID)"
        exit 1
    else
        rm "$PID_FILE"
    fi
fi

# Start watcher in background
nohup python3 "$SCRIPT_DIR/bridge_file_watcher.py" > "$LOG_FILE" 2>&1 &
echo $! > "$PID_FILE"

echo "✅ Bridge watcher started (PID: $(cat $PID_FILE))"
echo "📋 Logs: $LOG_FILE"
echo "⏱️  Checking every 5 seconds"
echo ""
echo "To stop: kill $(cat $PID_FILE)"
