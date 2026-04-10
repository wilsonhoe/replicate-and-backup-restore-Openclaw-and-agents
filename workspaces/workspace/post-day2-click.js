// Post Day 2 - TARGETED CLICK VERSION
// Inspects page to find exact Post Now button
const { chromium } = require('playwright');

const ZOHO_EMAIL = 'lisamolbot@gmail.com';
const ZOHO_PASSWORD = 'mv9p@T8iRWWQwBw';

const CONTENT = `Stop guessing your automation ROI. I built a calculator.

Example: 5 hrs/week × $50/hr = $13K/year saved*

*SoloHourly 2026 rates. Your results may vary.

What would you automate first? #Automation`;

(async () => {
  console.log('🚀 Posting Day 2 (TARGETED)\n');

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
    console.log('📄 Entering content...');
    await page.locator('div[contenteditable="true"]').first().fill(CONTENT);
    await page.waitForTimeout(2000);

    // Select channels
    console.log('📡 Selecting channels...');
    try { await page.click('text=Twitter'); console.log('✅ Twitter'); } catch (e) {}
    await page.waitForTimeout(1000);
    try { await page.click('text=LinkedIn'); console.log('✅ LinkedIn'); } catch (e) {}
    await page.waitForTimeout(2000);

    // Screenshot before clicking
    await page.screenshot({ path: './zoho-day2-before-click.png' });
    console.log('📸 Screenshot saved: zoho-day2-before-click.png\n');

    // FIND and CLICK Post Now button
    console.log('🚀 Looking for "Post Now" button...\n');

    // Method 1: Get all buttons and find the one with "Post Now" text
    const buttons = await page.locator('button').all();
    console.log(`Found ${buttons.length} buttons total`);

    let postNowButton = null;
    for (let i = 0; i < buttons.length; i++) {
      const text = await buttons[i].textContent().catch(() => '');
      const isVisible = await buttons[i].isVisible().catch(() => false);
      const isEnabled = await buttons[i].isEnabled().catch(() => false);

      if (text.includes('Post Now')) {
        console.log(`\n✅ Button ${i}: "${text.trim()}" - Visible: ${isVisible}, Enabled: ${isEnabled}`);
        if (isVisible && isEnabled) {
          postNowButton = buttons[i];
          break;
        }
      }
    }

    if (postNowButton) {
      console.log('\n🖱️  Clicking "Post Now" button...');
      await postNowButton.click();
      console.log('✅ CLICKED!\n');
    } else {
      // Fallback: try Playwright's getByRole
      console.log('\n⚠️  Trying alternative methods...');
      try {
        await page.getByRole('button', { name: /Post Now/i }).click();
        console.log('✅ Clicked using getByRole!');
      } catch (e) {
        console.log('getByRole failed:', e.message);

        // Last resort: try specific Zoho button class
        try {
          const btn = await page.locator('button.zsoBtn._round.fr._stroke.btn_resize:has-text("Post Now")').first();
          await btn.click();
          console.log('✅ Clicked using class selector!');
        } catch (e2) {
          console.log('Class selector failed:', e2.message);
        }
      }
    }

    await page.waitForTimeout(5000);
    await page.screenshot({ path: './zoho-day2-after-click.png' });
    console.log('📸 Screenshot saved: zoho-day2-after-click.png');
    console.log('\n✅ Done! Check if post published successfully.');

  } catch (error) {
    console.error('\n❌ Error:', error.message);
    await page.screenshot({ path: './zoho-day2-error.png' });
  }

  console.log('\n⏳ Browser staying open for verification.');
  console.log('Close manually when done.');
})();
