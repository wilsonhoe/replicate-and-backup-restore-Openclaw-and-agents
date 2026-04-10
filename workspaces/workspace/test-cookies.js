// Simple test to see if cookies work
const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  let browser;
  try {
    console.log('Testing cookie import...');
    
    browser = await chromium.launch({ headless: false });
    const context = await browser.newContext();
    
    // Import Twitter cookies
    const twitterCookies = JSON.parse(fs.readFileSync('./cookies-twitter.json', 'utf8'));
    await context.addCookies(twitterCookies);
    console.log('Twitter cookies imported');
    
    const page = await context.newPage();
    await page.goto('https://x.com');
    await page.waitForTimeout(3000);
    
    const url = await page.url();
    console.log('Current URL:', url);
    
    // Check if we're logged in by looking for user elements
    const isLoggedIn = await page.locator('[data-testid="SideNav_AccountSwitcher_Button"]').isVisible();
    console.log('Logged in to Twitter:', isLoggedIn);
    
    await page.screenshot({ path: './test-twitter-cookies.png' });
    
    await browser.close();
    console.log('Test completed successfully');
  } catch (error) {
    console.error('Error:', error);
    if (browser) await browser.close();
  }
})();
