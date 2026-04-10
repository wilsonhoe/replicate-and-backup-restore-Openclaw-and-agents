// Final Cookie Import Playwright Script
// Import cookies and post content with proper content extraction
const { chromium } = require('playwright');
const fs = require('fs');

// Function to load content from file
function loadContent(filePath) {
  return fs.readFileSync(filePath, 'utf8');
}

// Function to extract Twitter content
function extractTwitterContent(fullContent) {
  // Split by --- followed by newline(s)
  const parts = fullContent.split(/---[\r\n]+/);
  // Part 1 contains "## Twitter Version" header + content
  const twitterPart = parts[1];
  const lines = twitterPart.split('\\n');
  let contentLines = [];
  let foundContent = false;
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes('## Twitter Version')) {
      foundContent = true;
      continue;
    }
    if (foundContent && lines[i].trim() !== '') {
      contentLines.push(lines[i]);
    }
  }
  return contentLines.join('\\n').trim();
}

// Function to extract LinkedIn content
function extractLinkedInContent(fullContent) {
  // Split by --- followed by newline(s)
  const parts = fullContent.split(/---[\r\n]+/);
  // Part 2 contains "## LinkedIn Version" header + content
  const linkedinPart = parts[2];
  const lines = linkedinPart.split('\\n');
  let contentLines = [];
  let foundContent = false;
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes('## LinkedIn Version')) {
      foundContent = true;
      continue;
    }
    if (foundContent && lines[i].trim() !== '') {
      contentLines.push(lines[i]);
    }
  }
  return contentLines.join('\\n').trim();
}

(async () => {
  let twitterPage;
  let linkedinPage;
  let browser;

  try {
    console.log('Starting cookie-based posting...');

    // Load Day 2 content
    const fullContent = loadContent('./content/social-post-002.md');
    const twitterContent = extractTwitterContent(fullContent);
    const linkedinContent = extractLinkedInContent(fullContent);
    
    console.log('Twitter content to post:', twitterContent);
    console.log('LinkedIn content to post:', linkedinContent);

    // Launch browser with cookie context
    browser = await chromium.launch({ headless: true });
    const context = await browser.newContext();
    
    // Import Twitter cookies - check multiple possible locations
    let twitterCookiesPath = './cookies-twitter.json';
    if (!fs.existsSync(twitterCookiesPath)) {
      twitterCookiesPath = '/home/wls/.openclaw/browser-data/cookies.json';
    }
    if (fs.existsSync(twitterCookiesPath)) {
      const twitterCookies = JSON.parse(fs.readFileSync(twitterCookiesPath));
      await context.addCookies(twitterCookies);
      console.log('Twitter cookies imported successfully from:', twitterCookiesPath);
    } else {
      throw new Error('Twitter cookies file not found in any expected location');
    }
    
    // Post to Twitter
    twitterPage = await context.newPage();
    // First visit main site to establish session
    await twitterPage.goto('https://x.com');
    await twitterPage.waitForTimeout(2000);
    console.log('Current URL after x.com:', await twitterPage.url());
    await twitterPage.screenshot({ path: './debug-twitter-home.png' });
    // Now go to compose
    await twitterPage.goto('https://x.com/compose/tweet');
    await twitterPage.waitForTimeout(2000);
    console.log('Current URL after compose:', await twitterPage.url());
    await twitterPage.screenshot({ path: './debug-twitter-compose.png' });
    await twitterPage.waitForSelector('[data-testid="tweetTextarea_0"]', { timeout: 10000 });

    // Method 1: Focus and type character by character (most natural for React)
    console.log('Entering tweet content...');
    const textarea = twitterPage.locator('[data-testid="tweetTextarea_0"]').first();
    await textarea.click();
    await twitterPage.waitForTimeout(500);

    // Clear any existing content
    await twitterPage.keyboard.press('Control+a');
    await twitterPage.keyboard.press('Delete');
    await twitterPage.waitForTimeout(300);

    // Type content - handle all characters properly
    for (let i = 0; i < twitterContent.length; i++) {
      const char = twitterContent[i];
      if (char === '\n') {
        await twitterPage.keyboard.press('Enter');
      } else {
        await twitterPage.keyboard.press(char);
      }
      await twitterPage.waitForTimeout(12); // Slightly longer delay for reliability
    }
    await twitterPage.waitForTimeout(800);

    // Method 2: Set full content via execCommand (handles all characters including em-dash)
    console.log('Setting full content via execCommand...');
    const isButtonEnabled = await twitterPage.evaluate(() => {
      const btn = document.querySelector('[data-testid="tweetButton"]');
      return btn && !btn.disabled && btn.getAttribute('aria-disabled') !== 'true';
    });

    if (!isButtonEnabled) {
      console.log('Button not enabled after typing, triggering additional events...');
      await twitterPage.evaluate((text) => {
        const textarea = document.querySelector('[data-testid="tweetTextarea_0"]');
        if (textarea) {
          // Use execCommand which properly triggers contentEditable events
          textarea.focus();
          document.execCommand('selectAll', false, null);
          document.execCommand('delete', false, null);
          document.execCommand('insertText', false, text);

          // Trigger additional React events
          const events = ['input', 'change', 'keyup', 'keydown', 'keypress'];
          events.forEach(eventType => {
            textarea.dispatchEvent(new Event(eventType, { bubbles: true }));
          });
        }
      }, twitterContent);
      await twitterPage.waitForTimeout(1000);
    }
    // Take screenshot before clicking
    await twitterPage.screenshot({ path: './debug-before-tweet.png' });
    // Try clicking the button even if it appears disabled (sometimes React state lags)
    await twitterPage.click('[data-testid="tweetButton"]');
    await twitterPage.waitForTimeout(3000);
    await twitterPage.screenshot({ path: './proof-day2-twitter.png' });
    console.log('Twitter post successful');
    
    // Import LinkedIn cookies - check multiple possible locations
    let linkedinCookiesPath = './cookies-linkedin.json';
    if (!fs.existsSync(linkedinCookiesPath)) {
      linkedinCookiesPath = '/home/wls/.openclaw/browser-data-linkedin/cookies.json';
    }
    if (fs.existsSync(linkedinCookiesPath)) {
      const linkedinCookies = JSON.parse(fs.readFileSync(linkedinCookiesPath));
      await context.addCookies(linkedinCookies);
      console.log('LinkedIn cookies imported successfully from:', linkedinCookiesPath);
    } else {
      throw new Error('LinkedIn cookies file not found in any expected location');
    }
    
    // Post to LinkedIn
    linkedinPage = await context.newPage();
    await linkedinPage.goto('https://www.linkedin.com/feed/');
    await linkedinPage.waitForSelector('[data-testid="share-box-placeholder"]', { timeout: 10000 });
    await linkedinPage.click('[data-testid="share-box-placeholder"]');
    await linkedinPage.waitForSelector('[data-testid="rich-text-editor"]', { timeout: 10000 });
    await linkedinPage.fill('[data-testid="rich-text-editor"]', linkedinContent);
    await linkedinPage.click('[data-testid="share-actions"] button[aria-label="Post"]');
    await linkedinPage.waitForTimeout(3000);
    await linkedinPage.screenshot({ path: './proof-day2-linkedin.png' });
    console.log('LinkedIn post successful');
    
    await browser.close();
    console.log('All posts completed successfully!');
  } catch (error) {
    console.error('Error during posting:', error);
    // Save error screenshot for debugging
    try {
      if (twitterPage) await twitterPage.screenshot({ path: './error-twitter.png' });
    } catch (e) { /* ignore screenshot error */ }
    try {
      if (linkedinPage) await linkedinPage.screenshot({ path: './error-linkedin.png' });
    } catch (e) { /* ignore screenshot error */ }
    if (browser) await browser.close();
    throw error;
  }
})();
