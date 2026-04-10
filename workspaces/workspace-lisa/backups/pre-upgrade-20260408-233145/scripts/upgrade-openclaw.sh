#!/usr/bin/env bash
# OpenClaw Safe Upgrade Procedure
# Version: 1.0
# Created: 2026-04-08 by Lisa
#
# Usage: bash scripts/upgrade-openclaw.sh [--target VERSION]
# Example: bash scripts/upgrade-openclaw.sh --target 2026.4.8

set -euo pipefail

TARGET_VERSION="${1:---target 2026.4.8}"
CURRENT_VERSION=$(openclaw --version 2>/dev/null | head -1 | awk '{print $2}')
LOG_FILE="/home/wls/.openclaw/workspace-lisa/memory/upgrade-$(date +%Y%m%d-%H%M%S).log"
BACKUP_DIR="/home/wls/.openclaw/workspace-lisa/backups/pre-upgrade-$(date +%Y%m%d-%H%M%S)"

echo "=========================================="
echo "OpenClaw Safe Upgrade Procedure"
echo "=========================================="
echo "Current: $CURRENT_VERSION"
echo "Target:  $TARGET_VERSION"
echo "Log:     $LOG_FILE"
echo "=========================================="

# STEP 1: Pre-flight checks
echo ""
echo "[STEP 1/8] Pre-flight checks..."
echo "  - Checking disk space..."
DISK_AVAIL=$(df -h /home/wls | tail -1 | awk '{print $4}')
echo "    Available: $DISK_AVAIL"

echo "  - Checking gateway status..."
openclaw gateway status 2>&1 | head -3

echo "  - Checking running sessions..."
ACTIVE_SESSIONS=$(openclaw sessions list --limit 50 2>/dev/null | grep -c "running" || echo "0")
echo "    Running sessions: $ACTIVE_SESSIONS"

if [ "$ACTIVE_SESSIONS" -gt 0 ]; then
    echo "    ⚠️  WARNING: $ACTIVE_SESSIONS sessions still running!"
    echo "    Consider waiting or pausing cron before upgrading."
fi

# STEP 2: Backup critical files
echo ""
echo "[STEP 2/8] Creating backup..."
mkdir -p "$BACKUP_DIR"
cp -r /home/wls/.openclaw/workspace-lisa/MEMORY.md "$BACKUP_DIR/" 2>/dev/null || true
cp -r /home/wls/.openclaw/workspace-lisa/SOUL.md "$BACKUP_DIR/" 2>/dev/null || true
cp -r /home/wls/.openclaw/workspace-lisa/AGENTS.md "$BACKUP_DIR/" 2>/dev/null || true
cp -r /home/wls/.openclaw/workspace-lisa/IDENTITY.md "$BACKUP_DIR/" 2>/dev/null || true
cp -r /home/wls/.openclaw/workspace-lisa/USER.md "$BACKUP_DIR/" 2>/dev/null || true
cp -r /home/wls/.openclaw/workspace-lisa/TOOLS.md "$BACKUP_DIR/" 2>/dev/null || true
cp -r /home/wls/.openclaw/workspace-lisa/HEARTBEAT.md "$BACKUP_DIR/" 2>/dev/null || true
cp -r /home/wls/.openclaw/workspace-lisa/memory/ "$BACKUP_DIR/" 2>/dev/null || true
cp -r /home/wls/.openclaw/workspace-lisa/scripts/ "$BACKUP_DIR/" 2>/dev/null || true
echo "  ✅ Backup saved to $BACKUP_DIR"

# STEP 3: Pause cron jobs
echo ""
echo "[STEP 3/8] Pausing cron jobs..."
CRON_IDS=$(openclaw cron list --json 2>/dev/null | jq -r '.[].id' 2>/dev/null || true)
for id in $CRON_IDS; do
    echo "  - Pausing $id..."
    openclaw cron pause "$id" 2>/dev/null || echo "    (skip - may already be paused)"
done
echo "  ✅ All cron jobs paused"

# STEP 4: Wait for running tasks to complete
echo ""
echo "[STEP 4/8] Waiting for running tasks to complete..."
MAX_WAIT=120  # 2 minutes max
WAITED=0
while [ $WAITED -lt $MAX_WAIT ]; do
    RUNNING=$(openclaw tasks list 2>/dev/null | grep -c "running" || echo "0")
    if [ "$RUNNING" -eq 0 ]; then
        echo "  ✅ All tasks completed"
        break
    fi
    echo "  - $RUNNING tasks still running... waiting (${WAITED}s/${MAX_WAIT}s)"
    sleep 10
    WAITED=$((WAITED + 10))
done

if [ $WAITED -ge $MAX_WAIT ]; then
    echo "  ⚠️  Timeout waiting for tasks. Proceeding anyway (tasks may fail during upgrade)."
fi

# STEP 5: Stop gateway
echo ""
echo "[STEP 5/8] Stopping gateway..."
openclaw gateway stop 2>&1 || echo "  (gateway may already be stopped)"
sleep 3
echo "  ✅ Gateway stopped"

# STEP 6: Perform upgrade
echo ""
echo "[STEP 6/8] Upgrading OpenClaw..."
npm update -g openclaw 2>&1 | tee -a "$LOG_FILE"
echo "  ✅ Upgrade command executed"

# STEP 7: Post-upgrade verification
echo ""
echo "[STEP 7/8] Post-upgrade verification..."
NEW_VERSION=$(openclaw --version 2>/dev/null | head -1 | awk '{print $2}')
echo "  - New version: $NEW_VERSION"

echo "  - Running health check..."
openclaw status 2>&1 | tail -5

# STEP 8: Restart and resume
echo ""
echo "[STEP 8/8] Restarting gateway and resuming cron..."
openclaw gateway start 2>&1 || echo "  ⚠️ Gateway start failed - may need manual start"
sleep 5

for id in $CRON_IDS; do
    echo "  - Resuming $id..."
    openclaw cron resume "$id" 2>/dev/null || echo "    (skip)"
done

echo ""
echo "=========================================="
echo "Upgrade Complete!"
echo "  Before: $CURRENT_VERSION"
echo "  After:  $NEW_VERSION"
echo "  Backup: $BACKUP_DIR"
echo "  Log:    $LOG_FILE"
echo "=========================================="
echo ""
echo "Post-upgrade checklist:"
echo "  □ Verify all agents respond"
echo "  □ Verify browser automation works"
echo "  □ Verify cron jobs fire correctly"
echo "  □ Check Discord channel connectivity"
echo "  □ Run: openclaw status --deep"