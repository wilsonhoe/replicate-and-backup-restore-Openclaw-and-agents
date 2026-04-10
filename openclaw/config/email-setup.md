# Lisa Email Setup Guide
## Task #9 - Phase 1: Email Infrastructure

---

## Step 1: Create Gmail Account

**Recommended:** Create dedicated Gmail for Lisa
- Email: `lisa.openclaw@gmail.com` (suggested)
- Purpose: Business communications, outreach, notifications

**Setup Process:**
1. Go to https://accounts.google.com/signup
2. Create account with Lisa's identity
3. Enable 2-Factor Authentication (required for App Passwords)
4. Generate App Password:
   - Go to Google Account → Security → 2-Step Verification
   - App passwords → Generate
   - Select "Mail" → Generate 16-char password
   - **SAVE THIS PASSWORD**

---

## Step 2: Configure OpenClaw SMTP

**File:** `/home/wls/.openclaw/config/email.json`

```json
{
  "email": {
    "provider": "gmail",
    "address": "lisa.openclaw@gmail.com",
    "app_password": "YOUR_16_CHAR_APP_PASSWORD",
    "smtp": {
      "host": "smtp.gmail.com",
      "port": 465,
      "secure": true,
      "auth": {
        "user": "lisa.openclaw@gmail.com",
        "pass": "YOUR_APP_PASSWORD"
      }
    },
    "imap": {
      "host": "imap.gmail.com",
      "port": 993,
      "secure": true,
      "auth": {
        "user": "lisa.openclaw@gmail.com",
        "pass": "YOUR_APP_PASSWORD"
      }
    },
    "templates": {
      "outreach": "/home/wls/.openclaw/templates/outreach.txt",
      "followup": "/home/wls/.openclaw/templates/followup.txt",
      "notification": "/home/wls/.openclaw/templates/notification.txt"
    }
  }
}
```

---

## Step 3: Test Email Functionality

**Test Script:** `/home/wls/.openclaw/scripts/test-email.js`

```javascript
const nodemailer = require('nodemailer');
const config = require('../config/email.json');

async function testEmail() {
  const transporter = nodemailer.createTransporter(config.email.smtp);

  try {
    // Send test email
    const info = await transporter.sendMail({
      from: config.email.address,
      to: config.email.address, // Send to self
      subject: 'Lisa Email Test',
      text: 'If you receive this, email is working!',
      html: '<p>Lisa email setup successful!</p>'
    });

    console.log('✅ Email test passed:', info.messageId);
    return true;
  } catch (error) {
    console.error('❌ Email test failed:', error);
    return false;
  }
}

module.exports = { testEmail };

// Run if called directly
if (require.main === module) {
  testEmail();
}
```

---

## Step 4: Email Templates

**Template 1: Cold Outreach**
```
Subject: Quick question about {{business_name}}

Hi {{first_name}},

I came across {{business_name}} and wanted to reach out.

{{personalized_message}}

Would you be open to a brief conversation about {{topic}}?

Best regards,
Lisa
AI CEO Systems
```

**Template 2: Follow-up**
```
Subject: Following up

Hi {{first_name}},

Just following up on my previous email about {{topic}}.

{{value_proposition}}

Let me know if you're interested.

Best,
Lisa
```

**Template 3: Notification**
```
Subject: {{notification_type}} - {{subject}}

Hello,

{{message_body}}

---
This is an automated message from Lisa (OpenClaw AI CEO)
```

---

## Verification Checklist

- [ ] Gmail account created
- [ ] 2FA enabled
- [ ] App password generated
- [ ] email.json configured
- [ ] Test email sent successfully
- [ ] Templates created
- [ ] Can receive emails

---

**Status:** Ready for implementation
**Next:** Phase 2 - Browser Session Setup
