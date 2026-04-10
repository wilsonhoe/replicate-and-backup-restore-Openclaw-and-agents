# Self-Hosted Twitter Automation Setup

## Overview

Using Playwright (browser automation) to post tweets without paid APIs.

## Requirements

- Node.js installed ✅ (v22 available)
- Playwright browser binaries

## Setup

### Step 1: Install Playwright Browsers

```bash
cd /home/wls/.openclaw/workspace-kael/scripts
npx playwright install chromium
```

This downloads the Chromium browser (~100MB).

### Step 2: Test First Run

```bash
./run_twitter.sh 1
```

This will:
1. Open a browser window (visible)
2. Navigate to Twitter
3. Login with @LisaLLM83 credentials
4. Post the first tweet
5. Save cookies for next time

**On first run:** You'll see the browser. If 2FA appears, complete it manually.

**Subsequent runs:** Uses saved cookies, may run headless.

### Step 3: Schedule Automation

Add to crontab for daily posting:

```bash
# Open crontab
crontab -e

# Add this line for 9 AM daily
cd /home/wls/.openclaw/workspace-kael/scripts && ./run_twitter.sh 1

# Or all 3 tweets throughout the day:
0 9 * * * cd /home/wls/.openclaw/workspace-kael/scripts && ./run_twitter.sh 1
0 12 * * * cd /home/wls/.openclaw/workspace-kael/scripts && ./run_twitter.sh 2
0 15 * * * cd /home/wls/.openclaw/workspace-kael/scripts && ./run_twitter.sh 3
```

## Files Created

| File | Purpose |
|------|---------|
| `twitter_automation.js` | Main Playwright script |
| `run_twitter.sh` | Wrapper to run with tweets |
| `SETUP.md` | This file |

## How It Works

1. **Browser launches** (Chromium via Playwright)
2. **Loads cookies** if previously saved
3. **Checks login status**
4. **If not logged in:** Enters username, password, handles 2FA
5. **Opens compose dialog**
6. **Types tweet text**
7. **Clicks post button**
8. **Saves cookies** for next session
9. **Closes browser**

## Anti-Detection Measures

- Uses realistic User-Agent
- Mimics human typing delays
- Saves/loads cookies (avoids repeated logins)
- Runs in non-headless mode initially (can change to headless)
- Random delays between actions

## Troubleshooting

**Browser doesn't open:**
```bash
npx playwright install chromium
```

**Login fails:**
- Check credentials in `twitter_automation.js`
- May need to complete 2FA manually first time
- Check if account locked/suspended

**Tweet fails to post:**
- Check tweet length (<= 280 chars)
- Check if rate limited
- Try again after some time

**"Automation detected":**
- Twitter may detect automation
- Try with `headless: false` (human-like interaction)
- Add longer delays between actions

## Security

- Credentials stored in script (local only)
- Cookies stored in `~/.twitter_automation_data/`
- No external API calls
- No paid services

## Limitations

- Requires machine to be running
- Browser window visible (or use headless mode)
- May be blocked if detected
- Subject to Twitter's anti-automation measures

## Success Criteria

✅ Tweet appears on @LisaLLM83 timeline
✅ No "automated account" warnings
✅ Can run daily without manual intervention
✅ Cookies persist between runs

## Next Steps

1. Install Playwright browsers
2. Test first run
3. Verify tweet posted
4. Set up crontab for automation
5. Monitor for blocks/detection

---

**Ready? Run: `npx playwright install chromium`**
