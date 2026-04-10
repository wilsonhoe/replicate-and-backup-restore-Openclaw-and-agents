// LinkedIn-only test script - Using Playwright locators
const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  let browser;
  let linkedinPage;

  try {
    console.log('Starting LinkedIn-only test...');

    // Load Day 2 LinkedIn content
    const content = fs.readFileSync('./content/social-post-002.md', 'utf8');
    const linkedinContent = content.split('---\n')[4].trim();
    console.log('LinkedIn content loaded:', linkedinContent.substring(0, 50) + '...');

    // Launch browser
    browser = await chromium.launch({ headless: true });
    const context = await browser.newContext();

    // Import LinkedIn cookies
    if (fs.existsSync('./cookies-linkedin.json')) {
      const linkedinCookies = JSON.parse(fs.readFileSync('./cookies-linkedin.json'));
      await context.addCookies(linkedinCookies);
      console.log('LinkedIn cookies imported');
    } else {
      throw new Error('LinkedIn cookies file not found');
    }

    // Go to LinkedIn feed
    linkedinPage = await context.newPage();
    await linkedinPage.goto('https://www.linkedin.com/feed/', { waitUntil: 'networkidle' });
    await linkedinPage.waitForTimeout(5000);
    console.log('Page loaded');

    // Debug: Check if we're logged in
    const pageInfo = await linkedinPage.evaluate(() => ({
      url: window.location.href,
      title: document.title,
      hasStartPost: !!document.querySelector('[data-test-id="share-box-trigger"]') ||
                    !!Array.from(document.querySelectorAll('*')).find(el => el.textContent?.includes('Start a post')),
      hasLoginForm: !!document.querySelector('input[type="password"]') ||
                    !!document.querySelector('#username')
    }));
    console.log('Page info:', pageInfo);

    // Try keyboard shortcut first - LinkedIn uses 'c' for compose
    console.log('Trying keyboard shortcut to open post composer...');
    await linkedinPage.keyboard.press('c');
    await linkedinPage.waitForTimeout(3000);

    // Check if modal opened
    let hasEditor = await linkedinPage.evaluate(() => {
      return !!(document.querySelector('[contenteditable="true"]') ||
                document.querySelector('div[role="textbox"]'));
    });

    // If keyboard didn't work, try clicking the share box directly using Playwright locators
    if (!hasEditor) {
      console.log('Keyboard shortcut failed, trying button click...');

      // Try JavaScript click first - more reliable for React
      console.log('Trying JavaScript click...');
      const clicked = await linkedinPage.evaluate(() => {
        // Find element containing "Start a post" text
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        let node;
        while (node = walker.nextNode()) {
          if (node.textContent.includes('Start a post')) {
            // Walk up to find clickable parent
            let el = node.parentElement;
            for (let i = 0; i < 5 && el; i++) {
              if (el.click && (el.tagName === 'BUTTON' || el.getAttribute('role') === 'button')) {
                el.scrollIntoView({ block: 'center' });
                el.click();
                return 'Clicked: ' + el.tagName + ' with role=' + el.getAttribute('role');
              }
              el = el.parentElement;
            }
            // Fallback: click the text node's parent
            node.parentElement.click();
            return 'Clicked parent of text node';
          }
        }
        return 'Start a post not found';
      });
      console.log('JS click result:', clicked);

      await linkedinPage.waitForTimeout(5000);

      hasEditor = await linkedinPage.evaluate(() => {
        return !!(document.querySelector('[contenteditable="true"]') ||
                  document.querySelector('div[role="textbox"]'));
      });

      if (!hasEditor) {
        // Try Playwright locators as fallback
        const selectors = [
          'button[aria-label*="post" i]',
          'button[aria-label*="create" i]',
          '[role="button"][aria-label*="post" i]',
          'button span:text-matches("Start a post", "i")',
          '.share-box-feed-entry__trigger',
          '[data-test-id="share-box-trigger"]'
        ];

        for (const selector of selectors) {
          try {
            const element = linkedinPage.locator(selector).first();
            if (await element.count() > 0) {
              await element.click({ timeout: 5000 });
              console.log(`Clicked element with selector: ${selector}`);
              await linkedinPage.waitForTimeout(5000);

              hasEditor = await linkedinPage.evaluate(() => {
                return !!(document.querySelector('[contenteditable="true"]') ||
                          document.querySelector('div[role="textbox"]'));
              });

              if (hasEditor) {
                console.log('Editor found after clicking!');
                break;
              }
            }
          } catch (e) {
            // Continue to next selector
          }
        }
      }
    }

    // Final fallback: try navigating to direct share URL only if still no editor
    if (!hasEditor) {
      console.log('Trying direct share URL...');
      await linkedinPage.goto('https://www.linkedin.com/post/new', { waitUntil: 'networkidle' });
      await linkedinPage.waitForTimeout(5000);
    }

    // Wait longer for React to render the modal
    console.log('Waiting for composer to load...');
    await linkedinPage.waitForTimeout(5000);
    await linkedinPage.screenshot({ path: './debug-linkedin-modal.png' });

    // Broad search for any input-like elements
    const inputElements = await linkedinPage.evaluate(() => ({
      contentEditables: document.querySelectorAll('[contenteditable]').length,
      textBoxes: document.querySelectorAll('[role="textbox"]').length,
      textareas: document.querySelectorAll('textarea').length,
      inputs: document.querySelectorAll('input[type="text"]').length,
      editors: document.querySelectorAll('.ql-editor').length,
      forms: document.querySelectorAll('form').length,
      visibleDialogs: Array.from(document.querySelectorAll('[role="dialog"]')).filter(d => {
        const style = window.getComputedStyle(d);
        return style.display !== 'none' && style.visibility !== 'hidden';
      }).length
    }));
    console.log('Input elements found:', inputElements);

    // Check for content editor
    console.log('Looking for content editor...');
    hasEditor = await linkedinPage.evaluate(() => {
      return !!(document.querySelector('[contenteditable="true"]') ||
                document.querySelector('div[role="textbox"]'));
    });
    console.log('Editor found:', hasEditor);

    if (!hasEditor) {
      // Try finding any input-like element in dialogs
      const dialogContent = await linkedinPage.evaluate(() => {
        const dialogs = document.querySelectorAll('[role="dialog"]');
        return Array.from(dialogs).map(d => ({
          className: d.className,
          hasInput: !!d.querySelector('[contenteditable], textarea, input'),
          text: d.innerText?.substring(0, 200)
        }));
      });
      console.log('Dialog contents:', dialogContent);
      throw new Error('Content editor not found');
    }

    // Enter content using Playwright locators
    console.log('Entering content...');

    // Try to find and fill the editor
    const editorSelectors = [
      '[contenteditable="true"]',
      'div[role="textbox"]',
      '.ql-editor',
      '[data-test-id="editor-content"]'
    ];

    let contentEntered = false;
    for (const selector of editorSelectors) {
      try {
        const editor = linkedinPage.locator(selector).first();
        if (await editor.count() > 0) {
          // Clear and enter content properly
          await editor.click();
          await linkedinPage.keyboard.press('Control+a');
          await linkedinPage.keyboard.press('Delete');
          // Type character by character with small delay
          await linkedinPage.keyboard.type(linkedinContent, { delay: 5 });
          console.log(`Entered content using selector: ${selector}`);
          contentEntered = true;
          break;
        }
      } catch (e) {
        console.log(`Selector ${selector} failed:`, e.message);
      }
    }

    // Fallback to JS evaluation if Playwright locators didn't work
    if (!contentEntered) {
      console.log('Using JS fallback for content entry...');
      await linkedinPage.evaluate((text) => {
        const editor = document.querySelector('[contenteditable="true"]') ||
                       document.querySelector('div[role="textbox"]') ||
                       document.querySelector('.ql-editor');
        if (editor) {
          editor.focus();
          // Use document.execCommand which properly triggers React events
          document.execCommand('selectAll', false, null);
          document.execCommand('delete', false, null);
          document.execCommand('insertText', false, text);
        }
      }, linkedinContent);
    }

    // Wait for React to process the content
    console.log('Waiting for content to be processed...');
    await linkedinPage.waitForTimeout(2000);
    await linkedinPage.screenshot({ path: './debug-linkedin-content.png' });

    // Debug: Log all buttons in the dialog
    const buttonInfo = await linkedinPage.evaluate(() => {
      const dialogs = document.querySelectorAll('[role="dialog"]');
      const allButtons = [];
      for (const dialog of dialogs) {
        const buttons = dialog.querySelectorAll('button');
        buttons.forEach(btn => {
          allButtons.push({
            text: btn.textContent?.trim(),
            disabled: btn.disabled,
            ariaLabel: btn.getAttribute('aria-label'),
            className: btn.className?.substring(0, 50)
          });
        });
      }
      return allButtons;
    });
    console.log('Buttons in dialog:', JSON.stringify(buttonInfo, null, 2));

    // Click post button - wait for it to be enabled first
    console.log('Clicking post button...');

    // Wait for Post button to become enabled (up to 15 seconds)
    let postClicked = false;
    let attempts = 0;
    const maxAttempts = 30;

    while (!postClicked && attempts < maxAttempts) {
      attempts++;

      // Try to click the Post button if it's enabled
      const clicked = await linkedinPage.evaluate(() => {
        const dialogs = document.querySelectorAll('[role="dialog"]');
        for (const dialog of dialogs) {
          const buttons = dialog.querySelectorAll('button');
          for (const btn of buttons) {
            const text = btn.textContent?.toLowerCase().trim() || '';
            // Look for button with "Post" text (may have extra whitespace)
            if (text === 'post' && !btn.disabled) {
              btn.scrollIntoView({ block: 'center', behavior: 'instant' });
              // Use HTMLElement.click() which properly triggers click events
              btn.click();
              // Also dispatch mouse events
              btn.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
              btn.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
              btn.dispatchEvent(new MouseEvent('click', { bubbles: true }));
              return true;
            }
          }
        }
        return false;
      });

      if (clicked) {
        postClicked = true;
        console.log(`Post button clicked after ${attempts} attempts`);
        break;
      }

      // If button still disabled, try triggering more input events every few attempts
      if (attempts % 5 === 0) {
        console.log(`Button still disabled after ${attempts} attempts, triggering more events...`);
        await linkedinPage.evaluate(() => {
          const editor = document.querySelector('[contenteditable="true"]') ||
                         document.querySelector('div[role="textbox"]');
          if (editor) {
            // Trigger React input event with proper detail
            const event = new InputEvent('input', {
              bubbles: true,
              inputType: 'insertText',
              data: editor.innerText
            });
            editor.dispatchEvent(event);
            editor.dispatchEvent(new Event('change', { bubbles: true }));
          }
        });
      }

      await linkedinPage.waitForTimeout(500);
    }

    if (!postClicked) {
      console.log('WARNING: Could not find enabled Post button after maximum attempts');
    }

    // Wait and check if modal closed (indicating successful post)
    console.log('Waiting for post submission...');
    await linkedinPage.waitForTimeout(5000);

    // Check if we're back on the feed (modal closed)
    const modalStillOpen = await linkedinPage.evaluate(() => {
      const dialogs = document.querySelectorAll('[role="dialog"]');
      // Check if any dialog is actually visible
      for (const dialog of dialogs) {
        const style = window.getComputedStyle(dialog);
        if (style.display !== 'none' && style.visibility !== 'hidden') {
          return true;
        }
      }
      return false;
    });

    if (modalStillOpen) {
      console.log('Warning: Modal still open - post may not have submitted');
      await linkedinPage.screenshot({ path: './error-linkedin-modal-open.png' });
      // Try pressing Escape to close modal
      await linkedinPage.keyboard.press('Escape');
      await linkedinPage.waitForTimeout(1000);
    } else {
      console.log('Modal closed - post likely successful');
    }

    await linkedinPage.screenshot({ path: './proof-day2-linkedin.png' });
    console.log('LinkedIn post process complete!');

    await browser.close();
  } catch (error) {
    console.error('Error:', error.message);
    if (linkedinPage) {
      await linkedinPage.screenshot({ path: './error-linkedin.png' }).catch(() => {});
    }
    if (browser) await browser.close();
    process.exit(1);
  }
})();
