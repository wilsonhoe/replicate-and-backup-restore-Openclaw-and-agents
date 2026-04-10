// LinkedIn debug script - comprehensive diagnostics
const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  let browser;
  let page;

  try {
    console.log('=== LinkedIn Debug Script ===');

    // Launch browser
    browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
      viewport: { width: 1280, height: 800 },
      userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    });

    // Import cookies
    if (fs.existsSync('./cookies-linkedin.json')) {
      const cookies = JSON.parse(fs.readFileSync('./cookies-linkedin.json'));
      await context.addCookies(cookies);
      console.log('✓ Cookies imported:', cookies.length, 'cookies');

      // Check for li_at cookie
      const liat = cookies.find(c => c.name === 'li_at');
      if (liat) {
        console.log('✓ li_at cookie found, expires:', new Date(liat.expirationDate * 1000).toISOString());
      } else {
        console.log('✗ li_at cookie NOT found - authentication will fail');
      }
    } else {
      console.log('✗ No cookies file found');
      process.exit(1);
    }

    page = await context.newPage();

    // Navigate to feed
    console.log('\n--- Navigating to LinkedIn feed ---');
    await page.goto('https://www.linkedin.com/feed/', { waitUntil: 'networkidle' });
    await page.waitForTimeout(5000);

    const url = page.url();
    console.log('Current URL:', url);

    // Check login status
    console.log('\n--- Checking login status ---');
    const loginCheck = await page.evaluate(() => {
      const indicators = {
        hasStartPost: !!document.querySelector('[data-test-id="share-box-trigger"]') ||
                      !!Array.from(document.querySelectorAll('*')).find(el =>
                        el.textContent?.toLowerCase().includes('start a post')),
        hasLoginButton: !!document.querySelector('button[data-tracking-control-name="guest_home-page-basic_sign-in-button"]') ||
                       !!document.querySelector('a[href*="login"]'),
        hasPasswordField: !!document.querySelector('input[type="password"]'),
        hasFeedContent: !!document.querySelector('.feed-main') ||
                       !!document.querySelector('.scaffold-layout__main'),
        pageTitle: document.title,
        hasSecurityChallenge: !!document.querySelector('.challenge-form') ||
                             !!document.querySelector('[data-test-id="security-challenge"]') ||
                             document.body.innerText.toLowerCase().includes('security check') ||
                             document.body.innerText.toLowerCase().includes('verify'),
        bodyText: document.body.innerText.substring(0, 500)
      };
      return indicators;
    });

    console.log('Login check results:', JSON.stringify(loginCheck, null, 2));

    // Screenshot initial state
    await page.screenshot({ path: './debug-li-01-initial.png', fullPage: true });
    console.log('✓ Screenshot saved: debug-li-01-initial.png');

    if (loginCheck.hasSecurityChallenge) {
      console.log('\n⚠️ SECURITY CHALLENGE DETECTED - LinkedIn is blocking automation');
      await browser.close();
      process.exit(1);
    }

    if (!loginCheck.hasStartPost && (loginCheck.hasLoginButton || loginCheck.hasPasswordField)) {
      console.log('\n✗ NOT LOGGED IN - Redirected to login page despite cookies');
      console.log('  This means the cookies are expired or invalid');
      await browser.close();
      process.exit(1);
    }

    if (!loginCheck.hasStartPost) {
      console.log('\n⚠️ No "Start a post" button found - checking page structure...');

      // Get more page info
      const pageStructure = await page.evaluate(() => {
        const shareBox = document.querySelector('.share-box-feed-entry__wrapper');
        const shareTrigger = document.querySelector('[data-test-id="share-box-trigger"]');
        const allButtons = Array.from(document.querySelectorAll('button')).slice(0, 10).map(b => ({
          text: b.textContent?.trim().substring(0, 50),
          class: b.className?.substring(0, 50),
          ariaLabel: b.getAttribute('aria-label')?.substring(0, 50)
        }));

        return {
          hasShareBox: !!shareBox,
          hasShareTrigger: !!shareTrigger,
          buttonSamples: allButtons,
          htmlSnippet: document.body.innerHTML.substring(0, 2000)
        };
      });

      console.log('Page structure:', JSON.stringify(pageStructure, null, 2));
      await browser.close();
      process.exit(1);
    }

    console.log('\n✓ Logged in - found "Start a post" button');

    // Try to click Start a post using multiple methods
    console.log('\n--- Attempting to open post composer ---');

    // Method 1: JavaScript tree walker
    console.log('Method 1: JavaScript tree walker...');
    const clicked = await page.evaluate(() => {
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      let node;
      while (node = walker.nextNode()) {
        if (node.textContent.toLowerCase().includes('start a post')) {
          let el = node.parentElement;
          for (let i = 0; i < 10 && el; i++) {
            if (el.click && (el.tagName === 'BUTTON' || el.getAttribute('role') === 'button' || el.tagName === 'DIV')) {
              el.scrollIntoView({ block: 'center', behavior: 'instant' });
              el.click();
              return {
                success: true,
                method: 'tree-walker',
                element: el.tagName,
                role: el.getAttribute('role'),
                className: el.className?.substring(0, 50)
              };
            }
            el = el.parentElement;
          }
        }
      }
      return { success: false, method: 'tree-walker' };
    });
    console.log('Tree walker result:', clicked);

    await page.waitForTimeout(3000);
    await page.screenshot({ path: './debug-li-02-after-click.png' });

    // Check if modal opened
    let modalState = await page.evaluate(() => {
      const dialogs = document.querySelectorAll('[role="dialog"]');
      const visibleDialogs = Array.from(dialogs).filter(d => {
        const style = window.getComputedStyle(d);
        return style.display !== 'none' && style.visibility !== 'hidden';
      });

      // Look for editor with broader search
      const allContentEditables = document.querySelectorAll('[contenteditable]');
      const allTextboxes = document.querySelectorAll('[role="textbox"]');
      const allTextareas = document.querySelectorAll('textarea');

      return {
        totalDialogs: dialogs.length,
        visibleDialogs: visibleDialogs.length,
        allContentEditables: allContentEditables.length,
        allTextboxes: allTextboxes.length,
        allTextareas: allTextareas.length,
        dialogInfo: visibleDialogs.map(d => ({
          className: d.className?.substring(0, 50),
          hasEditor: !!d.querySelector('[contenteditable="true"]'),
          editorCount: d.querySelectorAll('[contenteditable="true"]').length,
          textboxCount: d.querySelectorAll('[role="textbox"]').length,
          text: d.innerText?.substring(0, 200),
          html: d.innerHTML?.substring(0, 500)
        }))
      };
    });
    console.log('Modal state after click:', JSON.stringify(modalState, null, 2));

    if (modalState.visibleDialogs === 0) {
      console.log('\n⚠️ Modal did not open. Trying Method 2...');

      // Method 2: Playwright locator
      console.log('Method 2: Playwright locator...');
      const selectors = [
        'span:text-matches("Start a post", "i")',
        'button:has-text("Start a post")',
        '[data-test-id="share-box-trigger"]',
        '.share-box-feed-entry__trigger'
      ];

      for (const selector of selectors) {
        try {
          const el = page.locator(selector).first();
          if (await el.count() > 0) {
            await el.click();
            console.log(`Clicked with selector: ${selector}`);
            await page.waitForTimeout(3000);
            break;
          }
        } catch (e) {
          console.log(`Selector failed: ${selector}`);
        }
      }

      await page.screenshot({ path: './debug-li-03-after-locator-click.png' });

      // Check modal again
      modalState = await page.evaluate(() => {
        const dialogs = document.querySelectorAll('[role="dialog"]');
        return {
          totalDialogs: dialogs.length,
          visibleDialogs: Array.from(dialogs).filter(d => {
            const style = window.getComputedStyle(d);
            return style.display !== 'none' && style.visibility !== 'hidden';
          }).length
        };
      });
      console.log('Modal state after locator click:', modalState);
    }

    // Method 3: Try direct post URL
    if (modalState.visibleDialogs === 0) {
      console.log('\n⚠️ Still no modal. Trying direct URL...');
      await page.goto('https://www.linkedin.com/post/new', { waitUntil: 'networkidle' });
      await page.waitForTimeout(3000);
      await page.screenshot({ path: './debug-li-04-direct-url.png' });

      const urlCheck = await page.evaluate(() => ({
        url: window.location.href,
        hasEditor: !!document.querySelector('[contenteditable="true"]') ||
                   !!document.querySelector('div[role="textbox"]'),
        pageTitle: document.title
      }));
      console.log('Direct URL result:', urlCheck);
    }

    // Wait a bit for modal to fully render
    await page.waitForTimeout(2000);

    // Final check for editor - comprehensive search
    const finalCheck = await page.evaluate(() => {
      // Find all potential editors
      const contentEditables = document.querySelectorAll('[contenteditable]');
      const textboxes = document.querySelectorAll('[role="textbox"]');
      const textareas = document.querySelectorAll('textarea');
      const editors = document.querySelectorAll('.ql-editor');

      // Get info about all editors found
      const allEditors = [];
      contentEditables.forEach((el, i) => {
        allEditors.push({
          type: 'contenteditable',
          index: i,
          tagName: el.tagName,
          contentEditable: el.contentEditable,
          className: el.className?.substring(0, 50),
          isVisible: window.getComputedStyle(el).display !== 'none',
          text: el.innerText?.substring(0, 50),
          inDialog: !!el.closest('[role="dialog"]')
        });
      });

      textboxes.forEach((el, i) => {
        allEditors.push({
          type: 'role=textbox',
          index: i,
          tagName: el.tagName,
          className: el.className?.substring(0, 50),
          isVisible: window.getComputedStyle(el).display !== 'none',
          inDialog: !!el.closest('[role="dialog"]')
        });
      });

      // Try to find the main editor
      const editor = document.querySelector('[contenteditable="true"]') ||
                    document.querySelector('div[role="textbox"]') ||
                    document.querySelector('.ql-editor');

      return {
        found: !!editor,
        totalContentEditables: contentEditables.length,
        totalTextboxes: textboxes.length,
        totalTextareas: textareas.length,
        totalQLEditors: editors.length,
        allEditors: allEditors,
        editorInfo: editor ? {
          tagName: editor.tagName,
          className: editor.className?.substring(0, 100),
          isVisible: window.getComputedStyle(editor).display !== 'none',
          inDialog: !!editor.closest('[role="dialog"]')
        } : null
      };
    });

    console.log('\n=== Final Editor Check ===');
    console.log(finalCheck);

    if (finalCheck.found && finalCheck.allEditors.length > 0) {
      console.log('\n✓ Editor found! Attempting to enter content...');

      // Try multiple selectors for the editor
      let editorFound = false;
      const selectors = [
        '[contenteditable="true"]',
        'div[role="textbox"]',
        '.ql-editor',
        '[data-test-id="editor-content"]'
      ];

      for (const selector of selectors) {
        try {
          const editor = page.locator(selector).first();
          if (await editor.count() > 0) {
            await editor.click();
            await page.keyboard.type('Test post from automation', { delay: 10 });
            editorFound = true;
            console.log(`✓ Content entered using selector: ${selector}`);
            break;
          }
        } catch (e) {
          console.log(`  Selector ${selector} failed: ${e.message}`);
        }
      }

      if (!editorFound) {
        console.log('✗ Could not click any editor with Playwright locators');
      }

      await page.waitForTimeout(1000);
      await page.screenshot({ path: './debug-li-05-content-entered.png' });

      // Check for Post button
      const postButton = await page.evaluate(() => {
        const buttons = document.querySelectorAll('button');
        for (const btn of buttons) {
          const text = btn.textContent?.trim().toLowerCase();
          if (text === 'post' && !btn.disabled) {
            return {
              found: true,
              text: btn.textContent?.trim(),
              disabled: btn.disabled
            };
          }
        }
        return { found: false };
      });
      console.log('Post button status:', postButton);
    } else {
      console.log('\n✗ Editor NOT found - cannot proceed with posting');
    }

    await browser.close();
    console.log('\n=== Debug Complete ===');

  } catch (error) {
    console.error('Error:', error.message);
    if (page) {
      await page.screenshot({ path: './debug-li-error.png' }).catch(() => {});
    }
    if (browser) await browser.close();
    process.exit(1);
  }
})();
