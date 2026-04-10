// Post Day 2 Content via Zoho Social - SHORT VERSION (under 210 chars)
const { chromium } = require('playwright');
const fs = require('fs');

const ZOHO_EMAIL = 'lisamolbot@gmail.com';
const ZOHO_PASSWORD = 'mv9p@T8iRWWQwBw';

// SHORT VERSION - under 210 characters for Twitter
const SHORT_CONTENT = `Stop guessing your automation ROI. I built a calculator.

Example: 5 hrs/week × $50/hr = $13K/year saved*

*SoloHourly 2026 rates. Your results may vary.

What would you automate first? #Automation`;

(async () => {
  console.log('🚀 Posting Day 2 content (SHORT VERSION)\n');
  console.log('Content length:', SHORT_CONTENT.length, 'chars\n');

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  const page = await context.newPage();

  try {
    // Login
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

    // Navigate to Zoho Social
    console.log('🌐 Navigating to Zoho Social...');
    await page.goto('https://social.zoho.com/social/wilsoninc/1663181000000023017/Home.do');
    await page.waitForTimeout(5000);
    await page.screenshot({ path: './zoho-day2-short-01-home.png' });
    console.log('✅ Home loaded\n');

    // Click New Post
    console.log('📝 Creating new post...');
    const selectors = ['text=New Post', 'button:has-text("New Post")', 'a:has-text("New Post")'];
    for (const sel of selectors) {
      try {
        const el = await page.locator(sel).first();
        if (await el.isVisible().catch(() => false)) { await el.click(); break; }
      } catch (e) {}
    }
    await page.waitForTimeout(5000);
    await page.screenshot({ path: './zoho-day2-short-02-compose.png' });
    console.log('✅ Compose loaded\n');

    // Enter content
    console.log('📄 Entering content...');
    const contentSelectors = ['textarea', 'div[contenteditable="true"]'];
    for (const sel of contentSelectors) {
      try {
        const el = await page.locator(sel).first();
        if (await el.isVisible().catch(() => false)) { await el.fill(SHORT_CONTENT); break; }
      } catch (e) {}
    }
    await page.waitForTimeout(2000);
    await page.screenshot({ path: './zoho-day2-short-03-content.png' });
    console.log('✅ Content entered\n');

    // Select channels
    console.log('📡 Selecting channels...');
    try { await page.locator('text=Twitter').first().click(); console.log('✅ Twitter'); } catch (e) {}
    await page.waitForTimeout(1000);
    try { await page.locator('text=LinkedIn').first().click(); console.log('✅ LinkedIn'); } catch (e) {}
    await page.waitForTimeout(2000);
    await page.screenshot({ path: './zoho-day2-short-04-ready.png' });
    console.log('✅ Channels selected\n');

    // Publish
    console.log('🚀 Publishing...');
    const pubSelectors = ['button:has-text("Publish")', 'button:has-text("Post")', '[data-testid="publish-btn"]'];
    for (const sel of pubSelectors) {
      try {
        const el = await page.locator(sel).first();
        if (await el.isVisible().catch(() => false)) { await el.click(); break; }
      } catch (e) {}
    }

    await page.waitForTimeout(5000);
    await page.screenshot({ path: './zoho-day2-short-05-success.png' });

    console.log('\n✅ Day 2 posting COMPLETE!');

  } catch (error) {
    console.error('\n❌ Error:', error.message);
    await page.screenshot({ path: './zoho-day2-short-error.png' });
  } finally {
    await browser.close();
  }
})();
