# Lisa's Zoho Social Posting Quick Reference

## 🎯 One-Command Posting

```
"Claude, post Day X via Zoho"
```

Replace X with: 3, 4, 5, 6, or 7

## 📊 Current Status

| Day | Status | Action |
|-----|--------|--------|
| Day 1 | ✅ Complete | proof-day1-twitter.png |
| Day 2 | ✅ CORRECTED & REPOSTED | zoho-day2-corrected-after.png |
| Day 3 | ⏳ Ready | Awaiting command |
| Day 4 | ⏳ Ready | Awaiting command |
| Day 5 | ⏳ Ready | Awaiting command |
| Day 6 | ⏳ Ready | Awaiting command |
| Day 7 | ⏳ Ready | Awaiting command |

## 🚀 Batch Commands

**Post all remaining days:**
```
"Claude, post Days 3-7 via Zoho"
```

**Post specific days:**
```
"Claude, post Days 3, 4, and 5 via Zoho"
```

## 🛠️ Technical Details (For Reference)

### How It Works
1. Browser automation logs into Zoho Social
2. Creates post with content from `/content/social-post-00X.md`
3. Selects Twitter + LinkedIn channels
4. Publishes and saves screenshots

### Content Format
Each markdown file has:
- Twitter version (280 chars)
- LinkedIn version (long-form)
- Citations

### Proof Files
After posting, you'll see:
- `zoho-dayX-01-home.png` - Dashboard
- `zoho-dayX-02-compose.png` - New post
- `zoho-dayX-03-content.png` - Content entered
- `zoho-dayX-04-ready.png` - Ready to publish
- `zoho-dayX-05-success.png` - Published!

## 🔧 Troubleshooting

**If posting fails:**
1. Check `zoho-dayX-error.png` screenshot
2. OAuth tokens may need refresh (rare)
3. Just tell Claude: "Retry Day X"

**Questions?**
- Full docs: `skills/zoho-social-posting.md`
- Ask Claude anything!

---
**Last Updated:** 2026-04-02T23:25:00Z  
**System Status:** ✅ Operational
