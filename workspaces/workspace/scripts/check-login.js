const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const context = browser.contexts()[0];
  const page = await context.newPage();
  await page.goto('https://twitter.com');
  await page.waitForTimeout(3000);
  const url = page.url();
  console.log('Current URL:', url);
  const isLoggedIn = await page.$('[data-testid="SideNav_AccountSwitcher_Button"]') !== null;
  console.log('Is logged in to Twitter:', isLoggedIn);
  
  // Take a screenshot
  await page.screenshot({ path: '/home/wls/.openclaw/workspace/content/twitter-check.png' });
  console.log('Screenshot saved');
  
  await browser.close();
})();