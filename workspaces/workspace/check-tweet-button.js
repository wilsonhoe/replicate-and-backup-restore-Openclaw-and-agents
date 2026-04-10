// Check what the tweet button selector is on the new compose page
const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  let browser;
  try {
    console.log('Launching browser...');
    browser = await chromium.launch({ headless: false });
    const context = await browser.newContext();
    
    console.log('Loading Twitter cookies...');
    const twitterCookies = JSON.parse(fs.readFileSync('./cookies-twitter.json', 'utf8'));
    await context.addCookies(twitterCookies);
    console.log('Twitter cookies imported');
    
    const page = await context.newPage();
    console.log('Navigating to x.com/compose/tweet...');
    await page.goto('https://x.com/compose/tweet');
    await page.waitForTimeout(3000);
    
    // Wait for redirect to complete
    await page.waitForURL('**/compose/post**', { timeout: 5000 });
    const url = await page.url();
    console.log('Final URL:', url);
    
    // Wait for page to load
    await page.waitForTimeout(3000);
    
    // Try to find the tweet button using various possible selectors
    const buttonSelectors = [
      '[data-testid="tweetButton"]',
      '[data-testid="tweetButtonInline"]',
      '[data-testid="tweetButton"] div[role="button"]',
      'button[data-testid="tweetButton"]',
      '[role="button"]:has-text("Post")',
      'button:has-text("Post")',
      '[aria-label="Post"]',
      'button[aria-label="Post"]'
    ];
    
    for (const selector of buttonSelectors) {
      try {
        const exists = await page.locator(selector).first().isVisible();
        if (exists) {
          console.log(`Button selector '${selector}' found and visible`);
          
          // Check if it's enabled
          const isEnabled = await page.evaluate((sel) => {
            const elem = document.querySelector(sel);
            return elem && !elem.disabled && elem.getAttribute('aria-disabled') !== 'true';
          }, selector);
          console.log(`Button is enabled: ${isEnabled}`);
          break;
        }
      } catch (error) {
        // Selector not found or not visible, continue to next
        continue;
      }
    }
    
    await browser.close();
    console.log('Button check completed');
  } catch (error) {
    console.error('Error:', error);
    if (browser) await browser.close();
  }
})();
