// Robust post script for both Twitter and LinkedIn
// Fixes timing, Unicode, and interception issues
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

// Wait for element with retries
async function waitForElement(page, selector, timeout = 5000, retries = 3) {
  for (let attempt = 0; attempt < retries; attempt++) {
    try {
      await page.waitForSelector(selector, { timeout });
      const element = page.locator(selector).first();
      const isVisible = await element.isVisible();
      const isEnabled = await element.isEnabled();
      if (isVisible && isEnabled) {
        return element;
      }
    } catch (error) {
      if (attempt === retries - 1) throw error;
      await page.waitForTimeout(1000); // Wait before retry
    }
  }
  throw new Error(`Element ${selector} not ready after ${retries} attempts`);
}

// Safely fill content (handles Unicode by using fill instead of keyboard typing for safety)
async function safeFill(page, selector, content) {
  const element = await waitForElement(page, selector);
  await element.click();
  await page.waitForTimeout(200);
  
  // Clear existing content
  await page.keyboard.press('Control+a');
  await page.keyboard.press('Delete');
  await page.waitForTimeout(200);
  
  // Fill with content
  await element.fill(content);
  
  // Trigger events to ensure framework detects the change
  await page.evaluate((sel) => {
    const elem = document.querySelector(sel);
    if (elem) {
      elem.dispatchEvent(new Event('input', { bubbles: true }));
      elem.dispatchEvent(new Event('change', { bubbles: true }));
    }
  }, selector);
  
  await page.waitForTimeout(500);
}

(async () => {
  let twitterPage;
  let linkedinPage;
  let browser;

  try {
    console.log('Starting robust cookie-based posting for both platforms...');

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
    
    // ========== TWITTER POSTING ==========
    console.log('\\n=== TWITTER POSTING ===');
    
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
    
    // Wait for the editor to be ready
    console.log('Waiting for tweet composer to be ready...');
    const twitterEditor = await waitForElement(twitterPage, '[contenteditable="true"]');
    console.log('Tweet composer is ready');
    
    // Fill and submit Twitter post
    await safeFill(twitterPage, '[contenteditable="true"]', twitterContent);
    
    // Submit using Ctrl+Enter (keyboard shortcut) to avoid overlay interception
    console.log('Submitting tweet using Ctrl+Enter...');
    await twitterPage.keyboard.press('Control+Enter');
    await twitterPage.waitForTimeout(3000);
    
    await twitterPage.screenshot({ path: './proof-day2-twitter.png' });
    console.log('✅ Twitter post successful');
    
    // ========== LINKEDIN POSTING ==========
    console.log('\\n=== LINKEDIN POSTING ===');
    
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
    await linkedinPage.waitForTimeout(3000);
    console.log('Current URL:', await linkedinPage.url());
    
    // Wait for and click the share box to open the editor
    console.log('Waiting for LinkedIn share box to be ready...');
    const shareBox = await waitForElement(linkedinPage, '[data-testid="share-box-placeholder"]');
    console.log('Share box is ready');
    
    await shareBox.click();
    await linkedinPage.waitForTimeout(2000);
    
    // Wait for the rich text editor to be ready
    console.log('Waiting for LinkedIn rich text editor to be ready...');
    const linkedinEditor = await waitForElement(linkedinPage, '[data-testid="rich-text-editor"]');
    console.log('Rich text editor is ready');
    
    // Fill LinkedIn post
    await safeFill(linkedinPage, '[data-testid="rich-text-editor"]', linkedinContent);
    
    // Submit LinkedIn post
    console.log('Submitting LinkedIn post...');
    await linkedinPage.click('[data-testid="share-actions"] button[aria-label="Post"]');
    await linkedinPage.waitForTimeout(3000);
    
    await linkedinPage.screenshot({ path: './proof-day2-linkedin.png' });
    console.log('✅ LinkedIn post successful');
    
    await browser.close();
    console.log('\\n🎉 All posts completed successfully!');
    console.log('📝 Day 2 content (Automation ROI Calculator) posted to both Twitter and LinkedIn');
  } catch (error) {
    console.error('\\n❌ Error during posting:', error);
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
