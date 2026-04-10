# Twitter/X Automation with Playwright

## Description

Automate posting to Twitter/X using Playwright with proper React state handling for contentEditable editors.

## When to Use

- Automating Twitter/X posts from Node.js scripts
- Scheduling social media content programmatically
- Integrating Twitter posting into content pipelines
- Testing Twitter interfaces with Playwright

## Requirements

- Playwright installed (`npm install playwright`)
- Valid Twitter/X cookies exported from a logged-in browser session
- Node.js 16+ with CommonJS support

## How It Works

### The Problem

Twitter/X uses React-based `contentEditable` editors that don't respond to standard `fill()` or `innerText` methods. Simply setting text doesn't trigger React's synthetic events, leaving the "Tweet" button disabled (`aria-disabled="true"`).

### The Solution

Use **character-by-character typing** with Playwright's `keyboard.press()` to simulate real user input, which properly triggers React's input event handlers.

## Implementation

### Basic Pattern

```javascript
const { chromium } = require('playwright');

async function postToTwitter(content, cookiesPath) {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  
  // Import cookies for authentication
  const cookies = require('fs').readFileSync(cookiesPath, 'utf8');
  await context.addCookies(JSON.parse(cookies));
  
  const page = await context.newPage();
  await page.goto('https://x.com/compose/tweet');
  
  // Wait for React editor to mount
  await page.waitForSelector('[data-testid="tweetTextarea_0"]', { timeout: 10000 });
  
  // Method 1: Character-by-character typing (PRIMARY - works best)
  const textarea = page.locator('[data-testid="tweetTextarea_0"]').first();
  await textarea.click();
  await page.waitForTimeout(500);
  
  // Clear existing content
  await page.keyboard.press('Control+a');
  await page.keyboard.press('Delete');
  await page.waitForTimeout(300);
  
  // Type content character by character
  for (const char of content) {
    await page.keyboard.press(char === '\n' ? 'Enter' : char);
  }
  await page.waitForTimeout(1000);
  
  // Click tweet button
  await page.click('[data-testid="tweetButton"]');
  await page.waitForTimeout(3000);
  
  await browser.close();
}
```

### Fallback Method: execCommand

If character typing doesn't work, use `document.execCommand` with manual event dispatching:

```javascript
// Method 2: execCommand with event dispatching (FALLBACK)
const isButtonEnabled = await page.evaluate(() => {
  const btn = document.querySelector('[data-testid="tweetButton"]');
  return btn && !btn.disabled && btn.getAttribute('aria-disabled') !== 'true';
});

if (!isButtonEnabled) {
  await page.evaluate((text) => {
    const textarea = document.querySelector('[data-testid="tweetTextarea_0"]');
    if (textarea) {
      textarea.focus();
      document.execCommand('selectAll', false, null);
      document.execCommand('delete', false, null);
      document.execCommand('insertText', false, text);
      
      // Trigger React synthetic events
      ['input', 'change', 'keyup', 'keydown', 'keypress'].forEach(eventType => {
        textarea.dispatchEvent(new Event(eventType, { bubbles: true }));
      });
    }
  }, content);
  await page.waitForTimeout(1000);
}
```

## Complete Working Script

```javascript
// twitter-automation.js
const { chromium } = require('playwright');
const fs = require('fs');

async function postToTwitter(content, cookiesPath) {
  let browser;
  let page;
  
  try {
    // Launch browser
    browser = await chromium.launch({ 
      headless: true,
      args: ['--disable-blink-features=AutomationControlled']
    });
    
    const context = await browser.newContext({
      viewport: { width: 1280, height: 800 },
      userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    });
    
    // Import authentication cookies
    if (!fs.existsSync(cookiesPath)) {
      throw new Error('Cookies file not found: ' + cookiesPath);
    }
    
    const cookies = JSON.parse(fs.readFileSync(cookiesPath, 'utf8'));
    await context.addCookies(cookies);
    console.log('Cookies imported:', cookies.length);
    
    // Navigate to compose
    page = await context.newPage();
    await page.goto('https://x.com/compose/tweet');
    await page.waitForTimeout(2000);
    
    // Verify we're on compose page
    const url = page.url();
    if (!url.includes('compose/tweet')) {
      throw new Error('Failed to navigate to compose page. Current URL: ' + url);
    }
    
    // Find and focus textarea
    await page.waitForSelector('[data-testid="tweetTextarea_0"]', { timeout: 10000 });
    const textarea = page.locator('[data-testid="tweetTextarea_0"]').first();
    await textarea.click();
    await page.waitForTimeout(500);
    
    // Clear and type content character by character
    await page.keyboard.press('Control+a');
    await page.keyboard.press('Delete');
    await page.waitForTimeout(300);
    
    for (const char of content) {
      await page.keyboard.press(char === '\n' ? 'Enter' : char);
    }
    await page.waitForTimeout(1000);
    
    // Take pre-click screenshot
    await page.screenshot({ path: './twitter-before-post.png' });
    
    // Click tweet button
    await page.click('[data-testid="tweetButton"]');
    await page.waitForTimeout(3000);
    
    // Take success screenshot
    await page.screenshot({ path: './twitter-posted.png' });
    console.log('✅ Tweet posted successfully');
    
    return { success: true, screenshot: './twitter-posted.png' };
    
  } catch (error) {
    console.error('❌ Error posting to Twitter:', error.message);
    if (page) {
      await page.screenshot({ path: './twitter-error.png' }).catch(() => {});
    }
    return { success: false, error: error.message };
    
  } finally {
    if (browser) await browser.close();
  }
}

// Export for use in other scripts
module.exports = { postToTwitter };

// Run if called directly
if (require.main === module) {
  const content = process.argv[2] || 'Test tweet from automation';
  postToTwitter(content, './cookies-twitter.json')
    .then(result => {
      process.exit(result.success ? 0 : 1);
    });
}
```

## Getting Cookies

### Chrome Extension Method

1. Install "Cookie-Editor" extension from Chrome Web Store
2. Log into Twitter/X in your browser
3. Click Cookie-Editor icon → Export → Export as JSON
4. Save to `cookies-twitter.json`

### Playwright Auth Method

```javascript
// auth.js - Run once to get cookies
const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  await page.goto('https://x.com/login');
  console.log('Log in manually, then press Enter in terminal...');
  
  process.stdin.once('data', async () => {
    const cookies = await context.cookies();
    fs.writeFileSync('cookies-twitter.json', JSON.stringify(cookies, null, 2));
    console.log('Cookies saved!');
    await browser.close();
  });
})();
```

## Common Issues and Solutions

### Issue: Button remains disabled after typing

**Solution:** Ensure you're using `keyboard.press()` not `fill()` or `innerText`:

```javascript
// WRONG - doesn't trigger React state
await textarea.fill('My tweet text');
await textarea.evaluate(el => el.innerText = 'My tweet text');

// CORRECT - triggers React synthetic events
for (const char of content) {
  await page.keyboard.press(char === '\n' ? 'Enter' : char);
}
```

### Issue: "Tweet" button not found

**Solution:** Check you're on the compose page and selector is correct:

```javascript
// Verify URL first
const url = await page.url();
if (!url.includes('compose/tweet')) {
  // Try navigating directly
  await page.goto('https://x.com/compose/tweet');
}

// Use multiple selector strategies
const button = await page.$('[data-testid="tweetButton"]') 
            || await page.$('div[role="button"]:has-text("Post")');
```

### Issue: Session expired / redirected to login

**Solution:** Cookies expired, regenerate them:

```javascript
// Check login status
const isLoggedIn = await page.evaluate(() => {
  return !!document.querySelector('[data-testid="tweetTextarea_0"]');
});

if (!isLoggedIn) {
  throw new Error('Session expired - regenerate cookies');
}
```

## Examples

### Schedule Daily Posts

```javascript
const { postToTwitter } = require('./twitter-automation');

const posts = [
  { time: '09:00', content: 'Morning automation tip...' },
  { time: '13:00', content: 'Afternoon productivity hack...' },
  { time: '17:00', content: 'End of day reflection...' }
];

// Check every minute for scheduled posts
setInterval(() => {
  const now = new Date();
  const currentTime = `${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')}`;
  
  const post = posts.find(p => p.time === currentTime);
  if (post) {
    postToTwitter(post.content, './cookies-twitter.json');
  }
}, 60000);
```

### Multi-Platform Posting

```javascript
async function postToAllPlatforms(content) {
  const results = await Promise.allSettled([
    postToTwitter(content, './cookies-twitter.json'),
    postToLinkedIn(content, './cookies-linkedin.json'),
    // postToThreads(content, './cookies-threads.json')
  ]);
  
  return {
    twitter: results[0].status === 'fulfilled' ? '✅' : '❌',
    linkedin: results[1].status === 'fulfilled' ? '✅' : '❌'
  };
}
```

## Security Considerations

- **Never commit cookies to git** - add `cookies-*.json` to `.gitignore`
- **Rotate cookies regularly** - they expire or get invalidated
- **Use environment variables** for sensitive paths
- **Rate limit your posts** - avoid triggering anti-spam measures
- **Store cookies securely** - use proper file permissions (chmod 600)

## Troubleshooting Checklist

- [ ] Cookies file exists and is valid JSON
- [ ] Cookies include `auth_token` and `ct0` for Twitter
- [ ] Content under 280 characters (Twitter limit)
- [ ] Playwright browsers installed (`npx playwright install`)
- [ ] No popups or verification challenges in browser
- [ ] Stable internet connection
- [ ] Not rate-limited by Twitter

## Related Skills

- `linkedin-playwright-automation` - Similar pattern for LinkedIn
- `playwright-cookie-auth` - General cookie-based authentication
- `content-pipeline` - Multi-platform content scheduling

## References

- Playwright docs: https://playwright.dev/docs/input
- Twitter Web API (unofficial): https://github.com/d60/twikit
- React synthetic events: https://reactjs.org/docs/events.html

## Attribution

- **Created:** 2026-04-02
- **Tested:** Twitter/X React editor
- **Working:** Character-by-character typing method
- **Verified by:** Lisa (LisaLLM83)
- **Context:** Claude-Lisa social media automation project
