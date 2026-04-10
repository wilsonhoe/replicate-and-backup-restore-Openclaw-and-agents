const puppeteer = require('puppeteer-core');

async function clickSSOButton() {
  console.log('🔌 Connecting to Chrome...');
  
  try {
    const browser = await puppeteer.connect({
      browserURL: 'http://127.0.0.1:9222',
      defaultViewport: null
    });

    const pages = await browser.pages();
    console.log(`Found ${pages.length} tabs`);

    // Find Google SSO page
    let page = pages.find(p => p.url().includes('accounts.google.com') && p.url().includes('signin'));
    
    if (!page) {
      console.log('Looking for X login redirect...');
      page = pages.find(p => p.url().includes('x.com') || p.url().includes('twitter.com'));
    }

    if (!page) {
      console.log('❌ No suitable page found');
      console.log('Pages:', pages.map(p => p.url()));
      return;
    }

    console.log('📱 Current page:', page.url());
    await page.bringToFront();

    // Wait for page load
    await new Promise(r => setTimeout(r, 2000));

    // Look for "Continue as" button
    console.log('🔍 Looking for "Continue as" button...');
    
    const buttons = await page.$$('button, [role="button"], div[role="button"]');
    console.log(`Found ${buttons.length} buttons`);

    for (const btn of buttons) {
      const text = await btn.evaluate(el => el.innerText || el.textContent || '');
      console.log('Button text:', text.substring(0, 50));
      
      if (text.toLowerCase().includes('continue') || text.toLowerCase().includes('lisa')) {
        console.log('✅ Found Continue button, clicking...');
        await btn.click();
        await new Promise(r => setTimeout(r, 3000));
        break;
      }
    }

    // Screenshot
    await page.screenshot({ path: '/home/wls/.openclaw/workspace/sso-click.png' });
    console.log('📸 Screenshot saved: sso-click.png');

    // Check result
    await new Promise(r => setTimeout(r, 3000));
    console.log('📱 New URL:', page.url());

    await page.screenshot({ path: '/home/wls/.openclaw/workspace/sso-after.png' });
    console.log('📸 After click screenshot saved');

  } catch (error) {
    console.error('❌ Error:', error.message);
  }
}

clickSSOButton();