// Test navigating to compose page and interacting with textarea
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
    
    const url = await page.url();
    console.log('Current URL:', url);
    
    // Check if textarea is present
    const textareaExists = await page.locator('[data-testid="tweetTextarea_0"]').isVisible();
    console.log('Textarea visible:', textareaExists);
    
    if (textareaExists) {
      console.log('Clicking textarea...');
      await page.locator('[data-testid="tweetTextarea_0"]').first().click();
      await page.waitForTimeout(1000);
      
      console.log('Filling textarea...');
      await page.fill('[data-testid="tweetTextarea_0"]', 'Test tweet from OpenClaw');
      
      // Trigger events
      await page.evaluate(() => {
        const textarea = document.querySelector('[data-testid="tweetTextarea_0"]');
        if (textarea) {
          textarea.dispatchEvent(new Event('input', { bubbles: true }));
          textarea.dispatchEvent(new Event('change', { bubbles: true }));
        }
      });
      
      await page.waitForTimeout(1000);
      
      // Check if button is enabled
      const isButtonEnabled = await page.evaluate(() => {
        const btn = document.querySelector('[data-testid="tweetButton"]');
        return btn && !btn.disabled && btn.getAttribute('aria-disabled') !== 'true';
      });
      console.log('Tweet button enabled:', isButtonEnabled);
      
      await page.screenshot({ path: './compose-test-result.png' });
      console.log('Screenshot saved');
    } else {
      console.log('Textarea not found!');
      await page.screenshot({ path: './compose-test-error.png' });
    }
    
    await browser.close();
    console.log('Compose test completed');
  } catch (error) {
    console.error('Error:', error);
    if (browser) await browser.close();
  }
})();
