# Browser-Based Social Media Access for Lisa

## Overview
Lisa will access LinkedIn and Twitter via OpenClaw's browser capabilities.

## Browser Configuration

**Current Status:**
- CDP URL: http://127.0.0.1:9222
- Status: ✅ Enabled
- Profile: user

## Platform Access

### 1. Gmail (lisamolbot@gmail.com)

**Access Method:** Browser or IMAP/SMTP
**Setup Required:**
- App password needed (2FA enabled Gmail)
- Or: Browser cookie-based login

**Instructions for Lisa:**
1. Open browser to https://mail.google.com
2. Login with: lisamolbot@gmail.com
3. If 2FA: Use app password or backup codes
4. Save session cookies for future access

### 2. LinkedIn

**Access Method:** Browser automation
**URL:** https://www.linkedin.com

**Lisa's Actions:**
1. Navigate to LinkedIn login
2. Login with provided credentials
3. Complete profile if new account
4. Enable messaging and posting capabilities

**Capabilities:**
- ✅ Post updates
- ✅ Send connection requests
- ✅ Send messages
- ✅ Browse feed
- ✅ Search profiles

### 3. Twitter/X

**Access Method:** Browser automation
**URL:** https://twitter.com or https://x.com

**Lisa's Actions:**
1. Navigate to Twitter login
2. Login with provided credentials
3. Complete profile setup
4. Enable tweeting and DM capabilities

**Capabilities:**
- ✅ Post tweets
- ✅ Send DMs
- ✅ Reply to tweets
- ✅ Follow/unfollow
- ✅ Browse timeline

## Authentication Management

### Cookie Persistence
Lisa should save cookies after login:
```javascript
// Save cookies to file
const cookies = await page.cookies();
fs.writeFileSync('/home/wls/.openclaw/cookies/linkedin.json', JSON.stringify(cookies));
```

### Session Restoration
```javascript
// Load cookies on next session
const cookies = JSON.parse(fs.readFileSync('/home/wls/.openclaw/cookies/linkedin.json'));
await page.setCookie(...cookies);
```

## Security Considerations

1. **Private Data**: Store credentials in auth-profiles.json, never hardcoded
2. **Session Timeout**: Re-authenticate if session expires
3. **Rate Limiting**: Respect platform limits (LinkedIn ~100 connections/day, Twitter ~500 actions/day)
4. **Human-like Behavior**: Add delays between actions

## Usage Patterns

### LinkedIn Daily Tasks
- Morning: Check messages (9 AM)
- Post content: 3x per week
- Connection requests: 10-20/day
- Engagement: Reply to comments

### Twitter Daily Tasks
- Check mentions and DMs
- Post threads: 1-2x per day
- Reply to relevant tweets
- Follow target accounts: 20-50/day

### Gmail Daily Tasks
- Check inbox: Every 2 hours
- Priority: Business inquiries, partnership requests
- Auto-archive: Promotions, newsletters

## Credentials Storage

**Location:** `/home/wls/.openclaw/workspace/auth/`

**Files:**
- `gmail-credentials.md` - Gmail login info
- `linkedin-credentials.md` - LinkedIn login info
- `twitter-credentials.md` - Twitter login info

**Format:**
```markdown
# Platform Credentials
Username: [value]
Password: [value or reference to secure storage]
2FA Method: [app/sms/backup codes]
Recovery: [recovery email/phone]
```

## Browser Commands for Lisa

### Launch Browser
```bash
openclaw browser launch
```

### Navigate to Platform
```bash
openclaw browser navigate --url https://linkedin.com
```

### Execute Action
```bash
openclaw browser execute --script "login-script.js"
```

## Monitoring

Lisa should report:
- Login status (success/failure)
- Session health
- Rate limit warnings
- New messages/notifications count

## Troubleshooting

**Browser not connecting:**
- Check if Chrome/Chromium is running with remote debugging
- Verify port 9222 is accessible
- Restart browser: `openclaw browser restart`

**Login failures:**
- Check credentials
- Verify 2FA not blocking
- Check for CAPTCHA
- Review platform security alerts

**Session expired:**
- Re-authenticate manually
- Update cookies
- Check for platform security changes

---

**Status**: READY FOR SETUP
**Next Action**: Lisa to authenticate each platform
