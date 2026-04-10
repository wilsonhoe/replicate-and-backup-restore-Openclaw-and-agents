// Post Day 2 Content - FIXED VERSION
// Clicks "Post" button at bottom right
const { chromium } = require('playwright');

const ZOHO_EMAIL = 'lisamolbot@gmail.com';
const ZOHO_PASSWORD = 'mv9p@T8iRWWQwBw';

const CONTENT = `Stop guessing your automation ROI. I built a calculator.

Example: 5 hrs/week × $50/hr = $13K/year saved*

*SoloHourly 2026 rates. Your results may vary.

What would you automate first? #Automation`;

(async () => {
  console.log('🚀 Posting Day 2 (FIXED)\n');

  const browser = await chromium.launch({ headless: false });
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

    // Navigate to Zoho Social
    console.log('🌐 Opening Zoho Social...');
    await page.goto('https://social.zoho.com/social/wilsoninc/1663181000000023017/Home.do');
    await page.waitForTimeout(5000);

    // Click New Post
    console.log('📝 New Post...');
    await page.click('text=New Post');
    await page.waitForTimeout(5000);

    // Enter content
    console.log('📄 Entering content...');
    await page.locator('div[contenteditable="true"]').first().fill(CONTENT);
    await page.waitForTimeout(2000);

    // Select Twitter and LinkedIn
    console.log('📡 Selecting channels...');
    try { await page.click('text=Twitter'); console.log('✅ Twitter'); } catch (e) {}
    await page.waitForTimeout(1000);
    try { await page.click('text=LinkedIn'); console.log('✅ LinkedIn'); } catch (e) {}
    await page.waitForTimeout(2000);

    // CLICK POST BUTTON (bottom right)
    console.log('🚀 Clicking POST button (bottom right)...');
    await page.click('button:has-text("Post"), button[type="submit"]');
    await page.waitForTimeout(5000);

    console.log('✅ Done! Check if post published.');

  } catch (error) {
    console.error('❌ Error:', error.message);
  }

  // Keep browser open for you to verify
  console.log('\nBrowser staying open. Verify the post, then close manually.');
})();
