// Basic test: launch browser, import cookies, go to twitter.com
const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  let browser;
  try {
    console.log('Launching browser...');
    browser = await chromium.launch({ headless: false }); // Visible so we can see
    const context = await browser.newContext();
    
    console.log('Loading Twitter cookies...');
    const twitterCookies = JSON.parse(fs.readFileSync('./cookies-twitter.json', 'utf8'));
    await context.addCookies(twitterCookies);
    console.log('Twitter cookies imported');
    
    const page = await context.newPage();
    console.log('Navigating to x.com...');
    await page.goto('https://x.com');
    await page.waitForTimeout(3000);
    
    const url = await page.url();
    console.log('Current URL:', url);
    
    await page.screenshot({ path: './basic-test-result.png' });
    console.log('Screenshot saved');
    
    await browser.close();
    console.log('Test completed successfully');
  } catch (error) {
    console.error('Error:', error);
    if (browser) await browser.close();
  }
})();
