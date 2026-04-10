// LinkedIn posting with stealth settings to avoid detection
const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  let browser;
  let page;

  try {
    console.log('Starting LinkedIn stealth test...');

    // Load content
    const content = fs.readFileSync('./content/social-post-002.md', 'utf8');
    const linkedinContent = content.split('---\n')[4].trim();
    console.log('Content loaded');

    // Launch browser with stealth settings
    browser = await chromium.launch({
      headless: true,
      args: [
        '--disable-blink-features=AutomationControlled',
        '--disable-web-security',
        '--disable-features=IsolateOrigins,site-per-process',
        '--disable-site-isolation-trials'
      ]
    });

    const context = await browser.newContext({
      viewport: { width: 1920, height: 1080 },
      userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
      locale: 'en-US',
      timezoneId: 'Asia/Singapore',
      permissions: ['notifications'],
      // Anti-detection measures
      bypassCSP: true,
      javaScriptEnabled: true
    });

    // Add stealth scripts to evade detection
    await context.addInitScript(() => {
      // Override navigator.webdriver
      Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
      });

      // Override permissions
      const originalQuery = window.navigator.permissions.query;
      window.navigator.permissions.query = (parameters) => (
        parameters.name === 'notifications' || parameters.name === 'clipboard-read' || parameters.name === 'clipboard-write'
          ? Promise.resolve({ state: 'prompt', onchange: null, addEventListener: () => {}, removeEventListener: () => {} })
          : originalQuery(parameters)
      );

      // Override plugins
      Object.defineProperty(navigator, 'plugins', {
        get: () => [1, 2, 3, 4, 5]
      });

      // Override languages
      Object.defineProperty(navigator, 'languages', {
        get: () => ['en-US', 'en']
      });
    });

    // Import cookies
    if (fs.existsSync('./cookies-linkedin.json')) {
      const cookies = JSON.parse(fs.readFileSync('./cookies-linkedin.json'));
      await context.addCookies(cookies);
      console.log('Cookies imported');
    } else {
      throw new Error('No LinkedIn cookies found');
    }

    page = await context.newPage();

    // Navigate to feed
    console.log('Navigating to LinkedIn...');
    await page.goto('https://www.linkedin.com/feed/', {
      waitUntil: 'domcontentloaded',
      timeout: 30000
    });

    // Wait for page to stabilize
    await page.waitForTimeout(5000);

    // Check if we're logged in
    const pageInfo = await page.evaluate(() => ({
      url: window.location.href,
      hasStartPost: !!document.querySelector('[data-test-id="share-box-trigger"]') ||
                    !!document.querySelector('.share-box-feed-entry__trigger') ||
                    !!Array.from(document.querySelectorAll('*')).find(el =>
                      el.textContent?.toLowerCase().includes('start a post')),
      title: document.title
    }));

    console.log('Page state:', pageInfo);

    if (!pageInfo.hasStartPost) {
      console.log('Not logged in or Start a post not found');
      await page.screenshot({ path: './error-not-logged-in.png' });
      await browser.close();
      process.exit(1);
    }

    // Click Start a post
    console.log('Clicking Start a post...');
    let clicked = false;

    // Try JavaScript click first
    clicked = await page.evaluate(() => {
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      let node;
      while (node = walker.nextNode()) {
        if (node.textContent.toLowerCase().includes('start a post')) {
          let el = node.parentElement;
          for (let i = 0; i < 10 && el; i++) {
            if (el.click) {
              el.scrollIntoView({ block: 'center', behavior: 'instant' });
              // Multiple click attempts
              el.click();
              el.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
              el.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
              el.dispatchEvent(new MouseEvent('click', { bubbles: true }));
              return true;
            }
            el = el.parentElement;
          }
        }
      }
      return false;
    });

    if (!clicked) {
      throw new Error('Could not click Start a post');
    }

    console.log('Clicked Start a post, waiting for modal...');
    await page.waitForTimeout(5000);
    await page.screenshot({ path: './debug-after-click.png' });

    // Wait for contenteditable with retry
    console.log('Waiting for editor...');
    let editor = null;
    let attempts = 0;
    const maxAttempts = 10;

    while (!editor && attempts < maxAttempts) {
      attempts++;
      editor = await page.$('[contenteditable="true"]');
      if (!editor) {
        await page.waitForTimeout(1000);
      }
    }

    if (!editor) {
      console.log('Editor not found after waiting');
      await page.screenshot({ path: './error-no-editor.png' });
      await browser.close();
      process.exit(1);
    }

    console.log('Editor found!');

    // Enter content
    console.log('Entering content...');
    await editor.click();
    await page.keyboard.press('Control+a');
    await page.keyboard.press('Delete');

    // Type content slowly
    for (const char of linkedinContent) {
      await page.keyboard.press(char === '\n' ? 'Enter' : char);
      await page.waitForTimeout(10);
    }

    await page.waitForTimeout(2000);
    await page.screenshot({ path: './debug-content-entered.png' });
    console.log('Content entered');

    // Find and click Post button
    console.log('Finding Post button...');
    let postClicked = false;
    let postAttempts = 0;
    const maxPostAttempts = 30;

    while (!postClicked && postAttempts < maxPostAttempts) {
      postAttempts++;

      // Check if button is enabled and click it
      const result = await page.evaluate(() => {
        const buttons = document.querySelectorAll('button');
        for (const btn of buttons) {
          const text = btn.textContent?.trim().toLowerCase();
          if (text === 'post' && !btn.disabled) {
            btn.scrollIntoView({ block: 'center' });
            btn.click();
            btn.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
            btn.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
            btn.dispatchEvent(new MouseEvent('click', { bubbles: true }));
            return { clicked: true, text: btn.textContent };
          }
        }
        return { clicked: false, foundDisabled: Array.from(buttons).some(b =>
          b.textContent?.trim().toLowerCase() === 'post' && b.disabled
        )};
      });

      if (result.clicked) {
        postClicked = true;
        console.log(`Post button clicked after ${postAttempts} attempts`);
        break;
      }

      // Trigger input event every 5 attempts to enable button
      if (postAttempts % 5 === 0) {
        console.log(`Button still disabled, triggering input events...`);
        await page.evaluate(() => {
          const editor = document.querySelector('[contenteditable="true"]');
          if (editor) {
            editor.dispatchEvent(new InputEvent('input', { bubbles: true, inputType: 'insertText' }));
            editor.dispatchEvent(new Event('change', { bubbles: true }));
          }
        });
      }

      await page.waitForTimeout(500);
    }

    if (!postClicked) {
      console.log('Could not click Post button');
      await page.screenshot({ path: './error-post-button.png' });
      await browser.close();
      process.exit(1);
    }

    // Wait for post to submit
    await page.waitForTimeout(5000);
    await page.screenshot({ path: './proof-linkedin-posted.png' });
    console.log('Done! Screenshot saved: proof-linkedin-posted.png');

    await browser.close();

  } catch (error) {
    console.error('Error:', error.message);
    if (page) {
      await page.screenshot({ path: './error-linkedin.png' }).catch(() => {});
    }
    if (browser) await browser.close();
    process.exit(1);
  }
})();
