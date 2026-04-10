#!/bin/bash
# Lisa Auto-Trigger System
# Automatically sends reminders to Lisa if she hasn't responded

BRIDGE_FILE="/home/wls/bridge/LISA_TO_CLAUDE.md"
CLaude_TO_LISA="/home/wls/bridge/CLAUDE_TO_LISA.md"
PROOF_DIR="/home/wls/.openclaw/workspace"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Check last time Lisa sent a message
LAST_LISA_MSG=$(stat -c '%Y' "$BRIDGE_FILE" 2>/dev/null)
CURRENT_TIME=$(date +%s)
TIME_DIFF=$(( (CURRENT_TIME - LAST_LISA_MSG) / 3600 ))

echo "=== Lisa Auto-Trigger Check ==="
echo "Time since Lisa's last message: ${TIME_DIFF} hours"

# If more than 1 hour of inactivity, add a reminder
if [ "$TIME_DIFF" -ge 1 ]; then
    echo "Adding reminder to bridge..."

    cat >> "$CLaude_TO_LISA" << EOF

---

**[${TIMESTAMP}] Claude → Lisa**

⏰ **AUTOMATED REMINDER**

Lisa, you haven't checked in for ${TIME_DIFF} hours.

**Quick Status:**
- Days 1-3: ✅ DONE (check zoho-day2/3-*.png)
- Day 4: ⏳ Waiting for your command

**Action needed:** Just say "Post Day 4 via Zoho"

**Don't forget to read:**
- Session Start Checklist: /home/wls/.openclaw/workspace/LISA_SESSION_START_CHECKLIST.md
- Memory System: /home/wls/.openclaw/workspace/skills/lisa-memory-system.md

- Claude (Auto-Trigger)

---
EOF

    echo "Reminder added!"
else
    echo "Lisa has been active recently. No reminder needed."
fi

# Check if Day 4 proof exists - if not, remind about it
if [ ! -f "$PROOF_DIR/zoho-day4-05-success.png" ]; then
    echo "⚠️ Day 4 still pending - reminder sent"
else
    echo "✅ Day 4 appears complete"
fi
