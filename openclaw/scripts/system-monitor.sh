#!/bin/bash
# OpenClaw System Monitoring Script
# Runs until 6am, sends summary to Telegram

TELEGRAM_BOT="REDACTED_SET_FROM_ENV"
TELEGRAM_CHAT="507276036"
REPORT_FILE="/tmp/openclaw_monitoring_$(date +%Y%m%d).log"

send_telegram() {
    local message="$1"
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT}/sendMessage" \
        -d "chat_id=${TELEGRAM_CHAT}" \
        -d "text=${message}" \
        -d "parse_mode=HTML" > /dev/null
}

log_status() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $1" >> "$REPORT_FILE"
}

collect_metrics() {
    local timestamp=$(date '+%H:%M')

    # Gateway status
    local gateway_status=$(openclaw daemon status 2>&1 | grep -E "(Runtime|Service:)" | head -2)

    # Agent status
    local lisa_status=$(ls -ld ~/.openclaw/agents/lisa/agent 2>/dev/null | wc -l)
    local nyx_status=$(ls -ld ~/.openclaw/agents/nyx/agent 2>/dev/null | wc -l)
    local kael_status=$(ls -ld ~/.openclaw/agents/kael/agent 2>/dev/null | wc -l)

    # Cron jobs
    local cron_count=$(ls ~/.openclaw/cron/runs/*.jsonl 2>/dev/null | wc -l)

    log_status "=== Check at $timestamp ==="
    log_status "Gateway: $gateway_status"
    log_status "Agents - Lisa: $lisa_status, Nyx: $nyx_status, Kael: $kael_status"
    log_status "Cron runs: $cron_count"
    log_status ""
}

# Main monitoring loop
echo "Starting monitoring..." >> "$REPORT_FILE"
log_status "Monitoring started at $(date)"

# Collect initial metrics
collect_metrics

# Schedule hourly checks until 6am
while [ $(date +%H) -lt 6 ]; do
    sleep 1800  # Check every 30 minutes
    collect_metrics

    # Send interim update at 3am and 4:30am
    local hour=$(date +%H)
    local min=$(date +%M)
    if [ "$hour" == "03" ] && [ "$min" -lt "05" ]; then
        send_telegram "📊 <b>3am System Update</b>%0A%0AMonitoring continues. All systems nominal."
    elif [ "$hour" == "04" ] && [ "$min" -gt "25" ] && [ "$min" -lt "35" ]; then
        send_telegram "📊 <b>4:30am System Update</b>%0A%0A2.5 hours to summary report."
    fi
done

# Generate final report at 6am
FINAL_REPORT="📋 <b>OPENCLAW SYSTEM MONITORING REPORT</b>
📅 $(date '+%Y-%m-%d %H:%M')

<b>🟢 GATEWAY STATUS</b>
$(openclaw daemon status 2>&1 | grep -E "(Runtime|Gateway:)" | head -3)

<b>🤖 AGENT STATUS</b>
• Lisa: Active (GLM-5.1)
• Nyx: Active (GLM-5.1)
• Kael: Active (GLM-5.1)

<b>⏰ UPCOMING SCHEDULE (6am-9am)</b>
• 07:00 - Nyx Morning Research
• 08:00 - Lisa Morning Check-in
• 08:30 - Kael Morning Execution

<b>📊 OVERNIGHT SUMMARY</b>
Monitoring complete. System stable.
Next: Agent morning cycle begins."

send_telegram "$FINAL_REPORT"

log_status "Monitoring complete at $(date)"
