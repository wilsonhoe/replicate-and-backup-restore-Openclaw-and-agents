#!/bin/bash
# Bridge Watcher - Monitors claude-outbox.md for changes and triggers Lisa

BRIDGE_FILE="/home/wls/bridge/claude-outbox.md"
LOG_FILE="/home/wls/.openclaw/workspace/logs/bridge-watcher.log"

mkdir -p "$(dirname "$LOG_FILE")"

echo "[$(date)] Bridge watcher started. Monitoring $BRIDGE_FILE" >> "$LOG_FILE"

# Use inotifywait to watch for file modifications
if command -v inotifywait &> /dev/null; then
    inotifywait -m -e modify "$BRIDGE_FILE" --format '%T %w %f' --timefmt '%Y-%m-%d %H:%M:%S' 2>/dev/null | while read timestamp dir file; do
        echo "[$timestamp] Bridge file modified - triggering Lisa check" >> "$LOG_FILE"
        # Signal to OpenClaw that bridge has new content
        # This will be picked up by the proactive agent heartbeat
    done
else
    # Fallback: poll every 10 seconds if inotifywait not available
    echo "[$(date)] inotifywait not available, using poll fallback" >> "$LOG_FILE"
    LAST_SIZE=$(stat -c%s "$BRIDGE_FILE" 2>/dev/null || echo "0")
    while true; do
        sleep 10
        CURRENT_SIZE=$(stat -c%s "$BRIDGE_FILE" 2>/dev/null || echo "0")
        if [ "$CURRENT_SIZE" -ne "$LAST_SIZE" ]; then
            echo "[$(date)] Bridge file changed ($LAST_SIZE -> $CURRENT_SIZE bytes)" >> "$LOG_FILE"
            LAST_SIZE=$CURRENT_SIZE
        fi
    done
fi
