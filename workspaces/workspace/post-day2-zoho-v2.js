// Post Day 2 Content via Zoho Social Browser Automation - Version 2
const { chromium } = require('playwright');
const fs = require('fs');

const ZOHO_EMAIL = 'lisamolbot@gmail.com';
const ZOHO_PASSWORD = 'mv9p@T8iRWWQwBw';

// Day 2 Content
const TWITTER_CONTENT = `Stop guessing your automation ROI. I built a calculator.

Example: 5 hrs/week × $50/hr = $250/week = $13K/year*

*Based on mid-level freelancer rates (SoloHourly, 2026). Your results may vary.

What would you automate first? #Automation #ROI`;

(async () => {
  console.log('🌐 Launching browser...');
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  const page = await context.newPage();

  try {
    // Step 1: Login
    console.log('🔐 Logging into Zoho...');
    await page.goto('https://accounts.zoho.com/signin');
    await page.waitForTimeout(2000);

    await page.fill('#login_id', ZOHO_EMAIL);
    await page.click('#nextbtn');
    await page.waitForTimeout(2000);

    await page.fill('#password', ZOHO_PASSWORD);
    await page.click('#nextbtn');
    await page.waitForTimeout(5000);

    // Step 2: Navigate to Zoho Social
    console.log('🌐 Navigating to Zoho Social...');
    await page.goto('https://social.zoho.com/social/wilsoninc/1663181000000023017/Home.do');
    await page.waitForTimeout(5000);
    await page.screenshot({ path: './zoho-day2-v2-01-home.png' });

    // Step 3: Click New Post
    console.log('📝 Opening new post...');
    // Try multiple selector patterns
    const newPostSelectors = [
      'text=New Post',
      'button:has-text("New Post")',
      'a:has-text("New Post")',
      '[data-testid="new-post-btn"]',
      '.new-post-btn',
      'button:has-text("Create")',
      '.create-post',
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
      } catch (e) {
        // Continue to next selector
      }
    }

    if (!clicked) {
      // Try direct navigation to NewPost URL
      console.log('⚠️ Direct navigation to NewPost...');
      await page.goto('https://social.zoho.com/social/wilsoninc/1663181000000023017/NewPost.do');
    }

    await page.waitForTimeout(5000);
    await page.screenshot({ path: './zoho-day2-v2-02-compose.png' });

    // Step 4: Enter content
    console.log('📄 Entering content...');
    const contentSelectors = [
      'textarea[name="content"]',
      'textarea',
      'div[contenteditable="true"]',
      '[data-testid="content-textarea"]',
      '.post-content',
      '.editor-content'
    ];

    let contentEntered = false;
    for (const selector of contentSelectors) {
      try {
        const element = await page.locator(selector).first();
        if (await element.isVisible().catch(() => false)) {
          await element.fill(TWITTER_CONTENT);
          contentEntered = true;
          console.log(`✅ Content entered via: ${selector}`);
          break;
        }
      } catch (e) {
        // Continue
      }
    }

    if (!contentEntered) {
      throw new Error('Could not find content input field');
    }

    await page.waitForTimeout(2000);
    await page.screenshot({ path: './zoho-day2-v2-03-content.png' });

    // Step 5: Select Twitter channel
    console.log('📡 Selecting channels...');
    const twitterSelectors = [
      'text=Twitter',
      '[data-testid="twitter"]',
      '.twitter-icon',
      'label:has-text("Twitter")',
      'input[value*="twitter"]'
    ];

    for (const selector of twitterSelectors) {
      try {
        const element = await page.locator(selector).first();
        if (await element.isVisible().catch(() => false)) {
          await element.click();
          console.log(`✅ Selected Twitter via: ${selector}`);
          break;
        }
      } catch (e) {
        // Continue
      }
    }

    // Step 6: Select LinkedIn channel
    const linkedinSelectors = [
      'text=LinkedIn',
      '[data-testid="linkedin"]',
      '.linkedin-icon',
      'label:has-text("LinkedIn")',
      'input[value*="linkedin"]'
    ];

    for (const selector of linkedinSelectors) {
      try {
        const element = await page.locator(selector).first();
        if (await element.isVisible().catch(() => false)) {
          await element.click();
          console.log(`✅ Selected LinkedIn via: ${selector}`);
          break;
        }
      } catch (e) {
        // Continue
      }
    }

    await page.waitForTimeout(2000);
    await page.screenshot({ path: './zoho-day2-v2-04-ready.png' });

    // Step 7: Publish
    console.log('🚀 Publishing...');
    const publishSelectors = [
      'button:has-text("Publish")',
      'button:has-text("Post")',
      '[data-testid="publish-btn"]',
      '.publish-btn',
      'button[type="submit"]'
    ];

    for (const selector of publishSelectors) {
      try {
        const element = await page.locator(selector).first();
        if (await element.isVisible().catch(() => false)) {
          await element.click();
          console.log(`✅ Published via: ${selector}`);
          break;
        }
      } catch (e) {
        // Continue
      }
    }

    await page.waitForTimeout(5000);
    await page.screenshot({ path: './zoho-day2-v2-05-success.png' });

    console.log('✅ Day 2 posting complete!');

  } catch (error) {
    console.error('❌ Error:', error.message);
    await page.screenshot({ path: './zoho-day2-v2-error.png' });
  } finally {
    await browser.close();
  }
})();
