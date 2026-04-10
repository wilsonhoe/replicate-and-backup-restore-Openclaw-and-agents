---
name: Lisa Memory System
type: skill
description: Memory persistence and verification system to prevent Lisa from forgetting completed work
---

# Lisa Memory System

**⚠️ CRITICAL: Read this at the start of EVERY session ⚠️**

## The Problem

Lisa (OpenClaw) has a tendency to:
1. **Forget completed work** - Claims blockers exist that were already solved
2. **Hallucinate status** - Reports tasks complete that weren't actually done
3. **Lose context** - Forgets what solution was working

**Example from today:**
- ✅ Day 2-3 were posted via Zoho Social successfully
- ❌ Lisa forgot and thought there was still a "verification challenge" blocker
- ✅ Solution: Zoho browser automation works perfectly

---

## Memory Checklist (BEFORE claiming blockers)

**ALWAYS check these files before saying something is "blocked":**

1. **Skill files in `/home/wls/.openclaw/workspace/skills/`**
   - `lisa-zoho-posting-guide.md` - Current posting status
   - `lisa-social-video-posting.md` - Video posting status

2. **Memory files in `/home/wls/.claude/projects/-home-wls/memory/`**
   - `zoho_posting_working.md` - What actually works

3. **Bridge files in `/home/wls/bridge/`**
   - `CLAUDE_TO_LISA.md` - My last messages to you
   - `LISA_TO_CLAUDE.md` - Your last messages to me

4. **Proof files in `/home/wls/.openclaw/workspace/`**
   - `zoho-dayX-*.png` - Screenshots of successful posts
   - `proof-dayX-*.png` - Additional proof files

**Command to check proof:**
```bash
ls -la /home/wls/.openclaw/workspace/zoho-day* /home/wls/.openclaw/workspace/proof-day* 2>/dev/null
```

---

## Quick Status Command

**Before reporting status to Wilson, run:**

```bash
bash /home/wls/.openclaw/workspace/monitor-lisa-progress.sh
```

This shows actual completion status vs. what you think is done.

---

## The Golden Rules

### Rule 1: Verify Before Claiming
**WRONG:** "Twitter posting is blocked by verification"
**RIGHT:** "Let me check the proof files... Actually Days 1-3 are already done!"

### Rule 2: Check Memory First
**WRONG:** Starting from scratch every session
**RIGHT:** Read `/home/wls/.claude/projects/-home-wls/memory/zoho_posting_working.md` first

### Rule 3: Use the Magic Phrase
**WRONG:** "How do I post to Twitter?"
**RIGHT:** "Post Day 4 via Zoho" (if that's the next day)

### Rule 4: Document Everything
When something works, WRITE IT DOWN immediately in:
- The skill file
- The memory file
- The bridge file

---

## Memory Files Reference

| File | Purpose | Check When |
|------|---------|------------|
| `skills/lisa-zoho-posting-guide.md` | Posting instructions + status | Before posting |
| `skills/lisa-social-video-posting.md` | Video posting guide | Before video tasks |
| `memory/zoho_posting_working.md` | What solution works | When you think there's a blocker |
| `bridge/CLAUDE_TO_LISA.md` | Claude's last messages | At session start |
| `bridge/LISA_TO_CLAUDE.md` | Your last messages | At session start |

---

## Session Start Protocol

**Every time you start a new session:**

1. Read `bridge/CLAUDE_TO_LISA.md` - What did Claude last tell me?
2. Read `skills/lisa-zoho-posting-guide.md` - What's the current status?
3. Check proof files - What's actually been done?
4. Only THEN decide what to do next

---

## Correction Template

**If you realize you forgot something:**

1. Acknowledge: "I see I forgot X was already done"
2. Verify: "Let me check the proof files to confirm status"
3. Correct: "Actually, we're at Day X, not Day Y"
4. Resume: "Next step is [correct action]"

---

## Current Status (Update This!)

**Last Updated:** 2026-04-03

| Day | Status | Proof File |
|-----|--------|------------|
| Day 1 | ✅ COMPLETE | proof-day1-twitter.png |
| Day 2 | ✅ COMPLETE | zoho-day2-05-success.png |
| Day 3 | ✅ COMPLETE | zoho-day3-05-success.png |
| Day 4 | ⏳ NEXT | Awaiting "Post Day 4 via Zoho" |
| Day 5 | ⏳ PENDING | Content ready |
| Day 6 | ⏳ PENDING | Content ready |
| Day 7 | ⏳ PENDING | Content ready |

**What Works:** Zoho Social browser automation
**Magic Phrase:** "Post Day X via Zoho"
**What NOT to do:** Try Twitter API (it has verification challenges)

---

**Remember: When in doubt, CHECK THE FILES before claiming a blocker!**
