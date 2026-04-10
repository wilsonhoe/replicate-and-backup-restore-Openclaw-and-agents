// Final post script - handles Unicode by replacing × with x for Twitter
const { chromium } = require('playwright');
const fs = require('fs');

// Function to load content from file
function loadContent(filePath) {
  return fs.readFileSync(filePath, 'utf8');
}

// Function to extract Twitter content
function extractTwitterContent(fullContent) {
  const parts = fullContent.split(/---[\r\n]+/);
  const twitterPart = parts[1];
  const lines = twitterPart.split(/[\r\n]+/);
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
  return contentLines.join('\n').trim();
}

// Function to extract LinkedIn content
function extractLinkedInContent(fullContent) {
  const parts = fullContent.split(/---[\r\n]+/);
  const linkedinPart = parts[2];
  const lines = linkedinPart.split(/[\r\n]+/);
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
  return contentLines.join('\n').trim();
}

// Replace Unicode multiplication sign with regular x for Twitter
function sanitizeTwitterContent(content) {
  return content.replace(/×/g, 'x');
}

(async () => {
  let twitterPage;
  let linkedinPage;
  let browser;

  try {
    console.log('Starting final cookie-based posting...');

    // Load Day 2 content
    const fullContent = loadContent('./content/social-post-002.md');
    let twitterContent = extractTwitterContent(fullContent);
    const linkedinContent = extractLinkedInContent(fullContent);
    
    // Sanitize Twitter content (replace Unicode × with ASCII x)
    const originalTwitterContent = twitterContent;
    twitterContent = sanitizeTwitterContent(twitterContent);
    if (originalTwitterContent !== twitterContent) {
      console.log('Twitter content sanitized: replaced Unicode × with ASCII x');
    }
    
    console.log('Twitter content length:', twitterContent.length);
    console.log('LinkedIn content length:', linkedinContent.length);

    // Launch browser with cookie context
    browser = await chromium.launch({ headless: true });
    const context = await browser.newContext();
    
    // Import Twitter cookies
    let twitterCookiesPath = './cookies-twitter.json';
    if (!fs.existsSync(twitterCookiesPath)) {
      twitterCookiesPath = '/home/wls/.openclaw/browser-data/cookies.json';
    }
    if (fs.existsSync(twitterCookiesPath)) {
      const twitterCookies = JSON.parse(fs.readFileSync(twitterCookiesPath));
      await context.addCookies(twitterCookies);
      console.log('Twitter cookies imported successfully');
    } else {
      throw new Error('Twitter cookies file not found');
    }
    
    // Post to Twitter
    twitterPage = await context.newPage();
    await twitterPage.goto('https://x.com/compose/post');
    await twitterPage.waitForTimeout(3000);
    console.log('Current URL:', await twitterPage.url());
    
    // Wait for the editor to be ready with retry logic
    console.log('Waiting for tweet composer to be ready...');
    let editorReady = false;
    let attempts = 0;
    const maxAttempts = 5;
    
    while (!editorReady && attempts < maxAttempts) {
      try {
        await twitterPage.waitForSelector('[contenteditable="true"]', { timeout: 3000 });
        const isVisible = await twitterPage.locator('[contenteditable="true"]').first().isVisible();
        const isEnabled = await twitterPage.locator('[contenteditable="true"]').first().isEnabled();
        if (isVisible && isEnabled) {
          editorReady = true;
          console.log('Tweet composer is ready and interactable');
        } else {
          console.log(`Attempt ${attempts + 1}: Composer found but not interactable`);
        }
      } catch (error) {
        console.log(`Attempt ${attempts + 1}: Selector not found yet, retrying...`);
      }
      attempts++;
      if (!editorReady && attempts < maxAttempts) {
        await twitterPage.waitForTimeout(2000);
      }
    }
    
    if (!editorReady) {
      throw new Error('Could not find interactable tweet composer after multiple attempts');
    }
    
    // Proven working sequence from inspection test:
    console.log('Clicking tweet composer...');
    await twitterPage.locator('[contenteditable="true"]').first().click();
    await twitterPage.waitForTimeout(500);
    
    console.log('Selecting all...');
    await twitterPage.keyboard.press('Control+a');
    await twitterPage.waitForTimeout(200);
    
    console.log('Deleting existing content...');
    await twitterPage.keyboard.press('Delete');
    await twitterPage.waitForTimeout(200);
    
    console.log('Typing tweet content...');
    // Type the content character by character (safe for ASCII-only content)
    for (let i = 0; i < twitterContent.length; i++) {
      const char = twitterContent[i];
      if (char === '\n') {
        await twitterPage.keyboard.press('Enter');
      } else {
        await twitterPage.keyboard.press(char);
      }
      await twitterPage.waitForTimeout(15);
    }
    
    await twitterPage.waitForTimeout(800);
    
    // Click the Post button
    console.log('Clicking Post button...');
    await twitterPage.click('[aria-label="Post"]');
    await twitterPage.waitForTimeout(3000);
    
    await twitterPage.screenshot({ path: './proof-day2-twitter.png' });
    console.log('Twitter post successful');
    
    // Import LinkedIn cookies
    let linkedinCookiesPath = './cookies-linkedin.json';
    if (!fs.existsSync(linkedinCookiesPath)) {
      linkedinCookiesPath = '/home/wls/.openclaw/browser-data-linkedin/cookies.json';
    }
    if (fs.existsSync(linkedinCookiesPath)) {
      const linkedinCookies = JSON.parse(fs.readFileSync(linkedinCookiesPath));
      await context.addCookies(linkedinCookies);
      console.log('LinkedIn cookies imported successfully');
    } else {
      throw new Error('LinkedIn cookies file not found');
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
