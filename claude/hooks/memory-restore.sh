#!/bin/bash
# Memory restore hook - loads previous session context

MEMORY_DIR="${ECC_MEMORY_DIR:-/home/wls/.claude/memory}"
SESSION_ID="${ECC_SESSION_ID:-default}"

if [ -f "$MEMORY_DIR/last_activity_$SESSION_ID.timestamp" ]; then
    LAST_ACTIVITY=$(cat "$MEMORY_DIR/last_activity_$SESSION_ID.timestamp")
    CURRENT_TIME=$(date +%s)
    DIFF=$((CURRENT_TIME - LAST_ACTIVITY))

    # Only restore if session was active in last 24 hours
    if [ $DIFF -lt 86400 ]; then
        echo "🔄 Restoring session context (last active $DIFF seconds ago)" >&2
    fi
fi

exit 0
