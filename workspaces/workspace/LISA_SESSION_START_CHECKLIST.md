# Lisa Session Start Checklist

**⚠️ READ THIS FIRST - EVERY TIME ⚠️**

## Step 1: Check Bridge (30 seconds)

Read: `/home/wls/bridge/CLAUDE_TO_LISA.md`
- What did Claude last tell me?
- What was the last action?

## Step 2: Check Memory (30 seconds)

Read: `/home/wls/.openclaw/workspace/skills/lisa-memory-system.md`
- What's the current status?
- What works / what doesn't?

## Step 3: Verify Proof (30 seconds)

Run:
```bash
ls -la /home/wls/.openclaw/workspace/zoho-day*.png /home/wls/.openclaw/workspace/proof-day*.png 2>/dev/null
```

## Step 4: Current Status (as of 2026-04-03)

| Day | Status | Proof |
|-----|--------|-------|
| 1 | ✅ DONE | proof-day1-twitter.png |
| 2 | ✅ DONE | zoho-day2-05-success.png |
| 3 | ✅ DONE | zoho-day3-05-success.png |
| 4 | ⏳ NEXT | Say "Post Day 4 via Zoho" |
| 5 | ⏳ WAITING | Content ready |
| 6 | ⏳ WAITING | Content ready |
| 7 | ⏳ WAITING | Content ready |

## Step 5: What Works

**Posting Method:** Zoho Social browser automation
**Magic Phrase:** "Post Day X via Zoho"
**What NOT to use:** Twitter API (has verification challenges)

## Step 6: If You Think There's a Blocker

**STOP.** Check these first:
1. Was it already solved? (read memory files)
2. Is there proof it works? (check screenshots)
3. Did Claude already fix it? (read bridge)

**Common False Blockers:**
- ❌ "Twitter API verification" - WE USE ZOHO, NOT API
- ❌ "Need cookie import" - WE USE ZOHO BROWSER
- ❌ "Need manual posting" - ZOHO AUTO-POSTS

## Quick Commands

**Check current status:**
```bash
bash /home/wls/.openclaw/workspace/monitor-lisa-progress.sh
```

**See all skills:**
```bash
ls /home/wls/.openclaw/workspace/skills/
```

**See memory files:**
```bash
ls /home/wls/.claude/projects/-home-wls/memory/
```

---

**Remember: VERIFY BEFORE CLAIMING. READ BEFORE ACTING.**
