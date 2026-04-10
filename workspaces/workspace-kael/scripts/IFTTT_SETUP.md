# IFTTT Twitter Automation Setup Guide

## Overview

Use IFTTT (If This Then That) to post tweets via webhook. Free tier: 5 applets.

---

## Step 1: Create IFTTT Account

1. Go to https://ifttt.com/
2. Sign up with **lisamolbot@gmail.com**
3. Verify email

---

## Step 2: Create Applet

1. Go to https://ifttt.com/create
2. Click **"If This"**
3. Search for **"Webhooks"**
4. Click **"Webhooks"** service
5. Choose **"Receive a web request"**
6. Enter event name: `lisa_daily_tweet`
7. Click **Create trigger**

---

## Step 3: Configure Twitter Action

1. Click **"Then That"**
2. Search for **"Twitter"**
3. Click **"Twitter"** service
4. Choose **"Post a tweet"**
5. Connect your **@LisaLLM83** Twitter account
6. In tweet text field, enter: `{{Value1}}`
   - This will use the webhook payload
7. Click **Create action**
8. Click **Continue**
9. Click **Finish**

---

## Step 4: Get Webhook URL

1. Go to https://ifttt.com/maker_webhooks
2. Click **Documentation**
3. You'll see your webhook URL format:
   ```
   https://maker.ifttt.com/trigger/lisa_daily_tweet/with/key/YOUR_KEY_HERE
   ```
4. Copy the full URL with your key

---

## Step 5: Test Webhook

Run this curl command (replace with your actual URL):

```bash
curl -X POST \
  https://maker.ifttt.com/trigger/lisa_daily_tweet/with/key/YOUR_KEY_HERE \
  -H "Content-Type: application/json" \
  -d '{"value1": "Test tweet from IFTTT webhook #AI #Automation"}'
```

**Expected result:** Tweet posts to @LisaLLM83

---

## Step 6: Update Automation

Once webhook works, give me the URL and I'll update the cron job.

---

## Data Format for Webhook

IFTTT expects this JSON:
```json
{
  "value1": "Your tweet text here #AI #Automation",
  "value2": "optional",
  "value3": "optional"
}
```

Only `value1` is used for tweet text.

---

## Important Notes

- **Rate limit:** 5 applets on free plan (we use 1)
- **Twitter connection:** Must authorize @LisaLLM83
- **Webhook delay:** Usually instant, can take 1-2 minutes
- **Character limit:** 280 characters (Twitter enforces this)

---

## Troubleshooting

**Webhook not working?**
1. Check applet is ON (toggle green)
2. Verify Twitter account connected
3. Test with simple text first
4. Check IFTTT activity log

**Tweet not posting?**
1. Check @LisaLLM83 has posting permissions
2. Verify no 2FA blocking IFTTT
3. Check Twitter developer settings

---

## Next Steps

1. Create IFTTT account
2. Create applet with webhook → Twitter
3. Get webhook URL
4. Paste URL here
5. I update automation to use it

**Ready to start?**
