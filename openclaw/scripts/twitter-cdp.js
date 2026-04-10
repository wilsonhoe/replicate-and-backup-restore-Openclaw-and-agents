const puppeteer = require('puppeteer');

async function connectToExistingChrome() {
  console.log('🔌 Connecting to existing Chrome session...\n');
  
  try {
    // Connect to existing Chrome with DevTools Protocol
    const browser = await puppeteer.connect({
      browserURL: 'http://127.0.0.1:9222',
      defaultViewport: null
    });

    console.log('✅ Connected to Chrome');

    // Get all pages/tabs
    const pages = await browser.pages();
    console.log(`Found ${pages.length} open tabs`);

    // Find or create Twitter developer page
    let twitterPage = null;
    for (const page of pages) {
      const url = page.url();
      console.log(`Tab: ${url.substring(0, 60)}...`);
      if (url.includes('developer.twitter.com')) {
        twitterPage = page;
        break;
      }
    }

    if (!twitterPage) {
      twitterPage = await browser.newPage();
      await twitterPage.goto('https://developer.twitter.com/en/portal/petition/essential/basic-info');
      console.log('📱 Opened Twitter Developer Portal');
    } else {
      console.log('📱 Using existing Twitter Developer Portal tab');
    }

    const wait = (ms) => new Promise(r => setTimeout(r, ms));

    // Wait for page load
    await wait(3000);

    // Screenshot current state
    await twitterPage.screenshot({ path: '/home/wls/.openclaw/workspace/twitter-cdp-1.png', fullPage: true });
    console.log('📸 Screenshot saved: twitter-cdp-1.png');

    // Check for login state
    const pageContent = await twitterPage.evaluate(() => document.body.innerText);
    console.log('Page content preview:', pageContent.substring(0, 200));

    // Try to find and click continue/app buttons
    const buttons = await twitterPage.$$('button');
    console.log(`Found ${buttons.length} buttons`);

    for (const btn of buttons) {
      try {
        const text = await btn.evaluate(el => el.innerText);
        if (text.includes('Continue') || text.includes('Next') || text.includes('Apply') || text.includes('Submit')) {
          console.log(`✅ Clicking button: "${text}"`);
          await btn.click();
          await wait(2000);
          await twitterPage.screenshot({ path: '/home/wls/.openclaw/workspace/twitter-cdp-2.png' });
        }
      } catch (e) {}
    }

    // Look for form elements
    const inputs = await twitterPage.$$('input:not([type="hidden"])');
    console.log(`Found ${inputs.length} input fields`);

    const textareas = await twitterPage.$$('textarea');
    console.log(`Found ${textareas.length} textarea fields`);

    const selects = await twitterPage.$$('select');
    console.log(`Found ${selects.length} select dropdowns`);

    // Fill any visible textareas
    for (const ta of textareas) {
      try {
        const visible = await ta.isIntersectingViewport();
        if (visible) {
          await ta.click();
          await ta.type('Automated content posting and engagement management for AI-powered business systems. Scheduling tweets and monitoring mentions for customer engagement.');
          console.log('✅ Filled textarea');
        }
      } catch (e) {}
    }

    // Select Singapore for country dropdown
    for (const sel of selects) {
      try {
        const name = await sel.evaluate(el => el.name || el.id || '');
        if (name.toLowerCase().includes('country')) {
          await sel.select('SG');
          console.log('✅ Selected country: Singapore');
        }
      } catch (e) {}
    }

    // Check all checkboxes
    const checkboxes = await twitterPage.$$('input[type="checkbox"]');
    for (const cb of checkboxes) {
      try {
        await cb.click();
        console.log('✅ Clicked checkbox');
        await wait(200);
      } catch (e) {}
    }

    await twitterPage.screenshot({ path: '/home/wls/.openclaw/workspace/twitter-cdp-3.png', fullPage: true });
    console.log('📸 Final screenshot saved');

    // Keep connected for manual interaction
    console.log('\n👀 Browser open - you can complete any remaining steps manually');
    console.log('Press Ctrl+C when done');

    // Keep process running
    await new Promise(() => {});

  } catch (error) {
    console.error('❌ Error:', error.message);
    console.log('\nMake sure Chrome is running with --remote-debugging-port=9222');
    console.log('Run: google-chrome --remote-debugging-port=9222 --user-data-dir="/home/wls/.config/google-chrome" --profile-directory="Default"');
  }
}

connectToExistingChrome();