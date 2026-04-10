// Simple test to see if LinkedIn cookies work
const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  let browser;
  try {
    console.log('Testing LinkedIn cookie import...');
    
    browser = await chromium.launch({ headless: false });
    const context = await browser.newContext();
    
    // Import LinkedIn cookies
    const linkedinCookies = JSON.parse(fs.readFileSync('./cookies-linkedin.json', 'utf8'));
    await context.addCookies(linkedinCookies);
    console.log('LinkedIn cookies imported');
    
    const page = await context.newPage();
    await page.goto('https://www.linkedin.com');
    await page.waitForTimeout(3000);
    
    const url = await page.url();
    console.log('Current URL:', url);
    
    // Check if we're logged in by looking for user elements
    const isLoggedIn = await page.locator('#global-nav-typeahead').isVisible();
    console.log('Logged in to LinkedIn:', isLoggedIn);
    
    await page.screenshot({ path: './test-linkedin-cookies.png' });
    
    await browser.close();
    console.log('LinkedIn test completed successfully');
  } catch (error) {
    console.error('Error:', error);
    if (browser) await browser.close();
  }
})();
