# AI Agent Setup Toolkit
## Complete Implementation Guide

**Version:** 1.0  
**Date:** 2026-03-31  
**Status:** Complete

---

## Quick Start (5 Minutes)

```bash
# 1. Clone repository
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# 2. Install dependencies
npm install

# 3. Configure environment
cp .env.example .env
# Edit .env with your settings

# 4. Start the system
npm run start
```

---

## System Requirements

### Hardware
- CPU: 2+ cores
- RAM: 4+ GB
- Storage: 10+ GB
- Internet: Stable connection

### Software
- Node.js 18+
- Chrome/Chromium browser
- Git
- Ollama (for local LLM)

---

## Installation Steps

### Step 1: Install Node.js
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18
```

### Step 2: Install Chrome
```bash
# Ubuntu/Debian
sudo apt-get install chromium-browser

# macOS
brew install --cask google-chrome
```

### Step 3: Install Ollama
```bash
curl https://ollama.ai/install.sh | sh
ollama pull kimi-k2.5:cloud
```

### Step 4: Configure OpenClaw
```bash
git clone https://github.com/openclaw/openclaw.git ~/openclaw
cd ~/openclaw
npm install

cp .env.example .env
# Edit .env:
# - Set OLLAMA_HOST=http://localhost:11434
# - Set DEFAULT_MODEL=kimi-k2.5:cloud
# - Set CHROME_DEBUG_PORT=9222

npm run start
```

---

## Browser Automation Setup

### Start Chrome with Remote Debugging
```bash
chromium-browser \
  --remote-debugging-port=9222 \
  --no-first-run \
  --user-data-dir=/home/wls/.chrome-profile
```

### Session Persistence Code
```javascript
// Save session
const cookies = await page.cookies();
const localStorage = await page.evaluate(() => JSON.stringify(localStorage));
fs.writeFileSync('session.json', JSON.stringify({cookies, localStorage}));

// Load session
const session = JSON.parse(fs.readFileSync('session.json'));
await page.setCookie(...session.cookies);
```

---

## Email Integration

### Gmail Setup
1. Enable 2FA on Google Account
2. Generate App Password (Security → App passwords)
3. Configure OpenClaw:

```javascript
const transporter = nodemailer.createTransporter({
  host: 'smtp.gmail.com',
  port: 465,
  secure: true,
  auth: {
    user: process.env.GMAIL_USER,
    pass: process.env.GMAIL_APP_PASSWORD
  }
});
```

---

## Social Media Automation

### Twitter/X Setup
```javascript
class TwitterBot {
  async login() {
    await page.goto('https://twitter.com/login');
    await page.fill('input[name="text"]', USERNAME);
    await page.fill('input[name="password"]', PASSWORD);
    await page.click('div[data-testid="LoginForm_Login_Button"]');
    
    // Save session after login
    await sessionManager.saveSession(page);
  }
  
  async postTweet(text) {
    await page.goto('https://twitter.com/compose/tweet');
    await page.fill('div[data-testid="tweetTextarea_0"]', text);
    await page.click('div[data-testid="tweetButton"]');
  }
}
```

### LinkedIn Setup
```javascript
class LinkedInBot {
  async login() {
    await page.goto('https://www.linkedin.com/login');
    await page.fill('#username', USERNAME);
    await page.fill('#password', PASSWORD);
    await page.click('.btn__primary--large');
    await sessionManager.saveSession(page);
  }
}
```

---

## Business Model Templates

### 1. Content Distribution Engine
```json
{
  "model": "content_distribution",
  "platforms": ["twitter", "linkedin"],
  "posts_per_day": 5,
  "content_sources": ["reddit", "youtube"],
  "monetization": "affiliate"
}
```

### 2. Lead Generation Agency
```json
{
  "model": "lead_gen",
  "target": "e-commerce",
  "sources": ["google_maps", "yellow_pages"],
  "outreach": "email",
  "pricing": "pay_per_lead"
}
```

### 3. Programmatic SEO
```json
{
  "model": "programmatic_seo",
  "niche": "local_services",
  "posts_per_day": 10,
  "monetization": "adsense"
}
```

---

## Health Monitoring

### Automated Health Checks
```bash
#!/bin/bash
# Check OpenClaw
if ! pgrep -f "openclaw"; then
  cd ~/openclaw && npm run start
fi

# Check Chrome CDP
if ! curl -s http://localhost:9222/json/version; then
  chromium --remote-debugging-port=9222 &
fi

# Check Ollama
if ! curl -s http://localhost:11434/api/tags; then
  sudo systemctl restart ollama
fi
```

Add to cron: `*/5 * * * * /home/wls/.openclaw/scripts/health-check.sh`

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Chrome won't start | `pkill -f chromium` then restart |
| Ollama not responding | `sudo systemctl restart ollama` |
| Session not persisting | Check file permissions on session dir |
| Out of memory | Increase swap or reduce concurrent agents |

---

## Essential Commands

```bash
# Start OpenClaw
npm run start

# Check status
curl http://localhost:3000/status

# View logs
tail -f ~/.openclaw/logs/app.log

# Restart Chrome
pkill -f chromium && chromium --remote-debugging-port=9222

# Check Ollama
ollama list

# Backup
tar -czf backup.tar.gz ~/.openclaw/
```

---

**Document Complete**
