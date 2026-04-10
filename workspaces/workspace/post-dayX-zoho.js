#!/usr/bin/env node
// Zoho Social Posting Script - Generic for any Day
// Usage: node post-dayX-zoho.js 3 (for Day 3)

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ZOHO_EMAIL = 'lisamolbot@gmail.com';
const ZOHO_PASSWORD = 'mv9p@T8iRWWQwBw';

// Get day number from command line
const dayNumber = process.argv[2] || '2';
const paddedDay = dayNumber.padStart(3, '0');

// Content file path
const contentFile = `./content/social-post-${paddedDay}.md`;

// Load content
function loadContent(filePath) {
  if (!fs.existsSync(filePath)) {
    throw new Error(`Content file not found: ${filePath}`);
  }

  const content = fs.readFileSync(filePath, 'utf8');

  // Extract Twitter version
  const twitterMatch = content.match(/## Twitter Version \(280 chars\)\n\n([\s\S]+?)(?=\n## |\n---|$)/);
  const twitterContent = twitterMatch ? twitterMatch[1].trim() : '';

  // Extract LinkedIn version
  const linkedinMatch = content.match(/## LinkedIn Version\n\n([\s\S]+?)(?=\n## |\n---|$)/);
  const linkedinContent = linkedinMatch ? linkedinMatch[1].trim() : '';

  return { twitter: twitterContent, linkedin: linkedinContent };
}

(async () => {
  console.log(`🚀 Posting Day ${dayNumber} content via Zoho Social...\n`);

  // Load content
  let content;
  try {
    content = loadContent(contentFile);
    console.log('✅ Content loaded');
    console.log('Twitter length:', content.twitter.length, 'chars');
    console.log('LinkedIn length:', content.linkedin.length, 'chars\n');
  } catch (err) {
    console.error('❌ Error:', err.message);
    process.exit(1);
  }

  // Check tokens exist
  if (!fs.existsSync('./zoho-tokens.json')) {
    console.error('❌ Error: zoho-tokens.json not found. Run OAuth flow first.');
    process.exit(1);
  }
  console.log('✅ OAuth tokens found\n');

  console.log('🌐 Launching browser...');
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  const page = await context.newPage();

  try {
    // Step 1: Login to Zoho
    console.log('🔐 Logging into Zoho...');
    await page.goto('https://accounts.zoho.com/signin');
    await page.waitForTimeout(2000);

    await page.fill('#login_id', ZOHO_EMAIL);
    await page.click('#nextbtn');
    await page.waitForTimeout(2000);

    await page.fill('#password', ZOHO_PASSWORD);
    await page.click('#nextbtn');
    await page.waitForTimeout(5000);
    console.log('✅ Logged in\n');

    // Step 2: Navigate to Zoho Social
    console.log('🌐 Navigating to Zoho Social...');
    await page.goto('https://social.zoho.com/social/wilsoninc/1663181000000023017/Home.do');
    await page.waitForTimeout(5000);
    await page.screenshot({ path: `./zoho-day${dayNumber}-01-home.png` });
    console.log('✅ Home page loaded\n');

    // Step 3: Click New Post
    console.log('📝 Creating new post...');
    const newPostSelectors = [
      'text=New Post',
      'button:has-text("New Post")',
      'a:has-text("New Post")',
      '[data-testid="new-post-btn"]',
      'a[href*="NewPost"]'
    ];

    let clicked = false;
    for (const selector of newPostSelectors) {
      try {
        const element = await page.locator(selector).first();
        if (await element.isVisible().catch(() => false)) {
          await element.click();
          clicked = true;
          console.log(`✅ Clicked: ${selector}`);
          break;
        }
      } catch (e) { /* Continue to next selector */ }
    }

    if (!clicked) {
      await page.goto('https://social.zoho.com/social/wilsoninc/1663181000000023017/NewPost.do');
    }

    await page.waitForTimeout(5000);
    await page.screenshot({ path: `./zoho-day${dayNumber}-02-compose.png` });
    console.log('✅ Compose page loaded\n');

    // Step 4: Enter content (use LinkedIn version as it's longer)
    console.log('📄 Entering content...');
    const contentSelectors = [
      'textarea[name="content"]',
      'textarea',
      'div[contenteditable="true"]',
      '[data-testid="content-textarea"]',
      '.post-content'
    ];

    let contentEntered = false;
    for (const selector of contentSelectors) {
      try {
        const element = await page.locator(selector).first();
        if (await element.isVisible().catch(() => false)) {
          await element.fill(content.linkedin);
          contentEntered = true;
          console.log(`✅ Content entered via: ${selector}`);
          break;
        }
      } catch (e) { /* Continue */ }
    }

    if (!contentEntered) {
      throw new Error('Could not find content input field');
    }

    await page.waitForTimeout(2000);
    await page.screenshot({ path: `./zoho-day${dayNumber}-03-content.png` });
    console.log('✅ Content entered\n');

    // Step 5: Select channels
    console.log('📡 Selecting channels...');

    // Select Twitter
    const twitterSelectors = ['text=Twitter', '[data-testid="twitter"]', '.twitter-icon', 'label:has-text("Twitter")'];
    for (const selector of twitterSelectors) {
      try {
        const element = await page.locator(selector).first();
        if (await element.isVisible().catch(() => false)) {
          await element.click();
          console.log('✅ Twitter selected');
          break;
        }
      } catch (e) { /* Continue */ }
    }

    // Select LinkedIn
    const linkedinSelectors = ['text=LinkedIn', '[data-testid="linkedin"]', '.linkedin-icon', 'label:has-text("LinkedIn")'];
    for (const selector of linkedinSelectors) {
      try {
        const element = await page.locator(selector).first();
        if (await element.isVisible().catch(() => false)) {
          await element.click();
          console.log('✅ LinkedIn selected');
          break;
        }
      } catch (e) { /* Continue */ }
    }

    await page.waitForTimeout(2000);
    await page.screenshot({ path: `./zoho-day${dayNumber}-04-ready.png` });
    console.log('✅ Channels selected\n');

    // Step 6: Publish
    console.log('🚀 Publishing...');
    const publishSelectors = [
      'button:has-text("Publish")',
      'button:has-text("Post")',
      '[data-testid="publish-btn"]',
      '.publish-btn'
    ];

    for (const selector of publishSelectors) {
      try {
        const element = await page.locator(selector).first();
        if (await element.isVisible().catch(() => false)) {
          await element.click();
          console.log(`✅ Published via: ${selector}`);
          break;
        }
      } catch (e) { /* Continue */ }
    }

    await page.waitForTimeout(5000);
    await page.screenshot({ path: `./zoho-day${dayNumber}-05-success.png` });

    console.log(`\n✅ Day ${dayNumber} posting COMPLETE!`);
    console.log('Screenshots saved:');
    console.log(`  - zoho-day${dayNumber}-01-home.png`);
    console.log(`  - zoho-day${dayNumber}-02-compose.png`);
    console.log(`  - zoho-day${dayNumber}-03-content.png`);
    console.log(`  - zoho-day${dayNumber}-04-ready.png`);
    console.log(`  - zoho-day${dayNumber}-05-success.png`);

  } catch (error) {
    console.error('\n❌ Error:', error.message);
    await page.screenshot({ path: `./zoho-day${dayNumber}-error.png` });
    console.log(`Error screenshot saved: zoho-day${dayNumber}-error.png`);
  } finally {
    await browser.close();
  }
})();
