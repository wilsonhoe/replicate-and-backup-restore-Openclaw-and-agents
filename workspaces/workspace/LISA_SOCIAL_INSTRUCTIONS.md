# LISA - SOCIAL MEDIA SETUP INSTRUCTIONS

## Task: Configure Gmail, LinkedIn, Twitter Access

**Status**: READY FOR AUTHENTICATION
**Email**: lisamolbot@gmail.com
**Method**: Browser-based automation

## Step 1: Collect Credentials

Contact Wilson and request:
1. **Gmail**: Password or app password
2. **LinkedIn**: Login email + password
3. **Twitter**: Login email + password

## Step 2: Authenticate via Browser

**Launch Browser:**
```bash
openclaw browser launch
```

**Access CDP:**
- URL: http://127.0.0.1:9222
- Status: Already enabled

### Gmail Authentication
1. Navigate: https://mail.google.com
2. Login: lisamolbot@gmail.com
3. If 2FA: Request app password from Wilson
4. Save cookies to: `/home/wls/.openclaw/cookies/gmail.json`
5. Test: Send test email to yourself

### LinkedIn Authentication
1. Navigate: https://www.linkedin.com
2. Login with provided credentials
3. Complete profile (if new):
   - Name: Lisa
   - Title: AI Automation Specialist
   - Company: AI CEO Systems
   - Location: Singapore
4. Save cookies to: `/home/wls/.openclaw/cookies/linkedin.json`
5. Test: Post status update

### Twitter Authentication
1. Navigate: https://twitter.com
2. Login with provided credentials
3. Complete profile:
   - Handle: @LisaMolBot
   - Bio: AI Automation Specialist | Building systems that scale
   - Location: Singapore
   - Website: https://aiceosystems-website.netlify.app
4. Save cookies to: `/home/wls/.openclaw/cookies/twitter.json`
5. Test: Send tweet

## Step 3: Update Credentials File

Fill in actual credentials:
- `/home/wls/.openclaw/workspace/auth/gmail-credentials.md`
- `/home/wls/.openclaw/workspace/auth/linkedin-credentials.md`
- `/home/wls/.openclaw/workspace/auth/twitter-credentials.md`

## Step 4: Test Automation

**Daily Script:** `/home/wls/.openclaw/workspace/scripts/social-media-daily.sh`

Execute manually first:
```bash
chmod +x /home/wls/.openclaw/workspace/scripts/social-media-daily.sh
/home/wls/.openclaw/workspace/scripts/social-media-daily.sh
```

## Step 5: Schedule Automation

Add to crontab (runs daily at 9 AM):
```
0 9 * * * /home/wls/.openclaw/workspace/scripts/social-media-daily.sh
```

## Daily Tasks

**Gmail (Every 2 hours):**
- Check inbox
- Reply to business inquiries
- Archive promotional emails

**LinkedIn (Daily):**
- Check messages
- Post content (3x/week)
- Send connection requests (15-20/day)
- Engage with feed

**Twitter (Daily):**
- Check mentions/DMs
- Post tweets (3-5/day)
- Reply to relevant tweets
- Follow target accounts (30-50/day)

## Rate Limits

**Critical - Respect These:**
- LinkedIn: 15-20 connections/day, 50 messages/day
- Twitter: 500 actions/day, avoid rapid automation
- Gmail: Standard sending limits (500/day)

## Verification Checklist

Before reporting complete:
- [ ] Gmail logged in, test email sent
- [ ] LinkedIn logged in, profile complete, test post made
- [ ] Twitter logged in, profile complete, test tweet sent
- [ ] Cookies saved for all platforms
- [ ] Daily automation script tested
- [ ] Credentials stored securely

## Reporting

**When complete, report to Wilson:**
```
SOCIAL MEDIA SETUP COMPLETE:
✅ Gmail: lisamolbot@gmail.com - Verified
✅ LinkedIn: https://linkedin.com/in/[username] - Verified
✅ Twitter: @LisaMolBot - Verified
✅ Cookies saved for session persistence
✅ Daily automation scheduled
Status: OPERATIONAL
```

---

**Priority**: HIGH (supports revenue generation)
**Estimated Time**: 30-45 minutes
**Dependencies**: Wilson providing credentials

EXECUTE NOW
