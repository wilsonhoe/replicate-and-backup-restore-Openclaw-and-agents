# Social Media API Setup Guide

## 1. Twitter/X Developer API

### Step 1: Apply for Developer Access
1. Go to: https://developer.twitter.com/en/portal/petition/essential/basic-info
2. Log in with your Twitter account
3. Fill out the application:
   - **Use Case**: "I'm building automation tools for my business"
   - **Description**: "Automated posting and engagement for AI CEO systems"
   - **Country**: Singapore

### Step 2: Create Project & App
1. Once approved, go to: https://developer.twitter.com/en/portal/dashboard
2. Create a Project → Name: "LisaAI"
3. Create an App → Name: "lisamolbot-automation"
4. Get Keys:
   - API Key (Consumer Key)
   - API Key Secret (Consumer Secret)
   - Bearer Token

### Step 3: Get Access Tokens
1. Go to App Settings → Keys and Tokens
2. Generate Access Token & Secret
3. Save all 4 values:
   - API Key
   - API Key Secret
   - Access Token
   - Access Token Secret

### Step 4: Provide to Lisa
Give me these values:
```
TWITTER_API_KEY=xxx
TWITTER_API_SECRET=xxx
TWITTER_ACCESS_TOKEN=xxx
TWITTER_ACCESS_SECRET=xxx
```

---

## 2. LinkedIn API

### Option A: LinkedIn Developer Portal (Company Pages)
1. Go to: https://www.linkedin.com/developers/
2. Create App:
   - App Name: "LisaAI Systems"
   - Company: AI CEO Systems (or personal)
   - Privacy Policy: https://aiceosystems-website.netlify.app/privacy
3. Products: Request "Share on LinkedIn" and "Sign In with LinkedIn"
4. Wait for approval (1-3 days)

### Option B: Use Browser Automation (Recommended for Personal)
No API needed - use Puppeteer with saved Chrome profile.

### LinkedIn API Values Needed:
```
LINKEDIN_CLIENT_ID=xxx
LINKEDIN_CLIENT_SECRET=xxx
```

---

## 3. Alternative: Use OAuth2 Automation

If you prefer not to wait for API approval, I can:
1. Use browser automation with your saved Chrome profile
2. Schedule posts via cron jobs
3. Run headless for 24/7 operation

---

## Next Steps

**Tell me which approach you want:**
- **A**: Apply for Twitter API + LinkedIn API (requires waiting for approval)
- **B**: Set up browser automation now (works immediately with saved profile)
- **C**: Both - API for future + browser automation for now