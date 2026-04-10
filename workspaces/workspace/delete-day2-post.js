// Delete Day 2 post from Zoho Social
const { chromium } = require('playwright');

const ZOHO_EMAIL = 'lisamolbot@gmail.com';
const ZOHO_PASSWORD = 'mv9p@T8iRWWQwBw';

(async () => {
  console.log('🗑️  Deleting Day 2 post from Zoho Social\n');

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

    // Navigate to Zoho Social
    console.log('🌐 Opening Zoho Social...');
    await page.goto('https://social.zoho.com/social/wilsoninc/1663181000000023017/Home.do');
    await page.waitForTimeout(5000);
    await page.screenshot({ path: './delete-day2-01-home.png' });

    // Navigate to Published Posts
    console.log('📋 Opening Published Posts...');
    try {
      await page.click('text=Published');
      console.log('✅ Clicked Published tab');
    } catch (e) {
      console.log('⚠️  Could not find Published tab, trying alternative...');
      // Try Posts section
      await page.goto('https://social.zoho.com/social/wilsoninc/1663181000000023017/Posts.do');
    }
    await page.waitForTimeout(5000);
    await page.screenshot({ path: './delete-day2-02-posts.png' });

    // Look for Day 2 post
    console.log('🔍 Looking for Day 2 post...');
    console.log('   Search for: "Stop guessing your automation ROI"');
    console.log('   Or look for posts from today\n');

    // Wait for user to find and delete
    console.log('⏳ Please find the Day 2 post manually:');
    console.log('   1. Look for post with "Stop guessing your automation ROI"');
    console.log('   2. Click the 3-dot menu on the post');
    console.log('   3. Select "Delete" or "Remove"\n');

    console.log('📸 Screenshot saved: delete-day2-02-posts.png');
    console.log('🌐 Browser open - delete the post manually\n');

    // Keep browser open
    await new Promise(() => {});

  } catch (error) {
    console.error('❌ Error:', error.message);
    await page.screenshot({ path: './delete-day2-error.png' });
  }
})();
