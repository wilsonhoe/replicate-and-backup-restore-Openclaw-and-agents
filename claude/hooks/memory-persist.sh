#!/bin/bash
# Memory persistence hook - saves context across sessions

MEMORY_DIR="${ECC_MEMORY_DIR:-/home/wls/.claude/memory}"
SESSION_ID="${ECC_SESSION_ID:-default}"

# Save current context state
echo "💾 Saving session context..." >&2
mkdir -p "$MEMORY_DIR"

# Store timestamp of last activity
date +%s > "$MEMORY_DIR/last_activity_$SESSION_ID.timestamp"

exit 0
