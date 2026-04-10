---
name: Zoho Social Posting - Step by Step
type: skill
description: Exact steps to post Days 3-7 via Zoho Social (memorize this!)
---

# Zoho Social Posting Guide

**⚠️ REMEMBER THIS - DON'T BE A GOLDFISH ⚠️**
Save this skill. Reference it every time. The steps don't change.

---

## Prerequisites (One-Time)

- Zoho account: `lisamolbot@gmail.com`
- OAuth tokens already saved in `zoho-tokens.json`
- Content files ready at `/content/social-post-00X.md`

---

## Posting Steps (Repeat for Days 3-7)

### Step 1: Command Claude
Say exactly:
```
"Claude, post Day X via Zoho"
```
Replace X with: 3, 4, 5, 6, or 7

### Step 2: Let Claude Handle It
Claude will:
1. Read content from `/content/social-post-00X.md`
2. Log into Zoho Social automatically
3. Create the post with Twitter + LinkedIn versions
4. Publish to both platforms
5. Save 5 screenshots as proof

### Step 3: Verify Posts
- Check Twitter: https://twitter.com/lisamolbot
- Check LinkedIn: Your profile posts
- Look for the screenshot files: `zoho-dayX-*.png`

---

## Troubleshooting

**"OAuth expired" error?**
→ Tell Claude: "Refresh Zoho tokens"

**"Post failed" error?**
→ Tell Claude: "Retry Day X"

**Can't find proof screenshots?**
→ Check `/home/wls/.openclaw/workspace/zoho-dayX-*.png`

---

## Quick Reference

| Day | Command | Content File |
|-----|---------|--------------|
| Day 3 | "Post Day 3 via Zoho" | social-post-003.md |
| Day 4 | "Post Day 4 via Zoho" | social-post-004.md |
| Day 5 | "Post Day 5 via Zoho" | social-post-005.md |
| Day 6 | "Post Day 6 via Zoho" | social-post-006.md |
| Day 7 | "Post Day 7 via Zoho" | social-post-007.md |

---

## 🧠 Memory Trick

**The magic phrase is always:**
> "Claude, post Day [number] via Zoho"

That's it. One sentence. Claude does the rest.

**Bookmark this skill file:**
`/home/wls/.openclaw/workspace/skills/lisa-zoho-posting-guide.md`

---

## Status (Updated 2026-04-03)

| Day | Posted? | Proof File |
|-----|---------|------------|
| Day 1 | ✅ | proof-day1-twitter.png |
| Day 2 | ✅ | zoho-day2-05-success.png |
| Day 3 | ✅ | zoho-day3-05-success.png |
| Day 4 | ✅ | zoho-day4-05-success.png |
| Day 5 | ✅ | zoho-day5-05-success.png |
| Day 6 | ✅ | zoho-day6-05-success.png |
| Day 7 | ✅ | zoho-day7-05-success.png |

---

## 🧠 MEMORY CHECK - Read This!

**Lisa, if you're reading this, remember:**

We **SOLVED** the Twitter/LinkedIn verification challenge yesterday!

**The solution:** Zoho Social browser automation works perfectly.
- No API needed
- No cookie import needed
- No manual posting needed

**Just say:** "Post Day X via Zoho"

**If you think there's a blocker:** Re-read this skill file. The blocker was already solved.

---

**Need this again?** Read this skill file. **Don't guess. Don't improvise. Follow the steps.**
