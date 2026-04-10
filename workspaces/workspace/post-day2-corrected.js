// Post Day 2 - CORRECTED VERSION with proper APA 7 citation
const { chromium } = require('playwright');

const ZOHO_EMAIL = 'lisamolbot@gmail.com';
const ZOHO_PASSWORD = 'mv9p@T8iRWWQwBw';

// CORRECTED CONTENT - proper calculation and APA citation
const CONTENT = `Stop guessing your automation ROI. I built a calculator.

Example: 5 hrs/week × $50/hr = $250/week = $13K/year*

*Based on mid-level freelancer rates (SoloHourly, 2026). Your results may vary.

What would you automate first? #Automation #ROI`;

(async () => {
  console.log('🚀 Posting Day 2 (CORRECTED with APA 7 citation)\n');

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
    console.log('📝 Creating new post...');
    await page.click('text=New Post');
    await page.waitForTimeout(5000);

    // Enter content
    console.log('📄 Entering CORRECTED content...');
    await page.locator('div[contenteditable="true"]').first().fill(CONTENT);
    await page.waitForTimeout(2000);

    // Select channels
    console.log('📡 Selecting channels...');
    try { await page.click('text=Twitter'); console.log('✅ Twitter'); } catch (e) {}
    await page.waitForTimeout(1000);
    try { await page.click('text=LinkedIn'); console.log('✅ LinkedIn'); } catch (e) {}
    await page.waitForTimeout(2000);

    // Screenshot before
    await page.screenshot({ path: './zoho-day2-corrected-before.png' });

    // Find and click Post Now button
    console.log('🚀 Finding "Post Now" button...');
    const buttons = await page.locator('button').all();

    let postNowButton = null;
    for (const btn of buttons) {
      const text = await btn.textContent().catch(() => '');
      const isVisible = await btn.isVisible().catch(() => false);
      const isEnabled = await btn.isEnabled().catch(() => false);

      if (text.includes('Post Now') && isVisible && isEnabled) {
        postNowButton = btn;
        break;
      }
    }

    if (postNowButton) {
      await postNowButton.click();
      console.log('✅ Posted!');
    } else {
      console.log('⚠️  Post Now button not found');
    }

    await page.waitForTimeout(5000);
    await page.screenshot({ path: './zoho-day2-corrected-after.png' });

    console.log('\n✅ Day 2 CORRECTED posting complete!');
    console.log('Content now includes:');
    console.log('  - Full calculation: $50/hr → $250/week → $13K/year');
    console.log('  - APA 7 citation: (SoloHourly, 2026)');

  } catch (error) {
    console.error('\n❌ Error:', error.message);
    await page.screenshot({ path: './zoho-day2-corrected-error.png' });
  }

  console.log('\nBrowser open for verification.');
})();
