// Post Day 2 Content via Zoho Social Browser Automation
const { chromium } = require('playwright');
const fs = require('fs');

const ZOHO_EMAIL = 'lisamolbot@gmail.com';
const ZOHO_PASSWORD = 'mv9p@T8iRWWQwBw';

// Load tokens
const tokens = JSON.parse(fs.readFileSync('./zoho-tokens.json', 'utf8'));

// Day 2 Content
const TWITTER_CONTENT = `Stop guessing your automation ROI. I built a calculator.

Example: 5 hrs/week × $50/hr = $250/week = $13K/year*

*Based on mid-level freelancer rates (SoloHourly, 2026). Your results may vary.

What would you automate first? #Automation #ROI`;

const LINKEDIN_CONTENT = `Most solopreneurs I talk to are bleeding money on repetitive tasks.

I built an ROI calculator to show the real numbers.

Example calculation:
- 5 hours/week on manual data entry
- $50/hour value (mid-level freelancer rate, SoloHourly 2026)
- $250/week saved
- $13,000/year recovered*

*This is an example. Your actual savings depend on your hourly rate and tasks automated.

The best automation isn't the fanciest—it's the one that pays for itself fastest.

What's one task you'd automate today if you could?

Source: SoloHourly. (2026). Average freelance rates in 2026. https://solohourly.com/guides/average-freelance-rates-2026`;

(async () => {
  console.log('🌐 Launching browser for Zoho Social posting...');
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    // Navigate to Zoho Social
    console.log('🔐 Logging into Zoho Social...');
    await page.goto('https://social.zoho.com');
    await page.waitForTimeout(3000);

    // Check if already logged in
    const currentUrl = page.url();
    if (currentUrl.includes('accounts.zoho.com/signin')) {
      // Enter email
      await page.fill('#login_id', ZOHO_EMAIL);
      await page.click('#nextbtn');
      await page.waitForTimeout(2000);

      // Enter password
      await page.fill('#password', ZOHO_PASSWORD);
      await page.click('#nextbtn');
      await page.waitForTimeout(5000);
    }

    // Navigate to New Post
    console.log('📝 Creating new post...');
    await page.goto('https://social.zoho.com');
    await page.waitForTimeout(5000);
    await page.screenshot({ path: './zoho-day2-01-home.png' });

    // Click New Post button
    await page.click('button:has-text("New Post"), a:has-text("New Post"), [data-testid="new-post-btn"]');
    await page.waitForTimeout(3000);
    await page.screenshot({ path: './zoho-day2-02-compose.png' });

    // Enter LinkedIn content (longer version)
    console.log('📄 Entering LinkedIn content...');
    await page.waitForSelector('textarea, div[contenteditable="true"]', { timeout: 10000 });
    await page.fill('textarea, div[contenteditable="true"]', LINKEDIN_CONTENT);
    await page.waitForTimeout(1000);

    // Select Twitter channel
    console.log('📡 Selecting Twitter channel...');
    await page.click('text=Twitter, [data-testid="twitter-channel"], .twitter-icon');
    await page.waitForTimeout(1000);

    // Select LinkedIn channel
    console.log('📡 Selecting LinkedIn channel...');
    await page.click('text=LinkedIn, [data-testid="linkedin-channel"], .linkedin-icon');
    await page.waitForTimeout(1000);

    // Take screenshot before posting
    await page.screenshot({ path: './zoho-day2-03-ready.png' });

    // Click Publish
    console.log('🚀 Publishing...');
    await page.click('button:has-text("Publish"), button:has-text("Post"), [data-testid="publish-btn"]');
    await page.waitForTimeout(5000);

    // Take success screenshot
    await page.screenshot({ path: './zoho-day2-04-success.png' });

    console.log('✅ Day 2 posted successfully!');
    console.log('📸 Screenshots saved: zoho-day2-*.png');

  } catch (error) {
    console.error('❌ Error:', error.message);
    await page.screenshot({ path: './zoho-day2-error.png' });
  } finally {
    await browser.close();
  }
})();
