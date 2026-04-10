#!/bin/bash
# Lisa Bridge Watcher - Monitors BRIDGE_LISA.md for changes
# Usage: ./watch_lisa_bridge.sh &

BRIDGE_FILE="/home/wls/.openclaw/workspace-lisa/BRIDGE_LISA.md"
LOG_FILE="/home/wls/.openclaw/workspace-lisa/.bridge_watch.log"
TRIGGER_FILE="/home/wls/.openclaw/workspace-lisa/.bridge_trigger"
LAST_HASH=""

echo "[$(date)] Lisa Bridge Watcher started" >> "$LOG_FILE"

# Initial hash
LAST_HASH=$(md5sum "$BRIDGE_FILE" | awk '{print $1}')

echo "[$(date)] Initial hash: $LAST_HASH" >> "$LOG_FILE"

# Watch loop
while true; do
    sleep 5
    CURRENT_HASH=$(md5sum "$BRIDGE_FILE" | awk '{print $1}')

    if [ "$CURRENT_HASH" != "$LAST_HASH" ]; then
        echo "[$(date)] 🔴 BRIDGE CHANGED - Lisa may have posted" >> "$LOG_FILE"
        echo "[$(date)] New hash: $CURRENT_HASH" >> "$LOG_FILE"

        # Get last 50 lines to see what changed
        echo "--- Last 50 lines of bridge ---" >> "$LOG_FILE"
        tail -50 "$BRIDGE_FILE" >> "$LOG_FILE"
        echo "--- End of change ---" >> "$LOG_FILE"
        echo "" >> "$LOG_FILE"

        # Create trigger file to notify Claude
        echo "BRIDGE_CHANGED_AT=$(date -Iseconds)" > "$TRIGGER_FILE"
        echo "PREVIOUS_HASH=$LAST_HASH" >> "$TRIGGER_FILE"
        echo "CURRENT_HASH=$CURRENT_HASH" >> "$TRIGGER_FILE"
        echo "ACTION=READ_AND_RESPOND" >> "$TRIGGER_FILE"

        # Update hash
        LAST_HASH="$CURRENT_HASH"
    fi
done
