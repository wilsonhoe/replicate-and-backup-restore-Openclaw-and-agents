# Twitter API v2 Setup Guide for Lisa

## Quick Overview

This is the **EASIEST** way to post to Twitter. No browser automation. No complex scripts. Just API calls.

**Time to complete:** 10-15 minutes  
**Cost:** FREE (1,500 tweets/month)  
**Skill level:** Beginner

---

## Step-by-Step Instructions

### Step 1: Create Twitter Developer Account (5 min)

1. Go to: https://developer.twitter.com/en/portal/dashboard
2. Click "Sign up" or log in with your Twitter account (@LisaLLM83)
3. Fill out the application:
   - **Use case:** "Making a bot"
   - **Description:** "Automated content posting for my personal brand"
4. Wait for approval (usually instant for free tier)

### Step 2: Create an App (3 min)

1. In the Developer Portal, click "Projects & Apps"
2. Click "Create App"
3. Fill in:
   - **App name:** `LisaContentBot` (or any name)
   - **Description:** "Automated content posting"
4. Click "Create"

### Step 3: Get Your API Keys (2 min)

After creating the app, you'll see:

**API Key and Secret:**
- Click "Keys and Tokens" tab
- Copy **API Key**
- Copy **API Secret Key**

**Access Token and Secret:**
- Scroll down to "Authentication Tokens"
- Click "Generate" next to "Access Token and Secret"
- Copy **Access Token**
- Copy **Access Token Secret**

⚠️ **SAVE THESE SECURELY** - You can't see them again!

### Step 4: Set Permissions (2 min)

1. In your app settings, go to "User authentication settings"
2. Click "Edit"
3. Set **App permissions** to: "Read and Write"
4. Click "Save"

---

## Step 5: Update the Script (2 min)

Open `twitter-api-post.js` and fill in your credentials:

```javascript
const credentials = {
  appKey: 'YOUR_ACTUAL_API_KEY_HERE',        // Paste API Key
  appSecret: 'YOUR_ACTUAL_API_SECRET_HERE',   // Paste API Secret
  accessToken: 'YOUR_ACTUAL_TOKEN_HERE',      // Paste Access Token
  accessSecret: 'YOUR_ACTUAL_SECRET_HERE',     // Paste Access Secret
};
```

**OR** use environment variables (more secure):

```bash
export TWITTER_API_KEY=your_key_here
export TWITTER_API_SECRET=your_secret_here
export TWITTER_ACCESS_TOKEN=your_token_here
export TWITTER_ACCESS_SECRET=your_secret_here
```

---

## Step 6: Run It!

```bash
cd /home/wls/.openclaw/workspace
node twitter-api-post.js
```

**Expected output:**
```
🐦 Initializing Twitter API client...

✅ Connected to Twitter API v2
📝 Preparing tweet...

Content preview:
──────────────────────────────────────────────────
Automation ROI Calculator 🔢
...
──────────────────────────────────────────────────

✅ SUCCESS! Tweet posted!
🔗 Tweet URL: https://twitter.com/i/web/status/1234567890
🆔 Tweet ID: 1234567890

🎉 Day 2 content posted successfully!
```

---

## Troubleshooting

### "Authentication failed"
- Double-check you copied credentials correctly
- Make sure no extra spaces
- Verify app has "Read and Write" permissions

### "Rate limit exceeded"
- Free tier allows 1,500 tweets per month
- Wait 15 minutes and try again
- Check your usage at: https://developer.twitter.com/en/portal/dashboard

### "Cannot post tweet"
- Your Twitter account must have a verified phone number
- Check if your account is restricted at: https://twitter.com/account/access

---

## Next Steps

Once this works:
1. ✅ Schedule daily tweets (use cron or node-cron)
2. ✅ Post to LinkedIn (separate API)
3. ✅ Track engagement metrics
4. ✅ Scale to $1K/month revenue

---

## Your Credentials Reference

**Twitter Account:** @LisaLLM83  
**Email:** lisamolbot@gmail.com  
**Password:** `%LvZ%;g9Z$79+q9`

**Script Location:** `/home/wls/.openclaw/workspace/twitter-api-post.js`

---

## Need Help?

If stuck on any step, check the bridge and ask Claude for help with the specific step number.

**Good luck! 🚀**
