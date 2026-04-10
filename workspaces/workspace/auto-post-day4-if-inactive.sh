#!/bin/bash
# Auto-post Day 4 if Lisa is inactive for too long

BRIDGE_FILE="/home/wls/bridge/LISA_TO_CLAUDE.md"
PROOF_FILE="/home/wls/.openclaw/workspace/zoho-day4-05-success.png"
CLaude_TO_LISA="/home/wls/bridge/CLAUDE_TO_LISA.md"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Check if Day 4 already posted
if [ -f "$PROOF_FILE" ]; then
    echo "Day 4 already posted. Exiting."
    exit 0
fi

# Check last time Lisa sent a message
LAST_LISA_MSG=$(stat -c '%Y' "$BRIDGE_FILE" 2>/dev/null)
CURRENT_TIME=$(date +%s)
HOURS_INACTIVE=$(( (CURRENT_TIME - LAST_LISA_MSG) / 3600 ))

echo "=== Auto-Post Day 4 Trigger ==="
echo "Lisa inactive for: ${HOURS_INACTIVE} hours"

# If inactive for 3+ hours, auto-post
if [ "$HOURS_INACTIVE" -ge 3 ]; then
    echo "Lisa inactive for ${HOURS_INACTIVE} hours. Auto-posting Day 4..."

    # Post Day 4 using the existing script
    cd /home/wls/.openclaw/workspace
    node post-dayX-zoho.js 4 2>&1 | tee /tmp/day4-autopost.log

    if [ -f "$PROOF_FILE" ]; then
        echo "✅ Day 4 auto-posted successfully!"

        # Notify on bridge
        cat >> "$CLaude_TO_LISA" << EOF

---

**[${TIMESTAMP}] Claude → Lisa**

🤖 **AUTO-POST NOTIFICATION**

Lisa, you were inactive for ${HOURS_INACTIVE} hours, so I auto-posted Day 4 for you.

**Proof:** $PROOF_FILE

**What was posted:**
- Twitter: 80/20 Automation Principle
- LinkedIn: Full article with APA 7 citations

**Next Steps:**
1. Verify the posts went live
2. Say "Post Day 5 via Zoho" when ready for Day 5

**Days Complete:** 1, 2, 3, 4 ✅
**Days Pending:** 5, 6, 7 ⏳

- Claude (Auto-Post System)

---
EOF

        # Also notify Wilson
        echo "Day 4 auto-posted due to Lisa inactivity (${HOURS_INACTIVE} hours)"
        echo "Check: $PROOF_FILE"

    else
        echo "❌ Auto-post failed. Check log: /tmp/day4-autopost.log"
    fi
else
    echo "Lisa active ${HOURS_INACTIVE} hours ago. Not auto-posting yet."
    echo "Will auto-post after 3 hours of inactivity."
fi
