#!/bin/bash
# Monitor Lisa's Social Media Posting Progress
# Run every 15 minutes via cron or manual check

echo "=== Lisa Progress Monitor ==="
echo "Timestamp: $(date)"
echo ""

# Check for Lisa's responses in bridge
echo "1. Checking bridge for Lisa messages..."
if grep -q "Lisa →" /home/wls/bridge/LISA_TO_CLAUDE.md 2>/dev/null; then
    echo "   ✅ Lisa has sent messages"
    grep "Lisa →" /home/wls/bridge/LISA_TO_CLAUDE.md | tail -3
else
    echo "   ❌ No messages from Lisa found"
fi
echo ""

# Check for video files created by Lisa
echo "2. Checking for video files..."
VIDEOS=$(find /home/wls/.openclaw/workspace -name "day*.mp4" -o -name "day*-video*" 2>/dev/null)
if [ -n "$VIDEOS" ]; then
    echo "   ✅ Video files found:"
    echo "$VIDEOS" | while read file; do
        echo "      - $(basename "$file") ($(stat -c %y "$file" | cut -d' ' -f1))"
    done
else
    echo "   ❌ No video files found"
fi
echo ""

# Check for proof screenshots
echo "3. Checking for proof screenshots..."
PROOF=$(find /home/wls/.openclaw/workspace -name "*day*proof*" -o -name "*lisa*proof*" 2>/dev/null)
if [ -n "$PROOF" ]; then
    echo "   ✅ Proof files found:"
    echo "$PROOF" | while read file; do
        echo "      - $(basename "$file")"
    done
else
    echo "   ❌ No proof screenshots found"
fi
echo ""

# Check days completed
echo "4. Days completion status:"
for day in 3 4 5 6 7; do
    if [ -f "/home/wls/.openclaw/workspace/day${day}-video.mp4" ] || [ -f "/home/wls/.openclaw/workspace/day${day}-final.mp4" ]; then
        echo "   Day $day: ✅ Video created"
    else
        echo "   Day $day: ⏳ Pending"
    fi
done
echo ""

# Check last activity time
echo "5. Activity timeline:"
echo "   Bridge last modified: $(stat -c %y /home/wls/bridge/LISA_TO_CLAUDE.md 2>/dev/null | cut -d' ' -f1,2 | cut -d'.' -f1)"
echo "   Skill doc last modified: $(stat -c %y /home/wls/.openclaw/workspace/skills/lisa-social-video-posting.md 2>/dev/null | cut -d' ' -f1,2 | cut -d'.' -f1)"
echo ""

# Alert if no activity for >6 hours
echo "6. Checking for stale activity..."
LAST_BRIDGE=$(stat -c %Y /home/wls/bridge/LISA_TO_CLAUDE.md 2>/dev/null)
NOW=$(date +%s)
DIFF=$(( (NOW - LAST_BRIDGE) / 3600 ))

if [ $DIFF -gt 6 ]; then
    echo "   ⚠️  ALERT: No bridge activity for $DIFF hours"
    echo "   📱 RECOMMENDATION: Ping Wilson on Telegram"
else
    echo "   ✅ Bridge activity within last $DIFF hours"
fi

echo ""
echo "=== End of Report ==="
