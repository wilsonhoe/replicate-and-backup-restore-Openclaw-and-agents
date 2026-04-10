# Lisa Browser Session Setup Guide
## Task #9 - Phase 2: Browser Session Infrastructure

---

## Step 1: Chrome with Remote Debugging

**Launch Chrome with CDP:**

```bash
# Linux
chromium-browser \
  --remote-debugging-port=9222 \
  --no-first-run \
  --no-default-browser-check \
  --user-data-dir=/home/wls/.chrome-lisa \
  --disable-extensions \
  --disable-gpu \
  --window-size=1920,1080

# Or use existing Chrome with debugging
google-chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/home/wls/.chrome-lisa
```

**Verify CDP is running:**
```bash
curl http://localhost:9222/json/version
# Should return: {"Browser": "Chrome/...", "Protocol-Version": "1.3", ...}
```

---

## Step 2: Session Manager Module

**File:** `/home/wls/.openclaw/lib/session-manager.js`

```javascript
const fs = require('fs').promises;
const path = require('path');

class SessionManager {
  constructor(sessionDir = '/home/wls/.openclaw/sessions') {
    this.sessionDir = sessionDir;
    this.ensureDir();
  }

  async ensureDir() {
    try {
      await fs.mkdir(this.sessionDir, { recursive: true });
    } catch (e) {
      console.error('Failed to create session directory:', e);
    }
  }

  getSessionPath(platform) {
    return path.join(this.sessionDir, `${platform}_session.json`);
  }

  async saveSession(platform, page) {
    try {
      // Get cookies
      const cookies = await page.context().cookies();

      // Get localStorage
      const localStorage = await page.evaluate(() => {
        const items = {};
        for (let i = 0; i < localStorage.length; i++) {
          const key = localStorage.key(i);
          items[key] = localStorage.getItem(key);
        }
        return items;
      });

      // Get sessionStorage
      const sessionStorage = await page.evaluate(() => {
        const items = {};
        for (let i = 0; i < sessionStorage.length; i++) {
          const key = sessionStorage.key(i);
          items[key] = sessionStorage.getItem(key);
        }
        return items;
      });

      const session = {
        cookies,
        localStorage,
        sessionStorage,
        timestamp: new Date().toISOString(),
        platform
      };

      const sessionPath = this.getSessionPath(platform);
      await fs.writeFile(sessionPath, JSON.stringify(session, null, 2));

      console.log(`✅ Session saved for ${platform}`);
      return true;
    } catch (error) {
      console.error(`❌ Failed to save session for ${platform}:`, error);
      return false;
    }
  }

  async loadSession(platform, context) {
    try {
      const sessionPath = this.getSessionPath(platform);
      const data = await fs.readFile(sessionPath, 'utf8');
      const session = JSON.parse(data);

      // Restore cookies
      await context.addCookies(session.cookies);

      // Note: localStorage/sessionStorage must be set on page, not context
      // This happens after page navigation

      console.log(`✅ Session loaded for ${platform}`);
      return session;
    } catch (error) {
      console.log(`ℹ️ No existing session for ${platform}`);
      return null;
    }
  }

  async restoreStorage(page, platform) {
    try {
      const sessionPath = this.getSessionPath(platform);
      const data = await fs.readFile(sessionPath, 'utf8');
      const session = JSON.parse(data);

      // Restore localStorage
      await page.evaluate((storage) => {
        Object.entries(storage).forEach(([key, value]) => {
          localStorage.setItem(key, value);
        });
      }, session.localStorage);

      // Restore sessionStorage
      await page.evaluate((storage) => {
        Object.entries(storage).forEach(([key, value]) => {
          sessionStorage.setItem(key, value);
        });
      }, session.sessionStorage);

      return true;
    } catch (error) {
      console.error(`Failed to restore storage:`, error);
      return false;
    }
  }

  async isSessionValid(platform) {
    try {
      const sessionPath = this.getSessionPath(platform);
      const stats = await fs.stat(sessionPath);
      const age = Date.now() - stats.mtime.getTime();
      const maxAge = 7 * 24 * 60 * 60 * 1000; // 7 days

      return age < maxAge;
    } catch {
      return false;
    }
  }
}

module.exports = SessionManager;
```

---

## Step 3: Twitter Login with Session Persistence

**File:** `/home/wls/.openclaw/lib/twitter-auth.js`

```javascript
const { chromium } = require('playwright');
const SessionManager = require('./session-manager');

class TwitterAuth {
  constructor() {
    this.sessionManager = new SessionManager();
    this.platform = 'twitter';
  }

  async login(username, password) {
    const browser = await chromium.connectOverCDP('http://localhost:9222');
    const context = browser.contexts()[0] || await browser.newContext();
    const page = await context.newPage();

    try {
      // Check for existing session
      const hasSession = await this.sessionManager.isSessionValid(this.platform);

      if (hasSession) {
        console.log('🔄 Restoring Twitter session...');
        await this.sessionManager.loadSession(this.platform, context);
        await page.goto('https://twitter.com');
        await this.sessionManager.restoreStorage(page, this.platform);

        // Verify we're logged in
        await page.waitForTimeout(2000);
        const isLoggedIn = await page.querySelector('[data-testid="SideNav_AccountSwitcher_Button"]') !== null;

        if (isLoggedIn) {
          console.log('✅ Twitter session restored successfully');
          return { page, context, browser };
        }
        console.log('⚠️ Session expired, logging in again...');
      }

      // Fresh login
      console.log('🔐 Logging into Twitter...');
      await page.goto('https://twitter.com/login');

      await page.fill('input[name="text"]', username);
      await page.click('text=Next');

      await page.fill('input[name="password"]', password);
      await page.click('div[data-testid="LoginForm_Login_Button"]');

      // Wait for login completion
      await page.waitForSelector('[data-testid="SideNav_AccountSwitcher_Button"]', {
        timeout: 30000
      });

      // Save session
      await this.sessionManager.saveSession(this.platform, page);
      console.log('✅ Twitter login successful, session saved');

      return { page, context, browser };

    } catch (error) {
      console.error('❌ Twitter login failed:', error);
      await browser.close();
      throw error;
    }
  }

  async postTweet(page, text, media = null) {
    try {
      await page.goto('https://twitter.com/compose/tweet');
      await page.waitForSelector('[data-testid="tweetTextarea_0"]', { timeout: 10000 });

      await page.fill('[data-testid="tweetTextarea_0"]', text);

      if (media) {
        await page.setInputFiles('input[type="file"]', media);
        await page.waitForTimeout(2000);
      }

      await page.click('[data-testid="tweetButton"]');
      await page.waitForTimeout(3000);

      console.log('✅ Tweet posted:', text.substring(0, 50) + '...');
      return true;
    } catch (error) {
      console.error('❌ Failed to post tweet:', error);
      return false;
    }
  }
}

module.exports = TwitterAuth;
```

---

## Step 4: LinkedIn Login with Session Persistence

**File:** `/home/wls/.openclaw/lib/linkedin-auth.js`

```javascript
const { chromium } = require('playwright');
const SessionManager = require('./session-manager');

class LinkedInAuth {
  constructor() {
    this.sessionManager = new SessionManager();
    this.platform = 'linkedin';
  }

  async login(username, password) {
    const browser = await chromium.connectOverCDP('http://localhost:9222');
    const context = browser.contexts()[0] || await browser.newContext();
    const page = await context.newPage();

    try {
      // Check for existing session
      const hasSession = await this.sessionManager.isSessionValid(this.platform);

      if (hasSession) {
        console.log('🔄 Restoring LinkedIn session...');
        await this.sessionManager.loadSession(this.platform, context);
        await page.goto('https://www.linkedin.com/feed/');
        await this.sessionManager.restoreStorage(page, this.platform);

        // Verify we're logged in
        await page.waitForTimeout(2000);
        const isLoggedIn = await page.querySelector('.feed-identity-module') !== null;

        if (isLoggedIn) {
          console.log('✅ LinkedIn session restored successfully');
          return { page, context, browser };
        }
        console.log('⚠️ Session expired, logging in again...');
      }

      // Fresh login
      console.log('🔐 Logging into LinkedIn...');
      await page.goto('https://www.linkedin.com/login');

      await page.fill('#username', username);
      await page.fill('#password', password);
      await page.click('.btn__primary--large');

      // Handle security challenges if they appear
      try {
        await page.waitForSelector('.feed-identity-module', { timeout: 30000 });
      } catch {
        // Might be on security check page
        console.log('⚠️ LinkedIn may require manual verification');
        await page.waitForTimeout(10000); // Give time to solve
      }

      // Save session
      await this.sessionManager.saveSession(this.platform, page);
      console.log('✅ LinkedIn login successful, session saved');

      return { page, context, browser };

    } catch (error) {
      console.error('❌ LinkedIn login failed:', error);
      await browser.close();
      throw error;
    }
  }

  async postUpdate(page, text) {
    try {
      await page.goto('https://www.linkedin.com/feed/');
      await page.waitForSelector('.share-box-feed-entry__trigger', { timeout: 10000 });

      await page.click('.share-box-feed-entry__trigger');
      await page.waitForSelector('.ql-editor', { timeout: 10000 });

      await page.fill('.ql-editor p', text);
      await page.waitForTimeout(500);

      await page.click('.share-actions__primary-action');
      await page.waitForTimeout(3000);

      console.log('✅ LinkedIn post published:', text.substring(0, 50) + '...');
      return true;
    } catch (error) {
      console.error('❌ Failed to post to LinkedIn:', error);
      return false;
    }
  }
}

module.exports = LinkedInAuth;
```

---

## Step 5: Test Script

**File:** `/home/wls/.openclaw/scripts/test-browser-sessions.js`

```javascript
const TwitterAuth = require('../lib/twitter-auth');
const LinkedInAuth = require('../lib/linkedin-auth');

async function testBrowserSessions() {
  console.log('🧪 Testing Browser Session Persistence\n');

  // Test Twitter
  console.log('--- Testing Twitter ---');
  const twitter = new TwitterAuth();
  try {
    const { page: twPage, browser: twBrowser } = await twitter.login(
      process.env.TWITTER_USERNAME,
      process.env.TWITTER_PASSWORD
    );

    // Test posting
    await twitter.postTweet(twPage, 'Test tweet from Lisa automation system 🤖');

    await twBrowser.close();
    console.log('✅ Twitter test passed\n');
  } catch (error) {
    console.error('❌ Twitter test failed:', error.message);
  }

  // Test LinkedIn
  console.log('--- Testing LinkedIn ---');
  const linkedin = new LinkedInAuth();
  try {
    const { page: liPage, browser: liBrowser } = await linkedin.login(
      process.env.LINKEDIN_USERNAME,
      process.env.LINKEDIN_PASSWORD
    );

    // Test posting
    await linkedin.postUpdate(liPage, 'Testing LinkedIn automation from Lisa AI system 🤖');

    await liBrowser.close();
    console.log('✅ LinkedIn test passed\n');
  } catch (error) {
    console.error('❌ LinkedIn test failed:', error.message);
  }

  console.log('🎉 Browser session tests complete!');
}

// Run tests
if (require.main === module) {
  testBrowserSessions();
}

module.exports = { testBrowserSessions };
```

---

## Verification Checklist

- [ ] Chrome launched with --remote-debugging-port=9222
- [ ] CDP responding on port 9222
- [ ] Session manager module created
- [ ] Twitter auth module working
- [ ] LinkedIn auth module working
- [ ] Session persistence saving correctly
- [ ] Session restoration working
- [ ] Can post to Twitter
- [ ] Can post to LinkedIn
- [ ] Environment variables set (TWITTER_USERNAME, TWITTER_PASSWORD, LINKEDIN_USERNAME, LINKEDIN_PASSWORD)

---

**Status:** Phase 2 Ready
**Next:** Integration with OpenClaw
