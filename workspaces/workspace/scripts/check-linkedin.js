const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const context = browser.contexts()[0];
  const page = await context.newPage();
  await page.goto('https://www.linkedin.com');
  await page.waitForTimeout(3000);
  const url = page.url();
  console.log('Current URL:', url);
  const isLoggedIn = await page.$('[data-testid="global-nav-typeahead"]') !== null || 
                     await page.$('[data-testid="nav-settings__dropdown-trigger"]') !== null;
  console.log('Is logged in to LinkedIn:', isLoggedIn);
  
  // Take a screenshot
  await page.screenshot({ path: '/home/wls/.openclaw/workspace/content/linkedin-check.png' });
  console.log('LinkedIn screenshot saved');
  
  await browser.close();
})();