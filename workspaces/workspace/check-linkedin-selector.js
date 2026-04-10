// Check what the LinkedIn share box selector is
const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  let browser;
  try {
    console.log('Launching browser...');
    browser = await chromium.launch({ headless: false });
    const context = await browser.newContext();
    
    console.log('Loading LinkedIn cookies...');
    let linkedinCookiesPath = './cookies-linkedin.json';
    if (!fs.existsSync(linkedinCookiesPath)) {
      linkedinCookiesPath = '/home/wls/.openclaw/browser-data-linkedin/cookies.json';
    }
    if (fs.existsSync(linkedinCookiesPath)) {
      const linkedinCookies = JSON.parse(fs.readFileSync(linkedinCookiesPath));
      await context.addCookies(linkedinCookies);
      console.log('LinkedIn cookies imported successfully');
    } else {
      throw new Error('LinkedIn cookies file not found');
    }
    
    const page = await context.newPage();
    console.log('Navigating to LinkedIn feed...');
    await page.goto('https://www.linkedin.com/feed/');
    await page.waitForTimeout(3000);
    
    const url = await page.url();
    console.log('Current URL:', url);
    
    // Wait for page to load
    await page.waitForTimeout(3000);
    
    // Try to find the share box using various possible selectors
    const selectors = [
      '[data-testid="share-box-placeholder"]',
      '[data-testid="share-box"]',
      '[role="button"][aria-label="Start a post"]',
      '[aria-label="Start a post"]',
      '.share-box-feed-entry__trigger',
      '.feed-share-update-v2__container',
      '[data-testid="feed-share-input"]',
      '[placeholder*="What do you want to talk about"]',
      '[contenteditable="true"][data-placeholder*="What do you want to talk about"]'
    ];
    
    for (const selector of selectors) {
      try {
        const count = await page.locator(selector).count();
        if (count > 0) {
          const first = page.locator(selector).first();
          const visible = await first.isVisible();
          if (visible) {
            console.log(`Selector '${selector}' found (${count} elements), first is visible`);
            
            // Try clicking it to see if it opens the editor
            await first.click();
            await page.waitForTimeout(2000);
            
            // Check if editor appears
            const editorSelectors = [
              '[data-testid="rich-text-editor"]',
              '[contenteditable="true"][role="textbox"]',
              '.rich-text-editor'
            ];
            
            for (const editorSel of editorSelectors) {
              try {
                const editorCount = await page.locator(editorSel).count();
                if (editorCount > 0) {
                  const editorVisible = await page.locator(editorSel).first().isVisible();
                  if (editorVisible) {
                    console.log(`  -> Editor found with selector '${editorSel}'`);
                  }
                }
              } catch (e) {}
            }
            break;
          }
        }
      } catch (error) {
        // Selector not found or error, continue to next
        continue;
      }
    }
    
    await browser.close();
    console.log('LinkedIn selector check completed');
  } catch (error) {
    console.error('Error:', error);
    if (browser) await browser.close();
  }
})();
