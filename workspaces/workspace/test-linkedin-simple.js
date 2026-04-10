// Simple LinkedIn test - direct approach
const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  let browser;
  let page;

  try {
    console.log('Starting LinkedIn test...');

    // Load content
    const content = fs.readFileSync('./content/social-post-002.md', 'utf8');
    const linkedinContent = content.split('---\n')[4].trim();
    console.log('Content loaded:', linkedinContent.substring(0, 50) + '...');

    // Launch browser
    browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({ viewport: { width: 1280, height: 800 } });

    // Import cookies
    if (fs.existsSync('./cookies-linkedin.json')) {
      const cookies = JSON.parse(fs.readFileSync('./cookies-linkedin.json'));
      await context.addCookies(cookies);
      console.log('Cookies imported');
    }

    page = await context.newPage();

    // Go to LinkedIn
    await page.goto('https://www.linkedin.com/feed/', { waitUntil: 'networkidle' });
    await page.waitForTimeout(3000);
    console.log('Page loaded');

    // Screenshot initial state
    await page.screenshot({ path: './debug-li-1-initial.png' });

    // Click on the "Start a post" text box in the feed
    console.log('Clicking Start a post...');
    const startPostSelectors = [
      'span:text-matches("Start a post", "i")',
      'button:has-text("Start a post")',
      '[data-test-id="share-box-trigger"]',
      '.share-box-feed-entry__trigger',
      'div[role="button"]:has-text("Start a post")'
    ];

    let clicked = false;
    for (const selector of startPostSelectors) {
      try {
        const el = page.locator(selector).first();
        if (await el.count() > 0 && await el.isVisible()) {
          await el.click();
          console.log(`Clicked: ${selector}`);
          clicked = true;
          break;
        }
      } catch (e) {}
    }

    if (!clicked) {
      // Fallback: try to find by text content
      await page.evaluate(() => {
        const elements = document.querySelectorAll('*');
        for (const el of elements) {
          if (el.textContent?.includes('Start a post') && el.click) {
            el.click();
            return;
          }
        }
      });
    }

    // Wait for modal to appear
    console.log('Waiting for modal...');
    await page.waitForTimeout(5000);
    await page.screenshot({ path: './debug-li-2-modal.png' });

    // Check if modal opened
    const modalInfo = await page.evaluate(() => {
      const dialogs = document.querySelectorAll('[role="dialog"]');
      const info = [];
      for (const dialog of dialogs) {
        const style = window.getComputedStyle(dialog);
        if (style.display !== 'none') {
          info.push({
            visible: true,
            hasEditor: !!dialog.querySelector('[contenteditable="true"]'),
            text: dialog.innerText?.substring(0, 100)
          });
        }
      }
      return info;
    });
    console.log('Modal info:', modalInfo);

    if (modalInfo.length === 0) {
      console.log('No modal found - trying direct post URL');
      await page.goto('https://www.linkedin.com/post/new', { waitUntil: 'networkidle' });
      await page.waitForTimeout(3000);
      await page.screenshot({ path: './debug-li-2b-direct.png' });
    }

    // Find and fill the editor
    console.log('Finding editor...');
    const editor = page.locator('[contenteditable="true"]').first();

    if (await editor.count() === 0) {
      throw new Error('No contenteditable editor found');
    }

    console.log('Entering content...');
    await editor.click();

    // Clear and type content
    await page.keyboard.press('Control+a');
    await page.keyboard.press('Delete');

    // Type with small delays
    for (const char of linkedinContent) {
      await page.keyboard.press(char === '\n' ? 'Enter' : char);
    }

    await page.waitForTimeout(2000);
    await page.screenshot({ path: './debug-li-3-content.png' });

    // Find and click Post button
    console.log('Finding Post button...');
    const postButtons = await page.locator('button').all();
    let postBtn = null;

    for (const btn of postButtons) {
      const text = await btn.textContent();
      if (text?.trim().toLowerCase() === 'post') {
        const isEnabled = await btn.isEnabled();
        console.log(`Found Post button, enabled: ${isEnabled}`);
        if (isEnabled) {
          postBtn = btn;
          break;
        }
      }
    }

    if (!postBtn) {
      // Try JavaScript approach
      console.log('Trying JavaScript click...');
      const clicked = await page.evaluate(() => {
        const buttons = document.querySelectorAll('button');
        for (const btn of buttons) {
          if (btn.textContent?.trim() === 'Post' && !btn.disabled) {
            btn.click();
            return true;
          }
        }
        return false;
      });

      if (!clicked) {
        throw new Error('Could not find enabled Post button');
      }
    } else {
      await postBtn.click();
      console.log('Clicked Post button');
    }

    // Wait and verify
    await page.waitForTimeout(5000);
    await page.screenshot({ path: './proof-linkedin-final.png' });

    // Check if back on feed
    const url = page.url();
    console.log('Final URL:', url);

    if (url.includes('/feed/')) {
      console.log('SUCCESS: Back on feed, post likely submitted');
    } else {
      console.log('WARNING: Not on feed, may need verification');
    }

    await browser.close();
  } catch (error) {
    console.error('Error:', error.message);
    if (page) {
      await page.screenshot({ path: './error-linkedin-final.png' }).catch(() => {});
    }
    if (browser) await browser.close();
    process.exit(1);
  }
})();
