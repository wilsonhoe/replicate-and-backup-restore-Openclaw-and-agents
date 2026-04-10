#!/bin/bash
# OpenClaw-compatible gateway monitoring script
# This script uses OpenClaw's built-in tools instead of direct execution

LOG_FILE="/home/wls/.openclaw/workspace/logs/gateway-monitor.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

# Function to log messages
log_message() {
    echo "[$TIMESTAMP] $1" >> "$LOG_FILE"
}

# Check if we can access the gateway configuration
if [ -f "/home/wls/.openclaw/openclaw.json" ]; then
    log_message("Gateway configuration file exists - checking basic health"
else
    log_message("ERROR: Gateway configuration file not found"
fi

# Check if logs directory is writable
if [ -w "$(dirname "$LOG_FILE")" ]; then
    log_message("Log directory is writable"
else
    log_message("WARNING: Log directory may not be writable"
fi

log_message("Gateway monitor check completed"