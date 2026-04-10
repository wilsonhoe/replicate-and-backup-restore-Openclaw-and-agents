#!/bin/bash
# Gateway monitoring report - sends summary via Telegram

LOG_FILE="/tmp/gateway-monitor-$(date +%Y%m%d).log"
REPORT_FILE="/tmp/gateway-report-$(date +%Y%m%d).txt"

if [[ ! -f "$LOG_FILE" ]]; then
    echo "No monitoring log found" > "$REPORT_FILE"
else
    TOTAL_CHECKS=$(wc -l < "$LOG_FILE")
    OK_CHECKS=$(grep -c "RPC probe: ok" "$LOG_FILE" 2>/dev/null || echo 0)
    FAILED_CHECKS=$(grep -c "RPC probe: failed\|error" "$LOG_FILE" 2>/dev/null || echo 0)

    START_TIME=$(head -1 "$LOG_FILE" | cut -d']' -f1 | tr -d '[')
    END_TIME=$(tail -1 "$LOG_FILE" | cut -d']' -f1 | tr -d '[')

    # Calculate uptime percentage
    if [ "$TOTAL_CHECKS" -gt 0 ]; then
        UPTIME_PCT=$(( OK_CHECKS * 100 / TOTAL_CHECKS ))
    else
        UPTIME_PCT=0
    fi

    # Determine stability status
    if [ "$UPTIME_PCT" -eq 100 ] && [ "$FAILED_CHECKS" -eq 0 ]; then
        STABILITY="🟢 STABLE - No issues detected"
    elif [ "$UPTIME_PCT" -ge 95 ]; then
        STABILITY="🟡 MOSTLY STABLE - Minor issues"
    else
        STABILITY="🔴 UNSTABLE - Frequent issues detected"
    fi

    cat > "$REPORT_FILE" << EOF
🦞 OpenClaw Gateway Monitoring Report

Period: $START_TIME to $END_TIME
Total Checks: $TOTAL_CHECKS
✅ Successful: $OK_CHECKS
❌ Failed: $FAILED_CHECKS
📊 Uptime: ${UPTIME_PCT}%

Status: $STABILITY

Gateway Status: $(openclaw gateway status 2>&1 | grep -E "Runtime:|RPC probe:" | tr '\n' ' ')

Recent Logs:
$(tail -5 "$LOG_FILE")
EOF
fi

# Send via Telegram using openclaw
openclaw message send --channel telegram --target "507276036" --message "$(cat $REPORT_FILE)" 2>&1

# Cleanup
rm -f "$LOG_FILE" "$REPORT_FILE"
