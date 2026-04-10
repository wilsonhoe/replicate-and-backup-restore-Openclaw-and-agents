// Post Day 2 - FINAL VERSION
// Uses precise selector for Post Now button
const { chromium } = require('playwright');

const ZOHO_EMAIL = 'lisamolbot@gmail.com';
const ZOHO_PASSWORD = 'mv9p@T8iRWWQwBw';

const CONTENT = \`Stop guessing your automation ROI. I built a calculator.

Example: 5 hrs/week × \$50/hr = \$13K/year saved*

*SoloHourly 2026 rates. Your results may vary.

What would you automate first? #Automation\`;

(async () => {
  console.log('🚀 Posting Day 2 (FINAL)\n');

  const browser = await chromium.launch({
    headless: false,
    executablePath: '/usr/bin/google-chrome'
  });

  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });

  try {
    // Login
    console.log('🔐 Logging in...');
    await page.goto('https://accounts.zoho.com/signin');
    await page.fill('#login_id', ZOHO_EMAIL);
    await page.click('#nextbtn');
    await page.waitForTimeout(2000);
    await page.fill('#password', ZOHO_PASSWORD);
    await page.click('#nextbtn');
    await page.waitForTimeout(5000);

    // Navigate
    console.log('🌐 Opening Zoho Social...');
    await page.goto('https://social.zoho.com/social/wilsoninc/1663181000000023017/Home.do');
    await page.waitForTimeout(5000);

    // New Post
    console.log('📝 New Post...');
    await page.click('text=New Post');
    await page.waitForTimeout(5000);

    // Enter content
    console.log('📄 Content...');
    await page.locator('div[contenteditable="true"]').first().fill(CONTENT);
    await page.waitForTimeout(2000);

    // Select channels
    console.log('📡 Channels...');
    try { await page.click('text=Twitter'); console.log('✅ Twitter'); } catch (e) {}
    await page.waitForTimeout(1000);
    try { await page.click('text=LinkedIn'); console.log('✅ LinkedIn'); } catch (e) {}
    await page.waitForTimeout(2000);

    // Scroll to see Post Now button
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(1000);

    // Find and click Post Now button
    console.log('🚀 Finding Post Now button...');
    
    // Try multiple selectors
    const selectors = [
      'button:has-text("Post Now")',
      'button:has-text("Post")',
      'button[type="submit"]:visible',
      '.zsoBtn:has-text("Post")',
      'button:has-text("Schedule") >> .. >> button', // Parent of Schedule
      '.post-btn',
      '[data-testid="post-button"]'
    ];

    for (const sel of selectors) {
      try {
        const btn = await page.locator(sel).filter({ hasText: /Post/ }).first();
        if (await btn.isVisible().catch(() => false)) {
          console.log('Found button with:', sel);
          await btn.click();
          console.log('✅ Clicked!');
          break;
        }
      } catch (e) {}
    }

    await page.waitForTimeout(5000);
    console.log('✅ Done!');

  } catch (error) {
    console.error('❌ Error:', error.message);
  }

  console.log('\nBrowser open. Check if post published!');
})();
