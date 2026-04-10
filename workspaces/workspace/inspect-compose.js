// Inspect the actual compose page to find correct selectors
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
    
    // Take a screenshot to see what we're working with
    await page.screenshot({ path: './inspect-compose.png' });
    console.log('Screenshot saved');
    
    // Try to find the textarea using various possible selectors
    const selectors = [
      '[data-testid="tweetTextarea_0"]',
      '[data-testid="tweetTextarea_1"]',
      '[data-testid="tweetTextarea"]',
      '[role="textbox"]',
      '[contenteditable="true"]',
      '.public-DraftStyleDefault-block',
      '[data-testid="editor"]',
      '[data-testid="tweetBox"]'
    ];
    
    for (const selector of selectors) {
      try {
        const exists = await page.locator(selector).first().isVisible();
        if (exists) {
          console.log(`Selector '${selector}' found and visible`);
          
          // Try to get the element and see if we can interact with it
          const element = page.locator(selector).first();
          await element.click();
          await page.waitForTimeout(500);
          
          // Try typing something simple
          await element.press('Control+a');
          await element.press('Delete');
          await element.type('Test from OpenClaw inspection');
          
          await page.waitForTimeout(1000);
          console.log(`Successfully interacted with '${selector}'`);
          break;
        }
      } catch (error) {
        // Selector not found or not visible, continue to next
        continue;
      }
    }
    
    // Also check what's in the DOM
    const pageContent = await page.content();
    console.log('Page contains "tweet":', pageContent.includes('tweet'));
    console.log('Page contains "textarea":', pageContent.includes('textarea'));
    console.log('Page contains "compose":', pageContent.includes('compose'));
    
    await browser.close();
    console.log('Inspection completed');
  } catch (error) {
    console.error('Error:', error);
    if (browser) await browser.close();
  }
})();
