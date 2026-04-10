#!/bin/bash
# Bridge Monitoring Status

PID_FILE="/tmp/bridge_file_watcher.pid"
TRIGGER_FILE="/home/wls/bridge/.bridge_trigger"
LAST_SEEN_FILE="/home/wls/.openclaw/workspace-lisa/memory/bridge-last-seen.txt"
OUTBOX_FILE="/home/wls/bridge/claude-outbox.md"

echo "═══════════════════════════════════════"
echo "  Bridge Monitoring System Status"
echo "═══════════════════════════════════════"
echo ""

# Watcher Status
echo "📡 File Watcher:"
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "   Status: 🟢 RUNNING (PID: $PID)"
    else
        echo "   Status: 🔴 NOT RUNNING (stale PID file)"
    fi
else
    echo "   Status: 🔴 NOT RUNNING"
fi
echo ""

# Last Seen
echo "🕐 Last Seen:"
if [ -f "$LAST_SEEN_FILE" ]; then
    echo "   $(cat "$LAST_SEEN_FILE")"
else
    echo "   No record"
fi
echo ""

# Trigger Status
echo "⚡ Trigger File:"
if [ -f "$TRIGGER_FILE" ]; then
    echo "   🟡 PENDING - New message waiting"
    cat "$TRIGGER_FILE"
else
    echo "   ✅ None (no new messages)"
fi
echo ""

# Bridge File
echo "📄 Bridge File:"
if [ -f "$OUTBOX_FILE" ]; then
    LINES=$(wc -l < "$OUTBOX_FILE")
    SIZE=$(du -h "$OUTBOX_FILE" | cut -f1)
    echo "   Path: $OUTBOX_FILE"
    echo "   Lines: $LINES"
    echo "   Size: $SIZE"
else
    echo "   ❌ File not found"
fi
echo ""

# Cron Jobs
echo "⏰ Active Cron Jobs:"
openclaw cron list | grep -E "(bridge|claude)" || echo "   No bridge-related jobs"
echo ""

echo "═══════════════════════════════════════"
echo "Commands:"
echo "  Start:  bash scripts/bridge_watcher_start.sh"
echo "  Stop:   bash scripts/bridge_watcher_stop.sh"
echo "  Status: bash scripts/bridge_status.sh"
echo "═══════════════════════════════════════"
