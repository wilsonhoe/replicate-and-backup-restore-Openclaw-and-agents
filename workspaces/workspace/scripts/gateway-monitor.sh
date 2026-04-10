#!/bin/bash
# Gateway monitoring script - logs status every 5 minutes

LOG_FILE="/tmp/gateway-monitor-$(date +%Y%m%d).log"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

# Get gateway status
STATUS=$(openclaw gateway status 2>&1)
RUNNING=$(echo "$STATUS" | grep -E "Runtime:|RPC probe:" | tr '\n' '|')

# Log the status
echo "[$TIMESTAMP] $RUNNING" >> "$LOG_FILE"

# Also log any errors
if echo "$STATUS" | grep -qi "error\|failed"; then
    echo "[$TIMESTAMP] ERROR: $(echo "$STATUS" | grep -iE "error|failed" | head -3)" >> "$LOG_FILE"
fi
