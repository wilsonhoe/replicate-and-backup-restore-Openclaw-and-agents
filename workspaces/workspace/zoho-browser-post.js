// Zoho Social Browser Automation Posting
// Logs into Zoho Social and posts to connected accounts

const { chromium } = require('playwright');
const fs = require('fs');

const ZOHO_EMAIL = 'lisamolbot@gmail.com';
const ZOHO_PASSWORD = 'mv9p@T8iRWWQwBw';
const SOCIAL_PROFILE_ID = '1663181000000023017';

// Load content
function loadContent(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const parts = content.split('---\n');
  if (parts.length >= 3) {
    return parts[2].trim();
  }
  return content.trim();
}

(async () => {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    console.log('🌐 Opening Zoho Social...');
    // Start with login page
    await page.goto('https://accounts.zoho.com/signin');
    await page.waitForTimeout(3000);
    await page.screenshot({ path: './zoho-01-initial.png' });

    console.log('🔐 Logging in...');
    // Enter email
    await page.fill('#login_id', ZOHO_EMAIL);
    await page.click('#nextbtn');
    await page.waitForTimeout(3000);
    await page.screenshot({ path: './zoho-02-after-email.png' });

    // Enter password
    await page.fill('#password', ZOHO_PASSWORD);
    await page.click('#nextbtn');
    await page.waitForTimeout(5000);
    await page.screenshot({ path: './zoho-03-logged-in.png' });

    // Now navigate to Zoho Social
    console.log('🌐 Navigating to Zoho Social...');
    await page.goto(`https://social.zoho.com/social/wilsoninc/${SOCIAL_PROFILE_ID}/Home.do`);
    await page.waitForTimeout(5000);
    await page.screenshot({ path: './zoho-04-social-home.png' });

    // Navigate to new post
    console.log('📝 Creating new post...');
    await page.goto(`https://social.zoho.com/social/wilsoninc/${SOCIAL_PROFILE_ID}/NewPost.do`);
    await page.waitForTimeout(5000);
    await page.screenshot({ path: './zoho-05-compose.png' });

    // Load and enter content
    const content = loadContent('./content/social-post-002.md');

    // Find and fill the content textarea
    await page.waitForSelector('textarea[name="content"], [data-testid="content-textarea"], .post-content, div[contenteditable="true"]', { timeout: 10000 });
    await page.fill('textarea[name="content"], [data-testid="content-textarea"], .post-content, div[contenteditable="true"]', content);
    await page.waitForTimeout(1000);
    await page.screenshot({ path: './zoho-06-content.png' });

    // Select channels (Twitter and LinkedIn)
    console.log('📡 Selecting channels...');

    // Click "Publish" button
    await page.click('button:has-text("Publish"), button:has-text("Post"), [data-testid="publish-btn"]');
    await page.waitForTimeout(5000);

    // Save success screenshot
    await page.screenshot({ path: './zoho-07-posted.png' });

    console.log('✅ Post published!');
    console.log('📸 Screenshot saved: zoho-07-posted.png');

  } catch (error) {
    console.error('❌ Error:', error.message);
    await page.screenshot({ path: './zoho-error.png' });
  } finally {
    await browser.close();
  }
})();
